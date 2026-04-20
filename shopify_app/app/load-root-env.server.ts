import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { config as loadDotenv } from "dotenv";

let dir = path.dirname(fileURLToPath(import.meta.url));
for (let i = 0; i < 12; i++) {
  const envPath = path.join(dir, ".env");
  const managePy = path.join(dir, "manage.py");
  if (fs.existsSync(managePy) && fs.existsSync(envPath)) {
    loadDotenv({ path: envPath });
    break;
  }
  const parent = path.dirname(dir);
  if (parent === dir) break;
  dir = parent;
}
