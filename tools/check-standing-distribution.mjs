#!/usr/bin/env node
// Proves that this package distributes only its canonical six skills.
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CONTRACT = join(ROOT, "STANDING-SOURCE-AND-ADAPTER-CONTRACT.md");
const SKILLS = join(ROOT, "skills");

export const CANONICAL_SKILLS = Object.freeze([
  "reasoning-doctrine",
  "governed-operator",
  "write-maintainable-code",
  "portable-adaptive-planning",
  "test-verification",
  "ship-it-or-fix-it",
]);
export const RETIRED = Object.freeze([
  "run-review-repair-loop",
  "scouted-rules",
  "orchestrator-seat",
  "builder-return",
  "reviewer-validation",
]);
export const NON_SKILL_REGISTERS = Object.freeze(["pending-convergence"]);
export const EXTERNAL_NOT_DISTRIBUTED = Object.freeze(["grilling", "unslop"]);

function section(markdown, heading) {
  const start = markdown.indexOf(heading);
  if (start === -1) return "";
  const end = markdown.indexOf("\n## ", start + heading.length);
  return markdown.slice(start, end === -1 ? undefined : end);
}

export function publishedSkills(skillsDir = SKILLS) {
  const found = readdirSync(skillsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && existsSync(join(skillsDir, entry.name, "SKILL.md")))
    .map((entry) => entry.name);
  return CANONICAL_SKILLS.filter((id) => found.includes(id))
    .concat(found.filter((id) => !CANONICAL_SKILLS.includes(id)).sort());
}

export function contractRows(markdown = readFileSync(CONTRACT, "utf8")) {
  const rows = new Map();
  for (const line of section(markdown, "## Distribution table").split("\n")) {
    const match = /^\|\s*\`([a-z0-9-]+)\`[^|]*\|\s*([^|]+?)\s*\|/.exec(line);
    if (match) rows.set(match[1], match[2].trim());
  }
  return rows;
}

export function retiredRows(markdown = readFileSync(CONTRACT, "utf8")) {
  return new Set([...section(markdown, "## Retired: must not regrow").matchAll(/^\|\s*\`([a-z0-9-]+)\`/gm)].map((match) => match[1]));
}

export function check({ skills = publishedSkills(), markdown = readFileSync(CONTRACT, "utf8") } = {}) {
  const rows = contractRows(markdown);
  const problems = [];
  if (JSON.stringify(skills) !== JSON.stringify(CANONICAL_SKILLS)) {
    problems.push(`package skills must equal the canonical six: ${CANONICAL_SKILLS.join(", ")}`);
  }
  if (JSON.stringify([...rows.keys()]) !== JSON.stringify(CANONICAL_SKILLS)) {
    problems.push("distribution rows must equal the canonical six in order");
  }
  for (const id of EXTERNAL_NOT_DISTRIBUTED) {
    if (skills.includes(id)) problems.push(`external skill must not be packaged: ${id}`);
    if (rows.has(id)) problems.push(`external skill must not have a distribution row: ${id}`);
  }
  const retired = retiredRows(markdown);
  for (const id of RETIRED) {
    if (skills.includes(id)) problems.push(`retired skill regrew in the package: ${id}`);
    if (!retired.has(id)) problems.push(`retired identifier is missing from the guard table: ${id}`);
  }
  for (const id of NON_SKILL_REGISTERS) {
    if (skills.includes(id)) problems.push(`non-skill register was packaged: ${id}`);
    const register = section(markdown, `## Register owner: \`${id}\``);
    if (!register.includes("relay/convergence/")) {
      problems.push(`non-skill register lacks its Relay convergence owner: ${id}`);
    }
  }
  return { ok: problems.length === 0, problems, published: skills.length, rows: rows.size };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const result = check();
  if (!result.ok) {
    for (const problem of result.problems) process.stderr.write(`standing-distribution: ${problem}\n`);
    process.exit(1);
  }
  process.stdout.write(`standing-distribution: OK (${result.published} canonical skills, ${result.rows} distribution rows)\n`);
}
