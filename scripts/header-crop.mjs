import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";

function getArg(name, fallback = null) {
  const idx = process.argv.indexOf(name);
  if (idx === -1) return fallback;
  const v = process.argv[idx + 1];
  return v ?? fallback;
}

const inputPath = getArg("--in", "assets/header.png");
const outputPath = getArg("--out", "assets/header_cropped.png");
const w = Number(getArg("--w", "1600"));
const h = Number(getArg("--h", "420"));

if (!Number.isFinite(w) || !Number.isFinite(h) || w <= 0 || h <= 0) {
  console.error(`[header-crop] invalid size: w=${w} h=${h}`);
  process.exit(1);
}

if (!fs.existsSync(inputPath)) {
  console.error(`[header-crop] input not found: ${inputPath}`);
  process.exit(1);
}

fs.mkdirSync(path.dirname(outputPath), { recursive: true });

const ext = path.extname(outputPath).toLowerCase();
const format =
  ext === ".jpg" || ext === ".jpeg" ? "jpeg" :
  ext === ".webp" ? "webp" :
  "png"; // default

try {
  const pipeline = sharp(inputPath).resize(w, h, { fit: "cover", position: "centre" });

  if (format === "jpeg") {
    await pipeline.jpeg({ quality: 90, mozjpeg: true }).toFile(outputPath);
  } else if (format === "webp") {
    await pipeline.webp({ quality: 90 }).toFile(outputPath);
  } else {
    await pipeline.png({ compressionLevel: 9 }).toFile(outputPath);
  }

  console.log(`[header-crop] OK: ${outputPath} (${w}x${h})`);
} catch (e) {
  console.error("[header-crop] FAILED:", e?.message ?? e);
  process.exit(1);
}
