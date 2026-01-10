import fs from "node:fs";
import Ajv from "ajv";

const manifestPath = "projects/manifest.json";
const schemaPath = "projects/manifest.schema.json";

const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));

const ajv = new Ajv({ allErrors: true });
const validate = ajv.compile(schema);

if (!validate(manifest)) {
  console.error("manifest.json validation failed:");
  console.error(validate.errors);
  process.exit(1);
}

console.log("manifest.json OK");
