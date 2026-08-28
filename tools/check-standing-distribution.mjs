#!/usr/bin/env node
// Proves the standing source/adapter contract against the actual package.
//
// Two failures this exists to catch, both observed in the 2026-08 audit:
//   1. a retired skill regrowing through a normal install or update;
//   2. a published skill with no row in the contract, so a byte difference on a
//      surface cannot be classified as adapter or drift.
//
// Exit 0 green, 1 red. No network, no dependencies.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CONTRACT = join(ROOT, "STANDING-SOURCE-AND-ADAPTER-CONTRACT.md");
const SKILLS = join(ROOT, "skills");

/** Retired by closed pruning manifest v2 and the builder-quality-system errata. */
export const RETIRED = Object.freeze([
  "portable-adaptive-planning",
  "write-maintainable-code",
  "run-review-repair-loop",
  "scouted-rules",
  "orchestrator-seat",
  "builder-return",
  "reviewer-validation",
  // Owned solely by Substrate-8/team-hub-operator-web per the standing source
  // ownership decision. It must not regrow as a generic standing duplicate.
  "test-verification",
  // Not a skill at all: a register migrated to a non-skill Relay convergence
  // record. It must never be recreated here as SKILL.md by sync or packaging.
  "pending-convergence",
]);

/**
 * Ids that are not skills at all. They must never be published here and must
 * never appear inside a section that assigns a skill source home, because an
 * owner statement is what a later sync or packaging step reads as licence to
 * create a `SKILL.md`.
 */
export const NON_SKILL_REGISTERS = Object.freeze(["pending-convergence"]);

/** Headings whose bodies assign a skill source home. */
const SKILL_OWNER_HEADINGS = ["## Distribution table", "## Ownership boundary with"];

function sectionsStartingWith(markdown, prefixes) {
  const found = [];
  const lines = markdown.split("\n");
  for (let index = 0; index < lines.length; index += 1) {
    if (!prefixes.some((prefix) => lines[index].startsWith(prefix))) continue;
    const body = [lines[index]];
    for (let cursor = index + 1; cursor < lines.length && !lines[cursor].startsWith("## "); cursor += 1) {
      body.push(lines[cursor]);
    }
    found.push({ heading: lines[index], text: body.join("\n") });
  }
  return found;
}

/** Sections that assign a skill source home, keyed by heading. */
export function skillOwnerSections(markdown = readFileSync(CONTRACT, "utf8")) {
  return sectionsStartingWith(markdown, SKILL_OWNER_HEADINGS);
}

/** The non-skill register owner statements, keyed by register id. */
export function registerOwnerStatements(markdown = readFileSync(CONTRACT, "utf8")) {
  const statements = new Map();
  for (const section of sectionsStartingWith(markdown, ["## Register owner:"])) {
    for (const id of NON_SKILL_REGISTERS) {
      if (section.heading.includes(`\`${id}\``)) statements.set(id, section.text);
    }
  }
  return statements;
}

export function publishedSkills(skillsDir = SKILLS) {
  return readdirSync(skillsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && existsSync(join(skillsDir, entry.name, "SKILL.md")))
    .map((entry) => entry.name)
    .sort();
}

/** Rows of the contract's distribution table, keyed by skill id. */
export function contractRows(markdown = readFileSync(CONTRACT, "utf8")) {
  const rows = new Map();
  for (const line of markdown.split("\n")) {
    const match = /^\|\s*`([a-z0-9-]+)`[^|]*\|\s*([^|]+?)\s*\|/.exec(line);
    if (match) rows.set(match[1], match[2].trim());
  }
  return rows;
}

/** Skills the contract lists in its retired table. */
export function retiredRows(markdown = readFileSync(CONTRACT, "utf8")) {
  const start = markdown.indexOf("## Retired: must not regrow");
  if (start === -1) return new Set();
  const end = markdown.indexOf("\n## ", start + 1);
  const block = markdown.slice(start, end === -1 ? undefined : end);
  return new Set([...block.matchAll(/^\|\s*`([a-z0-9-]+)`/gm)].map((m) => m[1]));
}

export function check({ skills = publishedSkills(), markdown = readFileSync(CONTRACT, "utf8") } = {}) {
  const rows = contractRows(markdown);
  const retiredListed = retiredRows(markdown);
  const problems = [];

  for (const skill of skills) {
    if (RETIRED.includes(skill)) problems.push(`skill that must not be published regrew in the package: ${skill}`);
    if (!rows.has(skill)) problems.push(`published skill has no distribution row: ${skill}`);
  }
  for (const id of rows.keys()) {
    if (!skills.includes(id) && !RETIRED.includes(id)) {
      problems.push(`distribution row names a skill this package does not publish: ${id}`);
    }
  }
  for (const id of NON_SKILL_REGISTERS) {
    for (const section of skillOwnerSections(markdown)) {
      if (section.text.includes(id)) {
        problems.push(`non-skill register named in a skill-source owner statement (${section.heading.trim()}): ${id}`);
      }
    }
    const statement = registerOwnerStatements(markdown).get(id);
    if (!statement) {
      problems.push(`non-skill register has no register-owner statement: ${id}`);
    } else if (!statement.includes("relay/convergence/")) {
      problems.push(`register-owner statement does not name the Relay convergence owner: ${id}`);
    }
  }
  for (const id of RETIRED) {
    if (!retiredListed.has(id) && ["portable-adaptive-planning", "write-maintainable-code", "run-review-repair-loop", "scouted-rules", "test-verification", "pending-convergence"].includes(id)) {
      problems.push(`retired skill is not recorded in the must-not-regrow table: ${id}`);
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
  process.stdout.write(`standing-distribution: OK (${result.published} published, ${result.rows} rows, ${RETIRED.length} retired guarded)\n`);
}
