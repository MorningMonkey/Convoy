import fs from "node:fs/promises";
import path from "node:path";
import { parseArgs } from "node:util";

const options = {
  page: { type: "string" }, // Figma page name
  url: { type: "string" },  // Figma URL
  out: { type: "string" },  // output file path (optional)
  "no-save": { type: "boolean", default: false }, // do not write prompt file
  "no-run": { type: "boolean", default: false },  // do not create runs folder/review.md
  base: { type: "string", default: "ui-lab/prompts/mcp_base_prompt.md" },
  specsDir: { type: "string", default: "ui-lab/specs" },
  rubric: { type: "string", default: "ui-lab/rubrics/ux_header_scorecard.md" },
  gates: { type: "string", default: "ui-lab/rubrics/smoke_test_header_gates.md" },
};

function today() {
  return new Date().toISOString().slice(0, 10);
}

function nowIso() {
  return new Date().toISOString();
}

function abs(p) {
  return path.isAbsolute(p) ? p : path.join(process.cwd(), p);
}

async function readText(filePath) {
  return await fs.readFile(filePath, "utf8");
}

async function readJson(filePath) {
  const raw = await fs.readFile(filePath, "utf8");
  return JSON.parse(raw);
}

function buildImplementationBlock(spec) {
  const component = spec.component ?? "Component";
  const heightPx = spec.layout?.heightPx ?? 56;
  const padX = spec.layout?.paddingX ?? 16;
  const tapMin = spec.interaction?.tapMinHeightPx ?? 44;

  const ariaLabels = spec.a11y?.ariaLabels ?? {};
  const ariaLines = Object.entries(ariaLabels)
    .map(([k, v]) => `     - ${k}: "${v}"`)
    .join("\n");

  return [
    "---",
    "UI SPEC (JSON, must be respected)",
    "",
    "Attach the following JSON verbatim:",
    "```json",
    JSON.stringify(spec, null, 2),
    "```",
    "",
    "---",
    "Implementation requirements (additional)",
    "",
    `A) Produce a single file: \`${component}.tsx\``,
    `B) Implement as a reusable component: \`${component}\``,
    "C) Props (TypeScript interface):",
    `   - title?: string (default "Convoy")`,
    `   - workspaceName?: string (default "Workspace")`,
    `   - canNavigateBack?: boolean (default false)`,
    `   - isLoading?: boolean (default false)`,
    `   - isOffline?: boolean (default false)`,
    `   - onBack?: () => void`,
    `   - onOpenCommand?: () => void`,
    `   - onOpenSettings?: () => void`,
    "",
    "D) Rendering logic:",
    `   - Derive workspace label: if isLoading => "Loading…", else if isOffline => "Offline" (+ status dot), else => workspaceName`,
    "   - Disable actions when isLoading is true",
    "   - Command button must be desktop only (hidden on small screens)",
    "",
    "E) Styling constraints:",
    "   - Tailwind utility classes only (no CSS files)",
    "   - Flex layout for left / center / right",
    `   - Header height: ${heightPx}px, horizontal padding: ${padX}px`,
    `   - Minimum interactive height: ${tapMin}px`,
    "   - Do NOT use absolute positioning for the main header layout",
    "",
    "F) Accessibility:",
    "   - Use <button> for actions",
    "   - Add focus-visible styles (ring) and keyboard accessibility",
    ariaLines ? `   - aria-labels:\n${ariaLines}` : "   - aria-labels: (use the spec values)",
    "",
  ].join("\n");
}

function buildReviewTemplate({
  productId,
  specId,
  pageName,
  figmaUrl,
  specPath,
  basePath,
  rubricPath,
  gatesPath,
  runDir,
  promptOutPath,
  noSave,
}) {
  const safePage = pageName ?? "[PAGE_NAME]";
  const safeUrl = figmaUrl ?? "[FIGMA_URL]";
  const promptPathLine = noSave
    ? "- Prompt file: (not saved; use terminal output or clipboard)"
    : `- Prompt file: ${promptOutPath}`;

  return `# Review: ${productId}/${specId}

- Generated at: ${nowIso()}
- Figma page: ${safePage}
- Figma URL: ${safeUrl}
- Run dir: ${runDir}
${promptPathLine}
- Spec: ${specPath}
- Base prompt: ${basePath}
- UX rubric: ${rubricPath}
- Smoke gates: ${gatesPath}

## 1) Smoke Test Gates (PASS/FAIL)
(Complete these first. Any Critical fail => reject output.)

> Copy the gates content below and check off items:

(Embedded)
--- 
${"".trim()}

## 2) UX Psychology Score (0/1/2 each)
Pass guideline: Total >= 16/20 and no critical NG.

| Item | Score (0/1/2) | Notes |
|---|---:|---|
| 1) Information hierarchy |  |  |
| 2) Cognitive load |  |  |
| 3) Affordance & recognition |  |  |
| 4) Fitts’ Law |  |  |
| 5) Consistency |  |  |
| 6) Feedback & system status |  |  |
| 7) Error prevention & recovery |  |  |
| 8) Grouping & scanning |  |  |
| 9) Accessibility |  |  |
| 10) Minimalism |  |  |

**Total:** / 20

## 3) Findings
- What passed:
- What failed:
- Key risks:

## 4) Fix Plan (next prompt iteration)
- Prompt changes:
- Figma changes (Auto Layout / Variables / naming):
- Component changes:

## 5) Decision
- [ ] Accept
- [ ] Revise and rerun
`;
}

async function main() {
  const { values, positionals } = parseArgs({
    options,
    allowPositionals: true,
    strict: false,
  });

  const productId = positionals?.[0];
  const specId = positionals?.[1];

  if (!productId || !specId) {
    console.error("Usage: pnpm ui:prompt <productId> <specId> [--page \"...\"] [--url \"...\"] [--out path] [--no-save] [--no-run]");
    console.error("Example: pnpm ui:prompt convoy ui-header --page \"Convoy UI\" --url \"https://www.figma.com/...\"");
    process.exit(1);
  }

  const specsDir = abs(values.specsDir);
  const specPath = path.join(specsDir, productId, `${specId}.json`);
  const basePath = abs(values.base);
  const rubricPath = abs(values.rubric);
  const gatesPath = abs(values.gates);

  const runDir = path.join(process.cwd(), "ui-lab", "runs", `${today()}_${productId}_${specId}`);

  // Default output location (when saving)
  const defaultOut = path.join(runDir, "mcp_prompt.md");
  const outPath = abs(values.out ?? defaultOut);

  const [basePromptRaw, spec, rubricRaw, gatesRaw] = await Promise.all([
    readText(basePath),
    readJson(specPath),
    readText(rubricPath),
    readText(gatesPath),
  ]);

  let prompt = basePromptRaw;

  // Replace placeholders if provided; otherwise keep placeholders as-is.
  if (values.page) prompt = prompt.replaceAll("[PAGE_NAME]", values.page);
  if (values.url) prompt = prompt.replaceAll("[FIGMA_URL]", values.url);

  const impl = buildImplementationBlock(spec);

  const finalPrompt =
    `${prompt.trim()}\n\n${impl}\n\n---\n` +
    `UX PSYCHOLOGY SCORECARD (use this as acceptance criteria)\n\n` +
    `${rubricRaw.trim()}\n`;

  // Always output to STDOUT for copy/paste
  console.log(finalPrompt);

  if (!values["no-run"]) {
    // Ensure run directory exists
    await fs.mkdir(runDir, { recursive: true });

    // Save prompt if enabled
    if (!values["no-save"]) {
      await fs.writeFile(outPath, finalPrompt, "utf8");
      console.error(`\n[Saved] ${outPath}`);
    }

    // Always generate review.md (strong standard)
    const reviewPath = path.join(runDir, "review.md");
    const review = buildReviewTemplate({
      productId,
      specId,
      pageName: values.page,
      figmaUrl: values.url,
      specPath,
      basePath,
      rubricPath,
      gatesPath,
      runDir,
      promptOutPath: outPath,
      noSave: values["no-save"],
    });

    // Embed gates inside review (so reviewers don't have to open another file)
    const reviewWithGates = review.replace(
      "(Embedded)\n--- \n",
      `### Gates (embedded)\n\n${gatesRaw.trim()}\n\n---\n`
    );

    await fs.writeFile(reviewPath, reviewWithGates, "utf8");
    console.error(`[Saved] ${reviewPath}`);
  }
}

main().catch((e) => {
  const msg = e?.message ?? String(e);
  if (msg.includes("ENOENT")) {
    console.error("Error: required file not found. Check spec/base/rubric/gates paths.");
  }
  console.error("Error:", msg);
  process.exit(1);
});