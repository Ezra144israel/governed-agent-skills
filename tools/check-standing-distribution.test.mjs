import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { check, contractRows, retiredRows, publishedSkills, registerOwnerStatements, skillOwnerSections, NON_SKILL_REGISTERS, RETIRED } from "./check-standing-distribution.mjs";

// Green against the real package.
const live = check();
assert.equal(live.ok, true, `expected green, got: ${live.problems.join("; ")}`);
assert.ok(live.published > 0, "no skills discovered");

// The five skills this package publishes are exactly the contract's rows.
const published = publishedSkills();
assert.deepEqual(published, ["governed-operator", "grilling", "reasoning-doctrine", "ship-it-or-fix-it", "unslop"]);

// Red: a retired skill reappearing in the package fails.
const regrown = check({ skills: [...published, "portable-adaptive-planning"] });
assert.equal(regrown.ok, false);
assert.ok(regrown.problems.some((p) => p.includes("regrew")), "must name the regrowth");

// Red: a published skill with no contract row fails.
const uncovered = check({ skills: [...published, "brand-new-skill"] });
assert.equal(uncovered.ok, false);
assert.ok(uncovered.problems.some((p) => p.includes("no distribution row")));

// Red: dropping the must-not-regrow table fails, so the guard cannot be deleted quietly.
const stripped = check({ markdown: "| `governed-operator` | release | x | no |\n| `grilling` | release | x | no |\n| `reasoning-doctrine` | release | x | no |\n| `ship-it-or-fix-it` | release | x | no |\n| `unslop` | release | x | no |\n" });
assert.equal(stripped.ok, false);
assert.ok(stripped.problems.some((p) => p.includes("must-not-regrow")));

// The retired set covers every generic workflow wrapper the pruning removed.
for (const id of ["orchestrator-seat", "builder-return", "reviewer-validation", "run-review-repair-loop"]) {
  assert.ok(RETIRED.includes(id), `retired set must include ${id}`);
}
// A skill sourced elsewhere, and a register that is not a skill, must both be
// blocked from regrowing here.
for (const id of ["test-verification", "pending-convergence"]) {
  const regrewElsewhere = check({ skills: [...published, id] });
  assert.equal(regrewElsewhere.ok, false, `${id} must not be publishable here`);
  assert.ok(regrewElsewhere.problems.some((p) => p.includes("must not be published")));
  assert.ok(retiredRows().has(id), `${id} must be recorded in the must-not-regrow table`);
}

// The owner-prose seam is real, not vacuous: both skill-owner sections parse,
// and the register-owner statement exists.
assert.deepEqual(skillOwnerSections().map((s) => s.heading.trim()), [
  "## Distribution table",
  "## Ownership boundary with `Substrate-8/team-hub-operator-web`",
]);
assert.ok(registerOwnerStatements().has("pending-convergence"));

// Red: reintroducing the forbidden skill-source owner statement fails.
const contractText = readFileSync(new URL("../STANDING-SOURCE-AND-ADAPTER-CONTRACT.md", import.meta.url), "utf8");
const forbiddenOwner = contractText.replace(
  "`test-verification` and `technique-scout` are Substrate-specific skill",
  "`test-verification`, `pending-convergence`, and `technique-scout` are Substrate-specific skill",
);
assert.notEqual(forbiddenOwner, contractText, "red control must actually change the owner section");
const ownerRed = check({ markdown: forbiddenOwner });
assert.equal(ownerRed.ok, false);
assert.ok(ownerRed.problems.some((p) => p.includes("skill-source owner statement") && p.includes("pending-convergence")));

// Red: dropping the register-owner statement fails.
const noStatement = contractText.replace("## Register owner:", "## Note:");
const statementRed = check({ markdown: noStatement });
assert.equal(statementRed.ok, false);
assert.ok(statementRed.problems.some((p) => p.includes("no register-owner statement")));

// Red: a register-owner statement that names no Relay convergence owner fails.
const wrongOwner = contractText.split("relay/convergence/").join("skills/convergence/");
const wrongOwnerRed = check({ markdown: wrongOwner });
assert.equal(wrongOwnerRed.ok, false);
assert.ok(wrongOwnerRed.problems.some((p) => p.includes("does not name the Relay convergence owner")));

// Green is restored from the real file.
assert.equal(check().ok, true, "green must be restored after the red controls");

assert.ok(NON_SKILL_REGISTERS.includes("pending-convergence"));
assert.ok(retiredRows().has("portable-adaptive-planning"));
assert.ok(contractRows().has("governed-operator"));

console.log("check-standing-distribution: 28/28 assertions passed");
