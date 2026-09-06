import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  CANONICAL_SKILLS,
  NON_SKILL_REGISTERS,
  RETIRED,
  check,
  contractRows,
  publishedSkills,
  retiredRows,
} from "./check-standing-distribution.mjs";

const live = check();
assert.equal(live.ok, true, `expected green, got: ${live.problems.join("; ")}`);
assert.deepEqual(publishedSkills(), CANONICAL_SKILLS);
assert.deepEqual([...contractRows().keys()], CANONICAL_SKILLS);

const g2Skill = readFileSync(new URL("../skills/ship-it-or-fix-it/SKILL.md", import.meta.url), "utf8");
assert.match(g2Skill, /At ORACLE_FREEZE, apply the current `test-verification` guidance to public-seam,\s+failure-path, and durable-evidence design\./);
assert.ok(!g2Skill.includes("Substrate-8/team-hub-operator-web"));
assert.ok(!g2Skill.includes("not in this package"));

// Red: removal of an original public skill fails the manifest check.
const missingOriginal = check({ skills: CANONICAL_SKILLS.filter((id) => id !== "portable-adaptive-planning") });
assert.equal(missingOriginal.ok, false);
assert.ok(missingOriginal.problems.some((problem) => problem.includes("canonical manifest")));

// Both accepted adaptations are now required members of the canonical package.
for (const id of ["grilling", "unslop"]) {
  assert.ok(CANONICAL_SKILLS.includes(id));
  assert.equal(check({ skills: CANONICAL_SKILLS.filter((name) => name !== id) }).ok, false);
}

const contract = readFileSync(new URL("../STANDING-SOURCE-AND-ADAPTER-CONTRACT.md", import.meta.url), "utf8");
// An undeclared upstream addition still fails the distribution check.
const externalRow = contract.replace(
  "| `ship-it-or-fix-it` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |",
  "| `ship-it-or-fix-it` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |\n| `unaccepted-upstream-skill` | release | x | no |",
);
assert.notEqual(externalRow, contract);
const externalDistribution = check({ markdown: externalRow });
assert.equal(externalDistribution.ok, false);
assert.ok(externalDistribution.problems.some((problem) => problem.includes("distribution rows")));

for (const id of RETIRED) {
  assert.ok(retiredRows().has(id), `${id} must remain retired`);
}
for (const id of NON_SKILL_REGISTERS) {
  const regrown = check({ skills: [...CANONICAL_SKILLS, id] });
  assert.equal(regrown.ok, false, `${id} must remain a non-skill register`);
  assert.ok(regrown.problems.some((problem) => problem.includes("non-skill register")));
}

const noRegisterOwner = check({ markdown: contract.replace("relay/convergence/", "skills/convergence/") });
assert.equal(noRegisterOwner.ok, false);
assert.ok(noRegisterOwner.problems.some((problem) => problem.includes("Relay convergence owner")));

console.log("check-standing-distribution: canonical and red controls passed");

const manifest = JSON.parse(readFileSync(new URL("../current-skills.json", import.meta.url), "utf8"));
const duplicate = structuredClone(manifest);
duplicate.skills.push(structuredClone(duplicate.skills[0]));
assert.ok(check({ manifest: duplicate }).problems.some((problem) => problem.includes("duplicate current identity")));
const wrongIdentity = structuredClone(manifest);
wrongIdentity.skills.find((row) => row.name === "grilling").source.members[0].sha256 = "0".repeat(64);
assert.ok(check({ manifest: wrongIdentity }).problems.some((problem) => problem.includes("canonical member identity mismatch")));
