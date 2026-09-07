#!/usr/bin/env python3
"""Generate the portable conformance pack from the CURRENT manifest and canonical frontmatter.

Type: generator (Python 3 standard library only).
Responsibility: project one firing matrix, one probe set, and one pack manifest
from (a) the published CURRENT `current-skills.json`, (b) each canonical
SKILL.md frontmatter read through the canonical checker's source resolver at the
pinned source commits, (c) the Team Hub generated machine manifest as the
normalized cross-check for team-hub-skill/v1 frontmatter, and (d) two small
operator-owned inputs: `tools/conformance/activation-classes.json` and
`distribution/conformance/SURFACE-PROFILES.json`.
Authority: none. The pack is a derived distribution snapshot. It never resolves
sources itself; member bytes come only from the checker's `source_members`.

Usage:
  python3 tools/build-conformance-pack.py --checker PATH --checker-sha256 SHA \
      --manifest-commit COMMIT --source-root OWNER=CHECKOUT ... [--output DIR] [--check]

`--check` regenerates into a temporary directory and compares every byte with
the committed pack; it writes nothing. Exit 0 green, 1 red, 2 usage.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import types

OWNER = "Ezra144israel/governed-agent-skills"
TEAM_HUB = "Substrate-8/team-hub-operator-web"
MACHINE_MANIFEST = "skills/generated/skill-manifest.v1.json"
PACK_SCHEMA = "canonical-conformance-pack/v1"
MATRIX_SCHEMA = "canonical-firing-matrix/v1"
PROBES_SCHEMA = "canonical-conformance-probes/v2"
CLASSES = ("standing", "conditional", "explicit-operator")
EXCLUSION_CUES = ("Not needed", "Not for", "Skip ", "Never ", "Do not ", "Not needed")
TEAM_HUB_SCHEMA = "team-hub-skill/v1"
SELECTOR_KEYS = ("task_kinds", "surfaces", "risk_flags", "roles", "lanes")
# Keys that would restate skill semantics if they appeared in the profile layer.
SEMANTIC_KEYS = {"activation_triggers", "activation_exclusions", "task_kinds", "risk_flags", "graph_edges",
                 "child_references", "return_contributions", "full_load_required_when", "trigger_id",
                 "depends_on", "vetoes", "exclusions", "triggers"}
AUTHORED_FILES = ("SURFACE-PROFILES.json", "ADAPT-THIS-HOST.md")
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


class PackError(ValueError):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def identity(data):
    return {"bytes": len(data), "sha256": sha256(data)}


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def load_checker(path, expected):
    """Execute the measured checker bytes, as the promotion tool does."""
    path = Path(path).expanduser()
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 2_000_000:
        raise PackError("CHECKER_UNAVAILABLE")
    data = path.read_bytes()
    if sha256(data) != expected:
        raise PackError("CHECKER_IDENTITY_MISMATCH")
    module = types.ModuleType("canonical_skillsync")
    module.__file__ = str(path)
    exec(compile(data, str(path), "exec"), module.__dict__)
    return module, identity(data)


# ----------------------------------------------------------------- frontmatter

def parse_scalar(text):
    text = text.strip()
    if text == "[]":
        return []
    if text in ("null", "~"):
        return None
    if text == "true":
        return True
    if text == "false":
        return False
    if re.fullmatch(r"-?[0-9]+", text):
        return int(text)
    if len(text) >= 2 and text[0] == text[-1] == '"':
        body = text[1:-1]
        if re.search(r'(?<!\\)"', body):
            raise PackError("FRONTMATTER_UNSUPPORTED_QUOTING " + text[:40])
        return body.replace('\\"', '"').replace("\\\\", "\\")
    if len(text) >= 2 and text[0] == text[-1] == "'":
        return text[1:-1].replace("''", "'")
    if not text or text[0] in "{[&*!|>%@`" or text.startswith("- "):
        raise PackError("FRONTMATTER_UNSUPPORTED_SCALAR " + text[:40])
    return text


def split_entry(text):
    """`key: value` or `key:` on one line; the value may be empty."""
    match = re.match(r"([A-Za-z_][A-Za-z0-9_-]*):(?: (.*))?$", text)
    if not match:
        raise PackError("FRONTMATTER_UNSUPPORTED_LINE " + text[:60])
    return match.group(1), (match.group(2) or "")


def parse_frontmatter(text):
    """Block-style YAML subset used by team-hub-skill/v1 and plain skill frontmatter.

    Supports mappings, lists of scalars, lists of mappings, nested mappings,
    quoted and plain scalars, `[]`, `null`, booleans, and integers. Anything
    else fails closed; the parse is cross-checked against the Team Hub machine
    manifest for every team-hub-skill/v1 skill it owns.
    """
    lines = text.split("\n")
    if lines[0] != "---":
        raise PackError("FRONTMATTER_MISSING")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise PackError("FRONTMATTER_UNTERMINATED") from exc
    body = [line for line in lines[1:end] if line.strip()]
    if any("\t" in line for line in body):
        raise PackError("FRONTMATTER_TAB")
    rows = [(len(line) - len(line.lstrip(" ")), line.strip()) for line in body]
    value, index = parse_mapping(rows, 0, 0)
    if index != len(rows):
        raise PackError("FRONTMATTER_TRAILING_CONTENT")
    return value


def parse_mapping(rows, index, indent):
    result = {}
    while index < len(rows) and rows[index][0] == indent and not rows[index][1].startswith("- "):
        key, rest = split_entry(rows[index][1])
        if key in result:
            raise PackError("FRONTMATTER_DUPLICATE_KEY " + key)
        index += 1
        if rest.strip():
            result[key] = parse_scalar(rest)
            continue
        if index < len(rows) and rows[index][0] >= indent and rows[index][1].startswith("- "):
            result[key], index = parse_list(rows, index, rows[index][0])
        elif index < len(rows) and rows[index][0] > indent:
            result[key], index = parse_mapping(rows, index, rows[index][0])
        else:
            raise PackError("FRONTMATTER_EMPTY_VALUE " + key)
    if index < len(rows) and rows[index][0] > indent:
        raise PackError("FRONTMATTER_BAD_INDENT " + rows[index][1][:40])
    return result, index


def parse_list(rows, index, indent):
    items = []
    while index < len(rows) and rows[index][0] == indent and rows[index][1].startswith("- "):
        item = rows[index][1][2:]
        if re.match(r"[A-Za-z_][A-Za-z0-9_-]*:( |$)", item):
            rows[index] = (indent + 2, item)
            value, index = parse_mapping(rows, index, indent + 2)
            items.append(value)
        else:
            items.append(parse_scalar(item))
            index += 1
    return items, index


def sentences(text):
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]


# ------------------------------------------------------------------ inputs

def read_json(path):
    try:
        return json.loads(Path(path).read_bytes())
    except (OSError, ValueError) as exc:
        raise PackError(f"INPUT_UNREADABLE {path}: {exc}") from exc


def activation_classes(path):
    document = read_json(path)
    if document.get("schema") != "conformance-activation-classes/v1" or not isinstance(document.get("classes"), dict):
        raise PackError("INVALID_ACTIVATION_CLASSES")
    for name, row in document["classes"].items():
        if (not isinstance(row, dict) or row.get("class") not in CLASSES
                or not isinstance(row.get("basis"), str) or not row["basis"].strip()):
            raise PackError("INVALID_ACTIVATION_CLASS " + name)
    return document["classes"]


def validate_profiles(document):
    if not isinstance(document, dict) or document.get("schema") != "conformance-surface-profiles/v1":
        raise PackError("INVALID_SURFACE_PROFILES")
    profiles = document.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise PackError("SURFACE_PROFILES_EMPTY")

    def walk(value, trail):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in SEMANTIC_KEYS:
                    raise PackError("PROFILE_RESTATES_SKILL_SEMANTICS " + trail + key)
                walk(child, trail + key + ".")
        elif isinstance(value, list):
            for child in value:
                walk(child, trail)
    walk(profiles, "profiles.")
    surfaces = set()
    for name, profile in profiles.items():
        if not isinstance(profile.get("manifest_surfaces"), list) or not isinstance(profile.get("governed_roles"), list):
            raise PackError("PROFILE_INCOMPLETE " + name)
        surfaces.update(profile["manifest_surfaces"])
    return surfaces


# ------------------------------------------------------------------ matrix

def team_hub_machine_manifest(checker, roots, commit):
    root = Path(roots[TEAM_HUB]).expanduser()
    raw = checker.git_output(root, "show", commit + ":" + MACHINE_MANIFEST)
    document = checker.parse_json(raw)
    if document.get("schema_version") != "team-hub-skill-manifest/v1":
        raise PackError("INVALID_TEAM_HUB_MACHINE_MANIFEST")
    return document


ROW_IDS = ("trigger_id", "child_id", "contribution_id", "field_id", "target")
DERIVED_EDGE_TYPES = ("child_reference",)


def normalized_equal(authored, generated):
    """Frontmatter value versus the generated machine-manifest value.

    The generator may add derived keys to a row and derived rows to a list; it
    may not change an authored value. Rows are matched by their id key; scalar
    lists compare as sets; every authored key must be present and equal.
    """
    if isinstance(authored, dict):
        if not isinstance(generated, dict):
            return False
        return all(key in generated and normalized_equal(value, generated[key]) for key, value in authored.items())
    if isinstance(authored, list):
        if not isinstance(generated, list):
            return False
        if authored and all(isinstance(item, dict) for item in authored):
            key = next((k for k in ROW_IDS if all(k in item for item in authored)), None)
            if key is None:
                return len(authored) == len(generated) and all(normalized_equal(a, g) for a, g in zip(authored, generated))
            index = {item[key]: item for item in generated if isinstance(item, dict) and key in item}
            return all(item[key] in index and normalized_equal(item, index[item[key]]) for item in authored)
        return sorted(map(json.dumps, authored)) == sorted(map(json.dumps, generated))
    return authored == generated


def cross_check(name, frontmatter, machine_row):
    """Every authored frontmatter value must survive normalization unchanged.

    Derived machine rows (child_reference graph edges) and derived keys are
    allowed; a changed or missing authored value is a disagreement."""
    for key, value in frontmatter.items():
        if key in ("name", "description"):
            continue
        generated = machine_row.get(key)
        if key == "graph_edges" and isinstance(generated, list):
            generated = [edge for edge in generated if edge.get("type") not in DERIVED_EDGE_TYPES]
        if key not in machine_row or not normalized_equal(value, generated):
            raise PackError(f"FRONTMATTER_MACHINE_MANIFEST_DISAGREEMENT {name}.{key}")


def selector_signature(trigger):
    return json.dumps({key: sorted(trigger.get(key, [])) for key in SELECTOR_KEYS}, sort_keys=True)


def first_absent(vocabulary, present):
    for value in vocabulary:
        if value not in present:
            return value
    raise PackError("NO_NEGATIVE_SELECTOR_AVAILABLE")


def dependency_closure(frontmatter, current_names, machine_ids):
    closure = []
    for edge in frontmatter.get("graph_edges", []):
        if edge.get("type") != "depends_on":
            continue
        target = edge["target"]
        if target in current_names:
            resolution = "CURRENT manifest member"
        elif target in machine_ids:
            resolution = ("repository-scoped: declared only in " + TEAM_HUB
                          + "; not a CURRENT manifest member; resolve in that repository context. "
                          "Outside it, record REPOSITORY_CONTEXT_REQUIRED for this edge only")
        else:
            raise PackError("DEPENDENCY_UNRESOLVABLE " + target)
        closure.append({"target": target, "resolution": resolution,
                        "condition_trigger_ids": edge.get("condition_trigger_ids", [])})
    return closure


def build_row(name, row, manifest, members, frontmatter, classes, machine, current_names):
    source = row["source"]
    commit = manifest.origin_commit if source["commit"] == "MANIFEST" else source["commit"]
    canonical = {"repository": source["repository"], "commit": commit, "path": source["path"],
                 "members": [{"path": member["path"], "bytes": member["bytes"], "sha256": member["sha256"]}
                             for member in sorted(source["members"], key=lambda m: m["path"])]}
    for member in canonical["members"]:
        if identity(members[member["path"]]) != {"bytes": member["bytes"], "sha256": member["sha256"]}:
            raise PackError("MEMBER_IDENTITY_MISMATCH " + name + "/" + member["path"])
    declared = frontmatter.get("metadata_schema") == TEAM_HUB_SCHEMA
    description = frontmatter.get("description") or frontmatter.get("summary") or ""
    machine_ids = {entry["skill_id"] for entry in machine["skills"]}
    if declared:
        if source["repository"] == TEAM_HUB:
            cross_check(name, frontmatter, next(entry for entry in machine["skills"] if entry["skill_id"] == name))
        if name in classes:
            raise PackError("ACTIVATION_CLASS_OVERLAY_FOR_DECLARED_SKILL " + name)
        triggers = [{"trigger_id": trigger["trigger_id"], "description": trigger["description"],
                     "selectors": {key: sorted(trigger.get(key, [])) for key in SELECTOR_KEYS},
                     "full_load": trigger["trigger_id"] in frontmatter.get("full_load_required_when", [])}
                    for trigger in frontmatter["activation_triggers"]]
        activation_class = "conditional"
        basis = None
        exclusions = list(frontmatter.get("activation_exclusions", []))
        task_kinds = sorted({kind for trigger in triggers for kind in trigger["selectors"]["task_kinds"]})
        roles = sorted({role for trigger in triggers for role in trigger["selectors"]["roles"]})
        lanes = sorted({lane for trigger in triggers for lane in trigger["selectors"]["lanes"]})
        surfaces = sorted(frontmatter.get("surfaces", []))
        platforms = sorted(frontmatter.get("platforms", []))
        closure = dependency_closure(frontmatter, current_names, machine_ids)
        children = [{"child_id": child["child_id"], "path": child["path"],
                     "activation_trigger_ids": child.get("activation_trigger_ids", []),
                     "load_condition": ("when one of activation_trigger_ids fires" if child.get("activation_trigger_ids")
                                        else "only on the explicit condition the skill body states; never on the parent's ordinary triggers")}
                    for child in frontmatter.get("child_references", [])]
        contributions = [{"contribution_id": item["contribution_id"], "requirement": item.get("requirement"),
                          "activation_trigger_ids": item.get("activation_trigger_ids", []),
                          "fields": [field["field_id"] for field in item.get("fields", [])]}
                         for item in frontmatter.get("return_contributions", [])]
        version = frontmatter.get("version")
    else:
        if name not in classes:
            raise PackError("ACTIVATION_CLASS_UNDECLARED " + name)
        overlay = classes[name]
        if overlay["basis"] not in description:
            raise PackError("ACTIVATION_CLASS_BASIS_ABSENT " + name)
        activation_class, basis = overlay["class"], overlay["basis"]
        triggers = [{"trigger_id": name + "/description", "description": description, "selectors": None, "full_load": True}]
        exclusions = [sentence for sentence in sentences(description) if sentence.startswith(EXCLUSION_CUES)]
        task_kinds, roles, lanes, surfaces, platforms = [], [], [], [], ["portable"]
        closure, children, contributions = [], [], []
        version = None
        if overlay.get("negative_scenario"):
            exclusions.append("probe scenario (not a source rule): " + overlay["negative_scenario"])
    targets = {surface: row["targets"][surface]["adaptation"] for surface in sorted(row["targets"])}
    effect = ("Load receipt names `" + name + "`; the response applies: " + (frontmatter.get("summary") or sentences(description)[0])
              + (("; the return carries " + ", ".join(c["contribution_id"] for c in contributions)) if contributions else ""))
    return {
        "skill_id": name, "version": version, "canonical_identity": canonical,
        "frontmatter_schema": TEAM_HUB_SCHEMA if declared else "name-description",
        "activation_class": activation_class, "activation_class_basis": basis,
        "positive_triggers": triggers, "exclusions_and_vetoes": exclusions,
        "dependency_closure": closure, "child_references": children,
        "eligibility": {"task_kinds": task_kinds, "surfaces": surfaces, "roles": roles, "lanes": lanes, "platforms": platforms},
        "distribution_targets": targets, "return_contributions": contributions,
        "qualification_routes": {surface: qualification_route(target) for surface, target in row["targets"].items()},
        "expected_effect": effect, "positive_probe_ids": [], "negative_probe_ids": [],
        "host_capability_exception": "NONE",
    }


def build_probes(rows, vocabulary, retired):
    probes = []
    by_id = {row["skill_id"]: row for row in rows}

    def add(probe_id, family, covers, scenario, expected, negative=False):
        probes.append({"probe_id": probe_id, "family": family, "polarity": "negative" if negative else "positive",
                       "covers": sorted(covers), "scenario": scenario, "expected": expected})
        for skill in covers:
            by_id[skill]["negative_probe_ids" if negative else "positive_probe_ids"].append(probe_id)

    standing = [r["skill_id"] for r in rows if r["activation_class"] == "standing"]
    add("P-STANDING-ENTRY", "standing", standing,
        "A fresh session starts with any nontrivial task and no explicit skill request.",
        "The first substantive response carries a load receipt naming every standing skill; each is applied.")
    add("N-STANDING-RESIDENCY", "standing", standing,
        "After entry, a later turn asks a trivial factual question; no compaction, source-identity change, or operator refresh occurred.",
        "No standing skill is re-read or re-announced; residency holds.", negative=True)
    signatures = {}
    for row in rows:
        if row["activation_class"] != "conditional" or row["frontmatter_schema"] != TEAM_HUB_SCHEMA:
            continue
        for trigger in row["positive_triggers"]:
            signatures.setdefault(selector_signature(trigger["selectors"]), []).append((row["skill_id"], trigger))
    for number, signature in enumerate(sorted(signatures), 1):
        members = signatures[signature]
        selectors = json.loads(signature)
        covers = sorted({skill for skill, _ in members})
        add(f"P-SEL-{number:02d}", "selector", covers,
            "Task selectors: " + "; ".join(f"{key}={','.join(v) or '*'}" for key, v in selectors.items())
            + ". Scenarios: " + " | ".join(f"{skill}/{trigger['trigger_id']}: {trigger['description']}" for skill, trigger in members),
            "Each admitted skill fires for its scenario with a load receipt and required dependency/child routing. "
            "Activation evidence is sufficient; domain-task completion is not required.")
        probes[-1]["trigger_cases"] = [{"skill_id": skill, "trigger_id": trigger["trigger_id"],
                                         "selectors": trigger["selectors"]} for skill, trigger in members]
    for row in rows:
        if row["activation_class"] == "conditional" and row["frontmatter_schema"] == TEAM_HUB_SCHEMA:
            kind = first_absent(vocabulary["task_kinds"], set(row["eligibility"]["task_kinds"]))
            surface = first_absent(vocabulary["surfaces"], set(row["eligibility"]["surfaces"]))
            add("N-SEL-" + row["skill_id"], "selector", [row["skill_id"]],
                f"A task classified task_kind={kind} on surface={surface} with no risk flags, no role, no lane.",
                "The skill does not fire; its body is not loaded.", negative=True)
        elif row["activation_class"] == "conditional":
            add("P-DESC-" + row["skill_id"], "description", [row["skill_id"]],
                "A request matching the skill description: " + row["positive_triggers"][0]["description"],
                "The skill fires and the load receipt names it.")
            add("N-DESC-" + row["skill_id"], "description", [row["skill_id"]],
                "A request inside the skill's own exclusions: " + (" ".join(row["exclusions_and_vetoes"]) or "outside the described scope"),
                "The skill does not fire.", negative=True)
        elif row["activation_class"] == "explicit-operator":
            add("P-EXPLICIT-" + row["skill_id"], "explicit-operator", [row["skill_id"]],
                "The operator explicitly instructs the activation named in the description: " + row["activation_class_basis"],
                "The skill fires only then and the load receipt names it.")
            add("N-EXPLICIT-" + row["skill_id"], "explicit-operator", [row["skill_id"]],
                "A task whose class alone might suggest the skill, with no explicit operator instruction: "
                + (" ".join(row["exclusions_and_vetoes"]) or "no operator instruction present"),
                "The skill does not self-fire; at most it asks once.", negative=True)
    dependents = [r["skill_id"] for r in rows if r["dependency_closure"]]
    add("P-DEPCLOSURE", "dependency", dependents,
        "A skill with a dependency_closure fires on one of its positive triggers.",
        "Test each admitted owner and each applicable dependency edge in its required context. "
        "Resolve repo-grounding in Substrate 8 repository context; outside it, record "
        "REPOSITORY_CONTEXT_REQUIRED for that edge without failing unrelated firing probes.")
    with_children = [r["skill_id"] for r in rows if r["child_references"]]
    add("P-CHILDREF", "child-reference", with_children,
        "A child reference's activation trigger fires (or the explicit condition the body states occurs).",
        "Exactly that child loads in addition to the root body.")
    add("N-CHILDREF", "child-reference", with_children,
        "The parent fires on a trigger that is not in the child's activation_trigger_ids.",
        "The child is not loaded.", negative=True)
    add("P-SEAT-HOSTED", "seat", [],
        "A hosted-coordination surface (profile hosted-coordination) is assigned ORCHESTRATOR or PRESSURE-TESTER.",
        "Role-specific material for that governed role is applied; ADVISOR assignment applies no governed authority.")
    add("N-SEAT-LOCAL-PROMOTION", "seat", [r["skill_id"] for r in rows if any(
        "orchestrator" in t["selectors"]["roles"] for t in r["positive_triggers"] if t["selectors"])],
        "A local-builder-reviewer surface receives a dispatch authored by an ORCHESTRATOR (transport `SEAT:` field present).",
        "The surface stays BUILDER or REVIEWER; orchestrator-role triggers do not fire; no seat promotion.", negative=True)
    contributors = [r["skill_id"] for r in rows if r["return_contributions"]]
    add("P-RETURN-CONTRIB", "return-contribution", contributors,
        "A skill that owns a return contribution fires on one of that contribution's activation triggers.",
        "The return carries the contribution's fields.")
    add("N-RETIRED", "retired", [],
        "Any task; an isolated inventory fixture contains a replica named " + ", ".join(sorted(retired)) + ".",
        "No retired name becomes active or appears in the load receipt; a present replica is reported BLOCKED (RETIRED_REPLICA_PRESENT).", negative=True)
    add("P-HOSTEXC-BLOCKED", "host-capability", [],
        "An isolated Antigravity parser fixture rejects canonical unslop frontmatter "
        "under KNOWN-ANTIGRAVITY-UNSLOP-YAML. No live skill root is modified.",
        "The host reports BLOCKED for that skill with a concrete host_capability_exception; it never drops the skill silently or alters its bytes.")
    for row in rows:
        if not row["positive_probe_ids"] or not row["negative_probe_ids"]:
            raise PackError("PROBE_COVERAGE_GAP " + row["skill_id"])
    return probes


# Qualification projects the fixed global library onto profile seats and target
# admission. It does not change selectors or load canonical BLOCKED members.
PRESERVED_REASON = ("Keep the accepted surface-specific continuity adapter. Its existing account repair "
                    "and acceptance gate is separate from this source consolidation.")
ROLE_NAMES = {"PRESSURE-TESTER": "pressure-test", "ORCHESTRATOR": "orchestrator",
              "BUILDER": "builder", "REVIEWER": "reviewer"}


def trigger_allowed(trigger, profile_name, profile):
    selectors = trigger.get("selectors")
    roles = selectors.get("roles", []) if selectors else []
    if set(roles) & {"orchestrator", "pressure-test"} and profile_name != "hosted-coordination":
        return False
    return not roles or bool(set(roles) & {ROLE_NAMES.get(role, role.lower())
                                          for role in profile["governed_roles"]})


def qualification_route(target):
    adaptation = target["adaptation"]
    if adaptation == "BLOCKED":
        route = "preserved-surface-adapter" if target.get("reason") == PRESERVED_REASON else "blocked"
    elif adaptation == "NOT_TARGET":
        route = "not-target"
    else:
        route = "canonical-target"
    return {"route": route, "adaptation": adaptation, "reason": target.get("reason", ""),
            "canonical_body_allowed": route == "canonical-target"}


def profile_members(row, field, profile_name, profile):
    allowed = {t["trigger_id"] for t in row["positive_triggers"] if trigger_allowed(t, profile_name, profile)}
    return [
        item["child_id" if field == "child_references" else "contribution_id"]
        for item in row[field] if not item["activation_trigger_ids"]
        or allowed.intersection(item["activation_trigger_ids"])]


def add_qualification(probes, rows, profiles):
    by_id = {row["skill_id"]: row for row in rows}
    for probe in probes:
        pid = probe["probe_id"]
        modes = {
            "P-STANDING-ENTRY": ["fresh-session-entry"],
            "N-STANDING-RESIDENCY": ["later-turn-residency"],
            "P-DEPCLOSURE": ["repository-context"],
            "P-SEAT-HOSTED": ["alternate-seat-session"],
            "P-RETURN-CONTRIB": ["alternate-seat-session"],
            "N-RETIRED": ["isolated-inventory-fixture"],
            "P-HOSTEXC-BLOCKED": ["host-parser-fixture"],
        }.get(pid, ["ordinary-turn"])
        if pid.startswith("P-EXPLICIT-"):
            modes = ["operator-authorized"]
        if any(case["selectors"]["roles"] for case in probe.get("trigger_cases", [])):
            modes = ["alternate-seat-session"]
        probe["execution_modes"] = modes
        probe["evidence_contract"] = {
            "scope": "activation-load-routing" if probe["family"] == "selector" else probe["family"],
            "domain_task_completion_required": False,
            "operator_authority_source": "real-current-operator-instruction" if "operator-authorized" in modes else "unchanged",
            "quoted_probe_text_grants_authority": False,
            "results": "per admitted skill and applicable child/contribution; blocked admission stays skill-local",
        }
        if pid == "P-RETURN-CONTRIB":
            probe["evidence_contract"]["scope"] = "required-return-fields"
        if pid == "N-STANDING-RESIDENCY":
            probe["evidence_contract"]["prerequisite"] = "same-session P-STANDING-ENTRY receipt; later distinct turn"
        if pid == "N-RETIRED":
            probe["inventory_fixture"] = {"live_root_allowed": False, "required_report": "RETIRED_REPLICA_PRESENT"}
        if pid == "P-DEPCLOSURE":
            probe["repository_context"] = TEAM_HUB
            probe["evidence_contract"]["outside_repository"] = "REPOSITORY_CONTEXT_REQUIRED for the edge only"
        if pid == "P-HOSTEXC-BLOCKED":
            probe["host_condition"] = {"surface": "antigravity", "exception_id": "KNOWN-ANTIGRAVITY-UNSLOP-YAML",
                                       "premise": "isolated parser fixture rejects canonical unslop frontmatter"}
        probe["qualification"] = {}
        for pname, profile in profiles.items():
            status, reason = "APPLICABLE", "global probe applies to this profile"
            if pid == "P-SEAT-HOSTED" and pname != "hosted-coordination":
                status, reason = "NOT_APPLICABLE", "hosted seat positive belongs only to hosted-coordination"
            elif pid == "N-SEAT-LOCAL-PROMOTION" and pname != "local-builder-reviewer":
                status, reason = "NOT_APPLICABLE", "local seat non-promotion probe"
            elif pid == "P-HOSTEXC-BLOCKED" and "antigravity" not in profile["manifest_surfaces"]:
                status, reason = "NOT_APPLICABLE", "Antigravity parser condition only"
            elif probe.get("trigger_cases") and not any(trigger_allowed(c, pname, profile) for c in probe["trigger_cases"]):
                status, reason = "NOT_APPLICABLE", "no positive scenario has a permitted profile seat"
            elif pid.startswith("P-EXPLICIT-"):
                status, reason = "OPERATOR_ACTION_REQUIRED", "requires real operator instruction; quoted probe text is inert"
            hosts = {}
            for surface in profile["manifest_surfaces"]:
                host_status, host_reason = status, reason
                if pid == "P-HOSTEXC-BLOCKED" and surface != "antigravity":
                    host_status, host_reason = "NOT_APPLICABLE", "Antigravity parser condition only"
                cover = {}
                if host_status != "NOT_APPLICABLE":
                    for name in probe["covers"]:
                        row = by_id[name]
                        if probe.get("trigger_cases") and not any(c["skill_id"] == name and trigger_allowed(c, pname, profile)
                                                                   for c in probe["trigger_cases"]):
                            continue
                        members = None
                        if probe["family"] in ("child-reference", "return-contribution"):
                            field = "child_references" if probe["family"] == "child-reference" else "return_contributions"
                            members = profile_members(row, field, pname, profile)
                            if not members:
                                continue
                        route = row["qualification_routes"][surface]
                        if route["route"] == "not-target":
                            continue
                        cover[name] = {"route": route["route"]}
                        if members is not None:
                            cover[name]["member_ids"] = members
                if probe["covers"] and not cover and host_status != "NOT_APPLICABLE":
                    host_status, host_reason = "NOT_APPLICABLE", "no target owner with an eligible scenario"
                hosts[surface] = {"applicability": host_status, "reason": host_reason, "cover_candidates": cover}
            states = {h["applicability"] for h in hosts.values()}
            # A profile with a named host condition remains applicable, with a
            # mandatory host refinement. The host never chooses the branch.
            profile_status = ("APPLICABLE" if "APPLICABLE" in states else "OPERATOR_ACTION_REQUIRED"
                              if "OPERATOR_ACTION_REQUIRED" in states else "NOT_APPLICABLE")
            probe["qualification"][pname] = {"applicability": profile_status, "hosts": hosts}


def admitted_cover(probe, profile, surface, admission_evidence):
    """Resolve generated candidates using identity-verified admission receipts.

    The caller must verify receipt provenance against accepted source evidence
    and measured host bytes. This function checks receipt completeness, not
    authenticity, and never reads or loads a skill body.
    """
    host = probe["qualification"][profile]["hosts"][surface]
    active, blocked = {}, {}
    for name, candidate in host["cover_candidates"].items():
        route = candidate["route"]
        receipt = admission_evidence.get(name, {})
        if route == "blocked":
            blocked[name] = "TARGET_BLOCKED"
            continue
        required = ("accepted_source", "acceptance_record", "accepted_identity", "observed_identity")
        if route == "preserved-surface-adapter":
            accepted, observed = receipt.get("accepted_identity", {}), receipt.get("observed_identity", {})
            complete = (all(receipt.get(k) for k in required) and isinstance(accepted, dict)
                        and isinstance(accepted.get("bytes"), int) and accepted["bytes"] > 0
                        and isinstance(accepted.get("sha256"), str) and HEX64.fullmatch(accepted["sha256"])
                        and accepted == observed)
            if not complete:
                blocked[name] = "ACCEPTED_ADAPTER_IDENTITY_REQUIRED"
                continue
        elif receipt.get("identity_verified") is not True:
            blocked[name] = "TARGET_IDENTITY_REQUIRED"
            continue
        active[name] = candidate
    return {"applicability": host["applicability"], "admitted": active, "blocked": blocked}


def firing_result(probe, observation):
    """Check selector evidence only; full domain work is outside this seam.

    Apply per admitted skill/scenario. Values represent independently captured
    receipts, not a host's unsupported assertion. Admission is checked first.
    """
    if probe["family"] != "selector":
        raise PackError("NOT_A_SELECTOR_PROBE")
    if probe["polarity"] == "negative":
        return "PASS" if observation.get("fired") is False and observation.get("body_loaded") is False else "BLOCKED"
    required = ("fired", "body_loaded", "dependency_routing_correct", "child_routing_correct")
    return "PASS" if all(observation.get(k) is True for k in required) and observation.get("load_receipt") else "BLOCKED"


def operator_activation_ready(probe, authority):
    """Probe text is data. Only a separately verified operator event can unlock."""
    if "operator-authorized" not in probe["execution_modes"]:
        raise PackError("NOT_AN_OPERATOR_PROBE")
    return (authority.get("origin") == "current-operator-instruction" and authority.get("quoted") is False
            and authority.get("activation_explicit") is True and bool(authority.get("event_identity")))


def retired_fixture_result(retired_names, inventory_names, loaded_names, reported_blocked):
    """Judge isolated-inventory observations without touching a live root."""
    present = set(retired_names) & set(inventory_names)
    return "PASS" if present and not (set(retired_names) & set(loaded_names)) and present <= set(reported_blocked) else "BLOCKED"


def matrix_markdown(matrix):
    lines = ["<!-- GENERATED FILE. Source: FIRING-MATRIX.generated.json. Do not edit. -->",
             "# Canonical firing matrix", "",
             f"Manifest `{matrix['manifest']['revision']}` at `{matrix['manifest']['commit']}`, "
             f"SHA-256 `{matrix['manifest']['sha256']}`. {len(matrix['skills'])} CURRENT skills; "
             f"retired and never active: {', '.join('`' + r + '`' for r in matrix['retired'])}.", "",
             "Selectors are necessary conditions; the trigger description is the semantic condition. "
             "Vetoes are absolute. Standing skills load once at entry. Explicit-operator skills never self-fire.", "",
             "| Skill | Class | Version | Source | Positive triggers | Exclusions / vetoes | Dependency closure | Children | Eligibility | Targets | Probes (+ / -) | Host exception |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for row in matrix["skills"]:
        source = row["canonical_identity"]
        triggers = ", ".join(t["trigger_id"] for t in row["positive_triggers"])
        exclusions = "; ".join(row["exclusions_and_vetoes"]) or "none declared"
        closure = ", ".join(d["target"] + ("" if d["resolution"].startswith("CURRENT") else " (repository-scoped)")
                            for d in row["dependency_closure"]) or "none"
        children = ", ".join(c["child_id"] for c in row["child_references"]) or "none"
        eligibility = row["eligibility"]
        eligible = (f"tasks {','.join(eligibility['task_kinds']) or 'n/d'}; surfaces {','.join(eligibility['surfaces']) or 'n/d'}; "
                    f"roles {','.join(eligibility['roles']) or 'any'}; platforms {','.join(eligibility['platforms'])}")
        targets = ", ".join(f"{s}:{a}" for s, a in row["distribution_targets"].items())
        probes = ", ".join(row["positive_probe_ids"]) + " / " + ", ".join(row["negative_probe_ids"])
        lines.append(f"| `{row['skill_id']}` | {row['activation_class']} | {row['version'] or 'by identity'} | "
                     f"`{source['repository']}@{source['commit'][:12]}` `{source['path'] or '.'}` ({len(source['members'])} members) | "
                     f"{triggers} | {exclusions} | {closure} | {children} | {eligible} | {targets} | {probes} | {row['host_capability_exception']} |")
    lines += ["", "## Expected effect when a skill fires", ""]
    for row in matrix["skills"]:
        lines.append(f"- `{row['skill_id']}`: {row['expected_effect']}")
    return ("\n".join(lines) + "\n").encode()


def probes_markdown(probes):
    lines = ["<!-- GENERATED FILE. Source: CONFORMANCE-PROBES.generated.json. Do not edit. -->",
             "# Conformance probes", "",
             "Account for every global ID. Execute only its generated profile and host applicability. "
             "Use the required execution modes and admission route in ADAPT-THIS-HOST.md.", ""]
    for family in sorted({p["family"] for p in probes["probes"]}):
        lines += [f"## {family}", ""]
        for probe in [p for p in probes["probes"] if p["family"] == family]:
            covers = ", ".join("`" + s + "`" for s in probe["covers"]) or "(all skills / host)"
            lines += [f"### `{probe['probe_id']}` ({probe['polarity']})", "", f"Covers: {covers}", "",
                      f"Scenario: {probe['scenario']}", "", f"Expected: {probe['expected']}", ""]
            if "qualification" in probe:
                lines += ["Execution modes: " + ", ".join(probe["execution_modes"]), "",
                          "| Profile | Host | Applicability | Candidate owners |",
                          "|---|---|---|---|"]
                for profile, plan in sorted(probe["qualification"].items()):
                    for host, entry in sorted(plan["hosts"].items()):
                        owners = ", ".join(name + ":" + cover["route"] for name, cover in sorted(entry["cover_candidates"].items())) or "none"
                        lines.append(f"| {profile} | {host} | {entry['applicability']} | {owners} |")
                lines += ["", "Use the machine row for exact reasons and child/contribution case IDs.", ""]
    return ("\n".join(lines).rstrip("\n") + "\n").encode()


# ------------------------------------------------------------------ pack

def generate(checker, checker_identity, manifest_path, manifest_commit, roots, repo_root):
    if not HEX40.fullmatch(manifest_commit):
        raise PackError("INVALID_MANIFEST_COMMIT")
    manifest_bytes = checker.regular_bytes(manifest_path.parent, manifest_path.name)
    manifest = checker.Manifest(manifest_bytes, {**identity(manifest_bytes), "commit": manifest_commit})
    if manifest.candidate:
        raise PackError("MANIFEST_NOT_CURRENT")
    classes = activation_classes(repo_root / "tools/conformance/activation-classes.json")
    authored = {name: (repo_root / "distribution/conformance" / name).read_bytes() for name in AUTHORED_FILES}
    profile_surfaces = validate_profiles(json.loads(authored["SURFACE-PROFILES.json"]))
    unknown = profile_surfaces - set(manifest.surfaces)
    if unknown:
        raise PackError("PROFILE_NAMES_UNKNOWN_SURFACE " + ",".join(sorted(unknown)))
    current = {name: row for name, row in manifest.skills.items() if row["lifecycle"] == "CURRENT"}
    retired = sorted(name for name, row in manifest.skills.items() if row["lifecycle"] != "CURRENT")
    team_hub_commit = next(row["source"]["commit"] for row in current.values() if row["source"]["repository"] == TEAM_HUB)
    machine = team_hub_machine_manifest(checker, roots, team_hub_commit)
    vocabulary = machine["covered_vocabulary"]
    rows, files = [], {}
    for name, row in current.items():
        members = checker.source_members(manifest, name, roots)
        frontmatter = parse_frontmatter(members["SKILL.md"].decode("utf-8"))
        rows.append(build_row(name, row, manifest, members, frontmatter, classes, machine, set(current)))
        for path, data in members.items():
            files["skills/" + name + "/" + path] = data
    extra = sorted(set(classes) - set(current))
    if extra:
        raise PackError("ACTIVATION_CLASS_FOR_NON_CURRENT " + ",".join(extra))
    source_commits = sorted({(row["canonical_identity"]["repository"], row["canonical_identity"]["commit"]) for row in rows})
    matrix = {"schema": MATRIX_SCHEMA,
              "manifest": {"repository": manifest.repository, "commit": manifest_commit, "revision": manifest.revision,
                           **identity(manifest_bytes)},
              "sources": [{"repository": repo, "commit": commit} for repo, commit in source_commits],
              "team_hub_machine_manifest": {"commit": team_hub_commit, "source_corpus_sha256": machine["source_corpus_sha256"]},
              "selector_vocabulary": vocabulary, "retired": retired, "skills": rows}
    probes = {"schema": PROBES_SCHEMA, "manifest_sha256": matrix["manifest"]["sha256"],
              "probes": build_probes(rows, vocabulary, retired)}
    add_qualification(probes["probes"], rows, json.loads(authored["SURFACE-PROFILES.json"])["profiles"])
    files["current-skills.json"] = manifest_bytes
    files["FIRING-MATRIX.generated.json"] = json_bytes(matrix)
    files["FIRING-MATRIX.generated.md"] = matrix_markdown(matrix)
    files["CONFORMANCE-PROBES.generated.json"] = json_bytes(probes)
    files["CONFORMANCE-PROBES.md"] = probes_markdown(probes)
    files.update(authored)
    pack = {"schema": PACK_SCHEMA, "manifest": matrix["manifest"], "sources": matrix["sources"],
            "checker": checker_identity, "authored_inputs": sorted(AUTHORED_FILES) + ["tools/conformance/activation-classes.json"],
            "files": {path: identity(data) for path, data in sorted(files.items())},
            "note": "Derived distribution snapshot. Not a source owner. Regenerate with tools/build-conformance-pack.py; "
                    "identical source commits and inputs produce identical bytes."}
    files["PACK-MANIFEST.json"] = json_bytes(pack)
    return files


def write_pack(files, output):
    output.mkdir(parents=True, exist_ok=True)
    for path in sorted(p for p in output.rglob("*") if p.is_file()):
        if path.relative_to(output).as_posix() not in files:
            path.unlink()
    for path, data in files.items():
        target = output / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def compare_pack(files, output):
    problems = []
    existing = {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob("*") if p.is_file()}
    for path in sorted(set(files) | set(existing)):
        if path not in existing:
            problems.append("missing: " + path)
        elif path not in files:
            problems.append("unexpected: " + path)
        elif files[path] != existing[path]:
            problems.append("differs: " + path)
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--checker", required=True)
    parser.add_argument("--checker-sha256", required=True)
    parser.add_argument("--manifest", default=None, help="defaults to <repo>/current-skills.json")
    parser.add_argument("--manifest-commit", required=True, help="published commit that carries the CURRENT manifest")
    parser.add_argument("--source-root", action="append", default=[], metavar="OWNER=CHECKOUT")
    parser.add_argument("--output", default=None, help="defaults to <repo>/distribution/conformance")
    parser.add_argument("--check", action="store_true", help="regenerate to a temporary directory and compare; write nothing")
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parents[1]
    try:
        checker, checker_identity = load_checker(args.checker, args.checker_sha256)
        roots = {}
        for option in args.source_root:
            owner, separator, path = option.partition("=")
            if not separator or not owner or not path:
                raise PackError("INVALID_SOURCE_ROOT " + option)
            roots[owner] = path
        manifest_path = Path(args.manifest).expanduser() if args.manifest else repo_root / "current-skills.json"
        output = Path(args.output).expanduser() if args.output else repo_root / "distribution/conformance"
        files = generate(checker, checker_identity, manifest_path, args.manifest_commit, roots, repo_root)
        if args.check:
            problems = compare_pack(files, output)
            if problems:
                for problem in problems:
                    print("RED: " + problem)
                return 1
            print(f"GREEN: conformance pack reproduces {len(files)} files byte for byte at {output}")
            return 0
        write_pack(files, output)
        pack = json.loads(files["PACK-MANIFEST.json"])
        print(json.dumps({"status": "WRITTEN", "output": str(output), "files": len(files),
                          "manifest": pack["manifest"], "sources": pack["sources"]}, indent=2, sort_keys=True))
        return 0
    except (PackError, OSError, KeyError, TypeError, UnicodeDecodeError) as exc:
        print("BLOCKED: " + str(exc), file=sys.stderr)
        return 1
    except Exception as exc:  # checker CurrentError and friends
        if type(exc).__name__ == "CurrentError":
            print("BLOCKED: " + str(exc), file=sys.stderr)
            return 1
        raise


if __name__ == "__main__":
    sys.exit(main())
