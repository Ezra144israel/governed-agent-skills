#!/usr/bin/env python3
"""Behavioral tests for tools/build-conformance-pack.py.

Pure seams (frontmatter parser, activation overlay, profile validation, row and
probe construction) run everywhere. The integration checks run against the real
pinned sources only when CONFORMANCE_TEST_INPUTS names a JSON file with
`checker`, `checker_sha256`, `manifest_commit`, and `source_roots`; otherwise
they are skipped and say so.

Run:  python3 tools/test_build_conformance_pack.py
"""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("build_conformance_pack", HERE / "build-conformance-pack.py")
gen = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gen)

DECLARED = """---
metadata_schema: team-hub-skill/v1
summary: "Finds what a change could break: beyond the diff."
skill_id: example
version: 1.0.0
lifecycle_status: active
family: verification
capabilities: []
source_provenance:
  kind: original
  references: []
  note: null
authority_boundary: docs-only
activation_triggers:
- trigger_id: change-risk-review
  task_kinds:
  - review
  - verification
  risk_flags: []
  path_globs: []
  roles: []
  lanes: []
  surfaces:
  - repository
  description: a change's risk is assessed
activation_exclusions: []
full_load_required_when:
- change-risk-review
platforms:
- portable
surfaces:
- repository
graph_edges:
- type: depends_on
  target: repo-grounding
  condition_trigger_ids: []
child_references:
- child_id: example/child
  path: skills/example/reference/child.md
  activation_trigger_ids:
  - change-risk-review
return_contributions:
- contribution_id: example/proof
  activation_trigger_ids:
  - change-risk-review
  requirement: required
  order: 310
  fields:
  - field_id: cases
    value_type: checklist
    required: true
    allowed_values: []
    prompt: List cases.
---

# Body
"""

PLAIN = """---
name: plain
description: Use when the operator asks for it. Not needed for quick factual questions.
---

# Plain
"""

VOCABULARY = {"task_kinds": ["architecture", "copy", "review", "verification"],
              "surfaces": ["api", "documentation", "repository"],
              "risk_flags": [], "roles": ["builder", "orchestrator"], "lanes": [], "platforms": ["portable"]}


class FakeManifest:
    origin_commit = "1" * 40


def manifest_row(name, repository, path, members, targets=("codex",)):
    return {"name": name, "lifecycle": "CURRENT",
            "source": {"repository": repository, "commit": "MANIFEST" if repository == gen.OWNER else "2" * 40,
                       "path": path, "members": [{"path": p, **gen.identity(d)} for p, d in members.items()]},
            "targets": {surface: {"adaptation": "release"} for surface in targets}}


class FrontmatterParserTest(unittest.TestCase):
    def test_declared_frontmatter_round_trips_typed_values(self):
        parsed = gen.parse_frontmatter(DECLARED)
        self.assertEqual(parsed["summary"], "Finds what a change could break: beyond the diff.")
        self.assertEqual(parsed["capabilities"], [])
        self.assertIsNone(parsed["source_provenance"]["note"])
        self.assertEqual(parsed["activation_triggers"][0]["task_kinds"], ["review", "verification"])
        self.assertEqual(parsed["return_contributions"][0]["order"], 310)
        self.assertIs(parsed["return_contributions"][0]["fields"][0]["required"], True)
        self.assertEqual(parsed["child_references"][0]["activation_trigger_ids"], ["change-risk-review"])

    def test_plain_frontmatter(self):
        parsed = gen.parse_frontmatter(PLAIN)
        self.assertEqual(parsed, {"name": "plain",
                                  "description": "Use when the operator asks for it. Not needed for quick factual questions."})

    def test_unsupported_shapes_fail_closed(self):
        for text, reason in ((DECLARED.replace("---\n\n# Body", "# Body"), "UNTERMINATED"),
                             ("# no frontmatter\n", "MISSING"),
                             ("---\nkey: value\nkey: again\n---\n", "DUPLICATE_KEY"),
                             ("---\nkey: {a: 1}\n---\n", "UNSUPPORTED_SCALAR"),
                             ("---\nkey:\n---\n", "EMPTY_VALUE"),
                             ("---\nkey: >\n  folded\n---\n", "UNSUPPORTED"),
                             ("---\n\tkey: value\n---\n", "TAB"),
                             ("---\nkey: value\n  stray: deeper\n---\n", "BAD_INDENT")):
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(gen.PackError, reason):
                    gen.parse_frontmatter(text)


class InputValidationTest(unittest.TestCase):
    def test_activation_classes_require_known_class_and_basis(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "classes.json"
            good = {"schema": "conformance-activation-classes/v1",
                    "classes": {"plain": {"class": "conditional", "basis": "Use when the operator asks for it"}}}
            path.write_text(json.dumps(good))
            self.assertEqual(gen.activation_classes(path)["plain"]["class"], "conditional")
            for bad in ({**good, "schema": "other"},
                        {**good, "classes": {"plain": {"class": "sometimes", "basis": "x"}}},
                        {**good, "classes": {"plain": {"class": "standing", "basis": ""}}}):
                path.write_text(json.dumps(bad))
                with self.assertRaises(gen.PackError):
                    gen.activation_classes(path)

    def test_profiles_may_not_restate_skill_semantics(self):
        good = {"schema": "conformance-surface-profiles/v1",
                "profiles": {"p": {"manifest_surfaces": ["codex"], "governed_roles": ["BUILDER"]}}}
        self.assertEqual(gen.validate_profiles(good), {"codex"})
        for key in ("activation_triggers", "task_kinds", "vetoes", "depends_on"):
            bad = copy.deepcopy(good)
            bad["profiles"]["p"][key] = ["anything"]
            with self.subTest(key=key), self.assertRaisesRegex(gen.PackError, "RESTATES_SKILL_SEMANTICS"):
                gen.validate_profiles(bad)
        nested = copy.deepcopy(good)
        nested["profiles"]["p"]["notes"] = [{"child_references": []}]
        with self.assertRaisesRegex(gen.PackError, "RESTATES_SKILL_SEMANTICS"):
            gen.validate_profiles(nested)
        with self.assertRaisesRegex(gen.PackError, "PROFILE_INCOMPLETE"):
            gen.validate_profiles({"schema": "conformance-surface-profiles/v1", "profiles": {"p": {}}})

    def test_shipped_authored_inputs_validate(self):
        root = HERE.parent
        gen.activation_classes(root / "tools/conformance/activation-classes.json")
        surfaces = gen.validate_profiles(json.loads((root / "distribution/conformance/SURFACE-PROFILES.json").read_bytes()))
        manifest_surfaces = set(json.loads((root / "current-skills.json").read_bytes())["surfaces"])
        self.assertTrue(surfaces <= manifest_surfaces, surfaces - manifest_surfaces)


class RowAndProbeTest(unittest.TestCase):
    def setUp(self):
        self.members = {"SKILL.md": DECLARED.encode(), "reference/child.md": b"# child\n"}
        self.machine = {"skills": [{"skill_id": "repo-grounding"}, {"skill_id": "example"}],
                        "covered_vocabulary": VOCABULARY}

    def declared_row(self, classes=None, machine=None):
        row = manifest_row("example", gen.TEAM_HUB, "skills/example", self.members)
        frontmatter = gen.parse_frontmatter(DECLARED)
        machine = machine or {**self.machine, "skills": [{"skill_id": "repo-grounding"},
                                                        {"skill_id": "example", **{k: v for k, v in frontmatter.items()}}]}
        return gen.build_row("example", row, FakeManifest(), self.members, frontmatter, classes or {}, machine, {"example"})

    def test_declared_row_is_conditional_with_closure_children_and_contributions(self):
        built = self.declared_row()
        self.assertEqual(built["activation_class"], "conditional")
        self.assertEqual(built["positive_triggers"][0]["selectors"]["task_kinds"], ["review", "verification"])
        self.assertEqual(built["dependency_closure"][0]["target"], "repo-grounding")
        self.assertIn("repository-scoped", built["dependency_closure"][0]["resolution"])
        self.assertEqual(built["child_references"][0]["child_id"], "example/child")
        self.assertEqual(built["return_contributions"][0]["fields"], ["cases"])
        self.assertEqual(built["eligibility"]["task_kinds"], ["review", "verification"])
        self.assertEqual(built["host_capability_exception"], "NONE")
        self.assertEqual(built["canonical_identity"]["commit"], "2" * 40)

    def test_declared_row_refuses_machine_manifest_disagreement_and_overlay(self):
        frontmatter = gen.parse_frontmatter(DECLARED)
        drifted = {**self.machine, "skills": [{"skill_id": "repo-grounding"},
                                              {"skill_id": "example", **frontmatter, "version": "9.9.9"}]}
        with self.assertRaisesRegex(gen.PackError, "DISAGREEMENT example.version"):
            self.declared_row(machine=drifted)
        with self.assertRaisesRegex(gen.PackError, "OVERLAY_FOR_DECLARED_SKILL"):
            self.declared_row(classes={"example": {"class": "standing", "basis": "x"}})

    def test_member_identity_mismatch_is_refused(self):
        row = manifest_row("example", gen.TEAM_HUB, "skills/example", self.members)
        row["source"]["members"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(gen.PackError, "MEMBER_IDENTITY_MISMATCH"):
            gen.build_row("example", row, FakeManifest(), self.members, gen.parse_frontmatter(DECLARED), {},
                          {**self.machine, "skills": [{"skill_id": "example", **gen.parse_frontmatter(DECLARED)}]}, {"example"})

    def test_plain_row_needs_overlay_bound_to_description(self):
        members = {"SKILL.md": PLAIN.encode()}
        row = manifest_row("plain", gen.OWNER, "skills/plain", members)
        frontmatter = gen.parse_frontmatter(PLAIN)
        with self.assertRaisesRegex(gen.PackError, "ACTIVATION_CLASS_UNDECLARED"):
            gen.build_row("plain", row, FakeManifest(), members, frontmatter, {}, self.machine, {"plain"})
        with self.assertRaisesRegex(gen.PackError, "BASIS_ABSENT"):
            gen.build_row("plain", row, FakeManifest(), members, frontmatter,
                          {"plain": {"class": "conditional", "basis": "never said"}}, self.machine, {"plain"})
        built = gen.build_row("plain", row, FakeManifest(), members, frontmatter,
                              {"plain": {"class": "conditional", "basis": "Use when the operator asks"}}, self.machine, {"plain"})
        self.assertEqual(built["activation_class"], "conditional")
        self.assertEqual(built["exclusions_and_vetoes"], ["Not needed for quick factual questions."])
        self.assertEqual(built["canonical_identity"]["commit"], "1" * 40)
        self.assertEqual(built["positive_triggers"][0]["selectors"], None)

    def test_probes_cover_every_row_positively_and_negatively(self):
        rows = [self.declared_row()]
        members = {"SKILL.md": PLAIN.encode()}
        rows.append(gen.build_row("plain", manifest_row("plain", gen.OWNER, "skills/plain", members), FakeManifest(), members,
                                  gen.parse_frontmatter(PLAIN), {"plain": {"class": "standing", "basis": "Use when"}},
                                  self.machine, {"plain"}))
        rows.append(gen.build_row("g2", manifest_row("g2", gen.OWNER, "skills/g2", members), FakeManifest(), members,
                                  gen.parse_frontmatter(PLAIN), {"g2": {"class": "explicit-operator", "basis": "Use when"}},
                                  self.machine, {"g2"}))
        probes = gen.build_probes(rows, VOCABULARY, ["retired-one"])
        ids = [p["probe_id"] for p in probes]
        self.assertEqual(len(ids), len(set(ids)))
        for row in rows:
            self.assertTrue(row["positive_probe_ids"] and row["negative_probe_ids"], row["skill_id"])
        negative = next(p for p in probes if p["probe_id"] == "N-SEL-example")
        self.assertIn("task_kind=architecture", negative["scenario"])
        self.assertIn("surface=api", negative["scenario"])
        self.assertIn("retired-one", next(p for p in probes if p["probe_id"] == "N-RETIRED")["scenario"])
        self.assertEqual(next(p for p in probes if p["probe_id"] == "P-RETURN-CONTRIB")["covers"], ["example"])
        self.assertEqual(next(p for p in probes if p["probe_id"] == "N-EXPLICIT-g2")["polarity"], "negative")

    def test_probe_coverage_gap_is_refused(self):
        members = {"SKILL.md": PLAIN.encode()}
        row = gen.build_row("plain", manifest_row("plain", gen.OWNER, "skills/plain", members), FakeManifest(), members,
                            gen.parse_frontmatter(PLAIN), {"plain": {"class": "conditional", "basis": "Use when"}},
                            self.machine, {"plain"})
        row["activation_class"] = "unknown"
        with self.assertRaisesRegex(gen.PackError, "PROBE_COVERAGE_GAP plain"):
            gen.build_probes([row], VOCABULARY, [])

    def test_markdown_projections_are_functions_of_the_json(self):
        rows = [self.declared_row()]
        matrix = {"schema": gen.MATRIX_SCHEMA, "manifest": {"revision": "r", "commit": "1" * 40, "sha256": "a" * 64},
                  "retired": ["retired-one"], "skills": rows}
        probes = {"schema": gen.PROBES_SCHEMA, "manifest_sha256": "a" * 64,
                  "probes": gen.build_probes(rows, VOCABULARY, ["retired-one"])}
        self.assertEqual(gen.matrix_markdown(matrix), gen.matrix_markdown(json.loads(json.dumps(matrix))))
        self.assertIn(b"`example` | conditional", gen.matrix_markdown(matrix))
        self.assertIn(b"### `N-SEL-example` (negative)", gen.probes_markdown(probes))


@unittest.skipUnless(os.environ.get("CONFORMANCE_TEST_INPUTS"), "CONFORMANCE_TEST_INPUTS not set; real-source checks skipped")
class RealSourceTest(unittest.TestCase):
    """Generation against the pinned real sources: reproducible, complete, and green through the CLI."""

    @classmethod
    def setUpClass(cls):
        inputs = json.loads(Path(os.environ["CONFORMANCE_TEST_INPUTS"]).read_text())
        cls.checker, cls.checker_identity = gen.load_checker(inputs["checker"], inputs["checker_sha256"])
        cls.inputs = inputs
        cls.root = HERE.parent
        cls.files = gen.generate(cls.checker, cls.checker_identity, cls.root / "current-skills.json",
                                 inputs["manifest_commit"], inputs["source_roots"], cls.root)

    def qualification_data(self):
        probes = json.loads(self.files["CONFORMANCE-PROBES.generated.json"])["probes"]
        rows = json.loads(self.files["FIRING-MATRIX.generated.json"])["skills"]
        return {p["probe_id"]: p for p in probes}, {r["skill_id"]: r for r in rows}

    def test_all_49_ids_and_canonical_meanings_survive(self):
        def original(path):
            return json.loads(subprocess.check_output([
                "git", "-C", str(self.root), "show",
                "02a34c775350b17c6150890d035802d44a012992:distribution/conformance/" + path]))
        probes, rows = self.qualification_data()
        prior = original("CONFORMANCE-PROBES.generated.json")["probes"]
        self.assertEqual(len(probes), 49)
        self.assertEqual(set(probes), {p["probe_id"] for p in prior})
        for old in prior:
            for key in ("family", "polarity", "covers"):
                self.assertEqual(probes[old["probe_id"]][key], old[key])
        for old in original("FIRING-MATRIX.generated.json")["skills"]:
            for key in ("canonical_identity", "activation_class", "positive_triggers", "exclusions_and_vetoes",
                        "eligibility", "distribution_targets", "child_references", "return_contributions"):
                self.assertEqual(rows[old["skill_id"]][key], old[key], (old["skill_id"], key))

    def test_every_profile_and_host_has_fixed_applicability(self):
        probes, _ = self.qualification_data()
        profiles = json.loads(self.files["SURFACE-PROFILES.json"])["profiles"]
        for probe in probes.values():
            self.assertEqual(set(probe["qualification"]), set(profiles))
            for name, profile in profiles.items():
                plan = probe["qualification"][name]
                self.assertIn(plan["applicability"], ("APPLICABLE", "NOT_APPLICABLE", "OPERATOR_ACTION_REQUIRED"))
                self.assertEqual(set(plan["hosts"]), set(profile["manifest_surfaces"]))
                for host in plan["hosts"].values():
                    self.assertIn(host["applicability"], ("APPLICABLE", "NOT_APPLICABLE", "OPERATOR_ACTION_REQUIRED"))
                    self.assertTrue(host["reason"])
                    if host["applicability"] == "NOT_APPLICABLE":
                        self.assertFalse(host["cover_candidates"])

    def test_local_seats_are_never_hosted_positive_cases(self):
        probes, _ = self.qualification_data()
        for p in probes.values():
            if p["probe_id"] == "P-SEAT-HOSTED" or any(
                    set(c["selectors"]["roles"]) & {"orchestrator", "pressure-test"}
                    for c in p.get("trigger_cases", [])):
                self.assertEqual(p["qualification"]["hosted-coordination"]["applicability"], "APPLICABLE")
                for name in ("local-builder-reviewer", "external-host-adapter", "chatgpt-hosted-application"):
                    self.assertEqual(p["qualification"][name]["applicability"], "NOT_APPLICABLE")
        self.assertEqual(probes["N-SEAT-LOCAL-PROMOTION"]["qualification"]["local-builder-reviewer"]["applicability"], "APPLICABLE")

    def test_parser_condition_is_antigravity_only(self):
        probes, _ = self.qualification_data()
        p = probes["P-HOSTEXC-BLOCKED"]
        for plan in p["qualification"].values():
            for surface, host in plan["hosts"].items():
                self.assertEqual(host["applicability"], "APPLICABLE" if surface == "antigravity" else "NOT_APPLICABLE")
        self.assertEqual(p["execution_modes"], ["host-parser-fixture"])

    def test_selector_pass_needs_actual_firing_but_no_domain_completion(self):
        probes, _ = self.qualification_data()
        p = next(p for p in probes.values() if p["probe_id"].startswith("P-SEL-"))
        evidence = {"fired": True, "body_loaded": True, "load_receipt": "observed-load-identity",
                    "dependency_routing_correct": True, "child_routing_correct": True,
                    "domain_task_completed": False}
        self.assertEqual(gen.firing_result(p, evidence), "PASS")
        for key in ("fired", "body_loaded", "load_receipt", "dependency_routing_correct", "child_routing_correct"):
            self.assertEqual(gen.firing_result(p, {**evidence, key: False}), "BLOCKED", key)
        negative = next(p for p in probes.values() if p["probe_id"].startswith("N-SEL-"))
        self.assertEqual(gen.firing_result(negative, {"fired": False, "body_loaded": False}), "PASS")
        self.assertEqual(gen.firing_result(negative, {"fired": False, "body_loaded": True}), "BLOCKED")

    def test_preserved_adapter_identity_is_required_and_failure_is_skill_local(self):
        probes, rows = self.qualification_data()
        p = probes["P-CHILDREF"]
        host = p["qualification"]["local-builder-reviewer"]["hosts"]["codex"]
        receipts = {name: {"identity_verified": True} for name in host["cover_candidates"]}
        route = rows["continuity-handoff"]["qualification_routes"]["codex"]
        self.assertEqual(route["route"], "preserved-surface-adapter")
        self.assertFalse(route["canonical_body_allowed"])
        missing = gen.admitted_cover(p, "local-builder-reviewer", "codex", receipts)
        self.assertEqual(missing["blocked"], {"continuity-handoff": "ACCEPTED_ADAPTER_IDENTITY_REQUIRED"})
        self.assertIn("technique-scout", missing["admitted"])
        identity = {"bytes": 12, "sha256": "a" * 64}
        proof = {"accepted_source": "immutable-source-receipt", "acceptance_record": "immutable-acceptance-receipt",
                 "accepted_identity": identity, "observed_identity": identity}
        receipts["continuity-handoff"] = proof
        accepted = gen.admitted_cover(p, "local-builder-reviewer", "codex", receipts)
        self.assertFalse(accepted["blocked"])
        self.assertIn("continuity-handoff", accepted["admitted"])
        for key in proof:
            receipts["continuity-handoff"] = {k: v for k, v in proof.items() if k != key}
            self.assertIn("continuity-handoff", gen.admitted_cover(p, "local-builder-reviewer", "codex", receipts)["blocked"])
        receipts["continuity-handoff"] = {**proof, "observed_identity": {"bytes": 13, "sha256": "a" * 64}}
        self.assertIn("continuity-handoff", gen.admitted_cover(p, "local-builder-reviewer", "codex", receipts)["blocked"])
        self.assertEqual(gen.qualification_route({"adaptation": "BLOCKED", "reason": "unverified target"})["route"], "blocked")

    def test_child_and_contribution_owners_follow_profile_and_admission(self):
        probes, _ = self.qualification_data()
        for pid in ("P-CHILDREF", "N-CHILDREF", "P-RETURN-CONTRIB"):
            p = probes[pid]
            local = p["qualification"]["local-builder-reviewer"]["hosts"]["codex"]["cover_candidates"]
            hosted = p["qualification"]["hosted-coordination"]["hosts"]["chatgpt"]["cover_candidates"]
            local_ids = local["continuity-handoff"]["member_ids"]
            self.assertTrue(local_ids)
            self.assertTrue(all("orchestrator" not in x and "pressure-test" not in x and "relay-queue" not in x for x in local_ids))
            self.assertTrue(all("builder-session" not in x for x in hosted["continuity-handoff"]["member_ids"]))
            grok = p["qualification"]["external-host-adapter"]["hosts"]["grok"]["cover_candidates"]
            if pid == "P-RETURN-CONTRIB":
                # General continuity contributions are role-agnostic. Grok's
                # target is BLOCKED, so it remains visible but never admitted.
                self.assertEqual(grok["continuity-handoff"]["route"], "blocked")
                resolved = gen.admitted_cover(p, "external-host-adapter", "grok", {})
                self.assertNotIn("continuity-handoff", resolved["admitted"])
                self.assertEqual(resolved["blocked"]["continuity-handoff"], "TARGET_BLOCKED")
            else:
                self.assertNotIn("continuity-handoff", grok)

    def test_repository_dependency_does_not_poison_unrelated_firing(self):
        probes, rows = self.qualification_data()
        p = probes["P-DEPCLOSURE"]
        self.assertEqual(p["execution_modes"], ["repository-context"])
        self.assertEqual(p["repository_context"], gen.TEAM_HUB)
        self.assertIn("edge only", p["evidence_contract"]["outside_repository"])
        self.assertNotIn("repo-grounding", rows)
        for row in rows.values():
            for edge in row["dependency_closure"]:
                if edge["target"] == "repo-grounding":
                    self.assertIn("Outside it, record REPOSITORY_CONTEXT_REQUIRED for this edge only", edge["resolution"])
        for p in probes.values():
            if p["family"] == "selector":
                self.assertNotIn("repo-grounding", p["covers"])
                self.assertNotIn("repository-context", p["execution_modes"])

    def test_retired_refusal_uses_isolated_inventory(self):
        probes, _ = self.qualification_data()
        p = probes["N-RETIRED"]
        self.assertEqual(p["execution_modes"], ["isolated-inventory-fixture"])
        self.assertFalse(p["inventory_fixture"]["live_root_allowed"])
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp) / "run-review-repair-loop"
            fixture.mkdir()
            (fixture / "SKILL.md").write_text("inert retired inventory fixture")
            inventory = [p.name for p in Path(tmp).iterdir()]
            retired = ["run-review-repair-loop"]
            self.assertEqual(gen.retired_fixture_result(retired, inventory, [], retired), "PASS")
            self.assertEqual(gen.retired_fixture_result(retired, inventory, retired, retired), "BLOCKED")
            self.assertEqual(gen.retired_fixture_result(retired, inventory, [], []), "BLOCKED")

    def test_entry_residency_and_real_operator_action_are_distinct(self):
        probes, _ = self.qualification_data()
        self.assertEqual(probes["P-STANDING-ENTRY"]["execution_modes"], ["fresh-session-entry"])
        self.assertEqual(probes["N-STANDING-RESIDENCY"]["execution_modes"], ["later-turn-residency"])
        self.assertIn("same-session", probes["N-STANDING-RESIDENCY"]["evidence_contract"]["prerequisite"])
        p = probes["P-EXPLICIT-ship-it-or-fix-it"]
        event = {"origin": "current-operator-instruction", "quoted": False,
                 "activation_explicit": True, "event_identity": "real-event-receipt"}
        self.assertTrue(gen.operator_activation_ready(p, event))
        for bad in ({**event, "quoted": True}, {**event, "origin": "probe-fixture"},
                    {**event, "activation_explicit": False}, {**event, "event_identity": ""}):
            self.assertFalse(gen.operator_activation_ready(p, bad))
        for plan in p["qualification"].values():
            for host in plan["hosts"].values():
                if host["cover_candidates"]:
                    self.assertEqual(host["applicability"], "OPERATOR_ACTION_REQUIRED")

    def test_every_current_skill_once_and_no_retired_row(self):
        manifest = json.loads((self.root / "current-skills.json").read_bytes())
        matrix = json.loads(self.files["FIRING-MATRIX.generated.json"])
        current = sorted(r["name"] for r in manifest["skills"] if r["lifecycle"] == "CURRENT")
        retired = sorted(r["name"] for r in manifest["skills"] if r["lifecycle"] != "CURRENT")
        self.assertEqual(sorted(r["skill_id"] for r in matrix["skills"]), current)
        self.assertEqual(len({r["skill_id"] for r in matrix["skills"]}), len(matrix["skills"]))
        self.assertEqual(matrix["retired"], retired)
        self.assertFalse(set(retired) & {r["skill_id"] for r in matrix["skills"]})

    def test_dependencies_children_and_members_resolve(self):
        matrix = json.loads(self.files["FIRING-MATRIX.generated.json"])
        for row in matrix["skills"]:
            paths = {m["path"] for m in row["canonical_identity"]["members"]}
            for member in row["canonical_identity"]["members"]:
                self.assertEqual(gen.identity(self.files["skills/" + row["skill_id"] + "/" + member["path"]]),
                                 {"bytes": member["bytes"], "sha256": member["sha256"]})
            for child in row["child_references"]:
                self.assertIn(child["path"].split("/", 2)[-1], paths, child)
            for dependency in row["dependency_closure"]:
                self.assertTrue(dependency["resolution"].startswith(("CURRENT", "repository-scoped")), dependency)
            for part in Path(row["canonical_identity"]["path"]).parts:
                self.assertNotIn(part.casefold(), self.checker.FORBIDDEN_SOURCE_PARTS)

    def test_generation_is_reproducible_and_projections_agree(self):
        again = gen.generate(self.checker, self.checker_identity, self.root / "current-skills.json",
                             self.inputs["manifest_commit"], self.inputs["source_roots"], self.root)
        self.assertEqual(self.files, again)
        matrix = json.loads(self.files["FIRING-MATRIX.generated.json"])
        probes = json.loads(self.files["CONFORMANCE-PROBES.generated.json"])
        self.assertEqual(gen.matrix_markdown(matrix), self.files["FIRING-MATRIX.generated.md"])
        self.assertEqual(gen.probes_markdown(probes), self.files["CONFORMANCE-PROBES.md"])
        pack = json.loads(self.files["PACK-MANIFEST.json"])
        self.assertEqual(set(pack["files"]), set(self.files) - {"PACK-MANIFEST.json"})

    def test_cli_check_is_green_against_the_committed_pack(self):
        command = [sys.executable, "-B", str(HERE / "build-conformance-pack.py"), "--check",
                   "--checker", self.inputs["checker"], "--checker-sha256", self.inputs["checker_sha256"],
                   "--manifest-commit", self.inputs["manifest_commit"]]
        for owner, path in self.inputs["source_roots"].items():
            command += ["--source-root", f"{owner}={path}"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("GREEN", result.stdout)

    def test_check_goes_red_on_a_modified_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "pack"
            gen.write_pack(self.files, output)
            (output / "FIRING-MATRIX.generated.md").write_bytes(b"edited\n")
            problems = gen.compare_pack(self.files, output)
            self.assertEqual(problems, ["differs: FIRING-MATRIX.generated.md"])


if __name__ == "__main__":
    unittest.main()
