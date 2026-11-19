# Jezneel birthday — exact preview edition

This version deliberately serves the original, browser-tested illustrated birthday experience. The entry point `index.html`, the standalone `preview.html`, and the generated `dist/index.html` are byte-identical. There are no external runtime dependencies. The optional Three.js implementation is in `optional-threejs/` and not imported by the default website. Its visuals differ and its WebGL path has not been verified.

## Run locally

Open `index.html` directly, or with Node 18+ run `npm run dev` and visit http://localhost:5173. No npm install is necessary locally. `npm run build` copies the validated entry point into `dist/index.html`; `npm run preview` serves the production output.

## Vercel

Import this folder/repository using Vercel with Framework Preset Other, Root Directory `./` (the directory containing this README and package.json), Build Command `npm run build`, Output Directory `dist`. The included vercel.json sets these automatically. No environment variables are required. If updating an old deployment, replace the previous source (do not merge with it), verify the Vercel project root is correct, and redeploy without the old build cache. CLI alternative: `npx vercel --prod` from this folder.

## Optional Three.js

To experiment with the visually distinct Three.js edition, separately enter `optional-threejs`, run `npm install` and `npm run dev`. Do not set this folder as Vercel's root if you want the exact illustrated preview. The original README in that folder describes the earlier project, not the default entry point.

## Verification of this package

`npm run build` passed. Original preview, root index, local preview and dist index have identical SHA-256 hashes. The local HTTP response also matched. Chromium blocked direct localhost navigation (administrator policy), so the production file contents were loaded directly into Chromium at a 390 × 844 touch-enabled viewport. The full gesture walkthrough passed, including the letter, replay and no page errors. This is not a test of a live Vercel deployment or a physical device. See `verification/production-browser-test.log`.
