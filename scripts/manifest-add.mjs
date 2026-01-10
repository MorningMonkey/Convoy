import fs from "node:fs";

const manifestPath = "projects/manifest.json";

function requiredEnv(name) {
  const v = process.env[name];
  if (!v || !v.trim()) throw new Error(`Missing env: ${name}`);
  return v.trim();
}

const name = requiredEnv("NAME");
const repo = requiredEnv("REPO");
const branch = (process.env.BRANCH ?? "main").trim();
const onDirty = (process.env.ONDlRTY ?? process.env.ONDIRTY ?? "abort").trim(); // typo-safe
const allowDuplicate = (process.env.ALLOW_DUPLICATE ?? "false").trim().toLowerCase() === "true";

const raw = fs.readFileSync(manifestPath, "utf8");
const manifest = JSON.parse(raw);

if (!manifest.rootDir) throw new Error("manifest.rootDir is missing");
if (!Array.isArray(manifest.projects)) manifest.projects = [];

const existingIndex = manifest.projects.findIndex((p) => p?.name === name);

if (existingIndex !== -1 && !allowDuplicate) {
  console.log(`Already exists: ${name} (no changes)`);
  process.exit(0);
}

const entry = { name, repo, branch, onDirty };

if (existingIndex !== -1) {
  // allowDuplicate=true の場合でも、実務上は上書き更新が安全
  manifest.projects[existingIndex] = entry;
  console.log(`Updated: ${name}`);
} else {
  manifest.projects.push(entry);
  console.log(`Added: ${name}`);
}

// sort for stable diffs
manifest.projects.sort((a, b) => String(a.name).localeCompare(String(b.name)));

fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n");
