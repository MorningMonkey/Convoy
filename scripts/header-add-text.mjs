import fs from "node:fs";
import sharp from "sharp";

function getArg(name, fallback = null) {
    const idx = process.argv.indexOf(name);
    if (idx === -1) return fallback;
    return process.argv[idx + 1] ?? fallback;
}

function escapeXml(s) {
    return String(s)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&apos;");
}

const inputPath = getArg("--in", "assets/header_cropped.png");
const outputPath = getArg("--out", "assets/header_cropped_text.png");
const titleText = escapeXml(getArg("--title", "Convoy"));
const subtitleText = escapeXml(getArg("--subtitle", "Mission Control workspace for agentic development"));

// Colors
const goldHex = "#E6D285";

async function main() {
    if (!fs.existsSync(inputPath)) {
        console.error("Input not found:", inputPath);
        process.exit(1);
    }

    const meta = await sharp(inputPath).metadata();
    const width = meta.width ?? 1600;
    const height = meta.height ?? 420;

    // Safe sizing (banner前提)
    const safePadX = Math.floor(width * 0.08);
    const safePadY = Math.floor(height * 0.12);

    const titleFontSize = Math.floor(height * 0.28);
    const subFontSize = Math.floor(titleFontSize * 0.42);
    const gap = Math.floor(height * 0.08);

    const titleY = safePadY + Math.floor((height - safePadY * 2) * 0.38);
    const subY = titleY + Math.floor(titleFontSize * 0.8) + gap;

    const svg = `
  <svg width="${width}" height="${height}">
    <defs>
      <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
        <feDropShadow dx="3" dy="3" stdDeviation="2" flood-color="black" flood-opacity="0.8"/>
      </filter>
    </defs>
    <style>
      .title { fill: ${goldHex}; font-size: ${titleFontSize}px; font-weight: 700;
        font-family: "Yu Mincho", Georgia, serif; text-anchor: middle; dominant-baseline: central; filter: url(#shadow); }
      .subtitle { fill: ${goldHex}; font-size: ${subFontSize}px; font-weight: 400;
        font-family: "Yu Gothic", "Segoe UI", sans-serif; text-anchor: middle; dominant-baseline: central; filter: url(#shadow); }
    </style>

    <text x="50%" y="${titleY}" class="title">${titleText}</text>
    <text x="50%" y="${subY}" class="subtitle">${subtitleText}</text>
  </svg>`;

    await sharp(inputPath)
        .composite([{ input: Buffer.from(svg), top: 0, left: 0 }])
        .toFile(outputPath);

    console.log(`OK: ${outputPath}`);
}

main().catch((e) => {
    console.error("FAILED:", e?.message ?? e);
    process.exit(1);
});
