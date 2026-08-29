import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  CANONICAL_SKILLS,
  EXTERNAL_NOT_DISTRIBUTED,
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

// Red: removal of an original public skill fails the exact-six check.
const missingOriginal = check({ skills: CANONICAL_SKILLS.filter((id) => id !== "portable-adaptive-planning") });
assert.equal(missingOriginal.ok, false);
assert.ok(missingOriginal.problems.some((problem) => problem.includes("canonical six")));

// Red: either external skill returning as a package folder fails.
for (const id of EXTERNAL_NOT_DISTRIBUTED) {
  const reintroduced = check({ skills: [...CANONICAL_SKILLS, id] });
  assert.equal(reintroduced.ok, false, `${id} must not be packageable`);
  assert.ok(reintroduced.problems.some((problem) => problem.includes("external skill must not be packaged")));
}

const contract = readFileSync(new URL("../STANDING-SOURCE-AND-ADAPTER-CONTRACT.md", import.meta.url), "utf8");
// Red: an external distribution row fails even when no external folder exists.
const externalRow = contract.replace(
  "| `ship-it-or-fix-it` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |",
  "| `ship-it-or-fix-it` | release | Claude Code, Codex, Agents, Claude shared, ChatGPT project | no |\n| `grilling` | release | x | no |",
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
