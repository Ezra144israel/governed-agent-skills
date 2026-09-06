#!/usr/bin/env node
// Source-side package check. Current identity is owned by current-skills.json.
import { existsSync, readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CONTRACT = join(ROOT, "STANDING-SOURCE-AND-ADAPTER-CONTRACT.md");
const SKILLS = join(ROOT, "skills");
const CURRENT = JSON.parse(readFileSync(join(ROOT, "current-skills.json"), "utf8"));
const OWNER = "Ezra144israel/governed-agent-skills";

export const NON_SKILL_REGISTERS = Object.freeze(["pending-convergence"]);
export const CANONICAL_SKILLS = Object.freeze(CURRENT.skills
  .filter((row) => row.lifecycle === "CURRENT" && row.source.repository === OWNER)
  .map((row) => row.name));
export const RETIRED = Object.freeze(CURRENT.skills
  .filter((row) => row.lifecycle === "RETIRED" && !NON_SKILL_REGISTERS.includes(row.name))
  .map((row) => row.name));

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

export function check({ skills = publishedSkills(), markdown = readFileSync(CONTRACT, "utf8"), manifest = CURRENT, requireCurrent = false } = {}) {
  const rows = contractRows(markdown);
  const problems = [];
  if (JSON.stringify(skills) !== JSON.stringify(CANONICAL_SKILLS)) {
    problems.push(`package skills must equal the canonical manifest: ${CANONICAL_SKILLS.join(", ")}`);
  }
  if (JSON.stringify([...rows.keys()]) !== JSON.stringify(CANONICAL_SKILLS)) {
    problems.push("distribution rows must equal the canonical manifest in order");
  }
  if (manifest.schema !== "canonical-current-skills/v1") problems.push("invalid current manifest schema");
  if (!["CANDIDATE", "CURRENT"].includes(manifest.status)) problems.push("invalid manifest status");
  if (requireCurrent && manifest.status !== "CURRENT") problems.push("manifest is not a current release");
  const names = manifest.skills.map((row) => row.name);
  if (new Set(names).size !== names.length) problems.push("duplicate current identity in canonical manifest");
  for (const row of manifest.skills) {
    if (row.lifecycle !== "CURRENT" || row.source?.repository !== OWNER) continue;
    if (row.source.path !== `skills/${row.name}`) {
      problems.push(`unexpected canonical source path: ${row.name}`);
      continue;
    }
    for (const member of row.source.members) {
      if (!member.path || member.path.startsWith("/") || member.path.split("/").some((part) => !part || part === "." || part === ".." || part === ".git")) {
        problems.push(`invalid canonical member path: ${row.name}`);
        continue;
      }
      const file = join(ROOT, row.source.path, member.path);
      if (!existsSync(file)) { problems.push(`canonical member missing: ${row.name}/${member.path}`); continue; }
      const bytes = readFileSync(file);
      if (bytes.length !== member.bytes || createHash("sha256").update(bytes).digest("hex") !== member.sha256) {
        problems.push(`canonical member identity mismatch: ${row.name}/${member.path}`);
      }
    }
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
  if (process.argv.slice(2).some((arg) => arg !== "--require-current")) {
    process.stderr.write("standing-distribution: unknown argument\n");
    process.exit(2);
  }
  const result = check({ requireCurrent: process.argv.includes("--require-current") });
  if (!result.ok) {
    for (const problem of result.problems) process.stderr.write(`standing-distribution: ${problem}\n`);
    process.exit(1);
  }
  process.stdout.write(`standing-distribution: OK (${result.published} canonical skills, ${result.rows} distribution rows)\n`);
}
