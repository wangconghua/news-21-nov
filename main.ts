// Entry point for the news-image-20261121 bounty (Node 22, standard library
// only). The rendered infographic lives next to this file as entry.png; this
// program places a copy of it at /output/entry.png, or at the directory named
// by MAKEFUN_OUTPUT_DIR when that is set, for local runs:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(targetDir, { recursive: true });
writeFileSync(
  join(targetDir, "entry.png"),
  readFileSync(join(here, "entry.png")),
);
