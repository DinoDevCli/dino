# Website

Landing page for Dino — notarization/seal visual language, Free vs Proof Pack aligned with the root README.

**CTAs:** mailto `dinodevcli@gmail.com` or GitHub Early Access — never `dino.dev`.

## Local

```bash
npm install
npm run dev
```

→ http://localhost:3000

With Pages base path locally:

```bash
NEXT_PUBLIC_BASE_PATH=/dino npm run build && npx serve out
```

## Env

```
NEXT_PUBLIC_GITHUB_OWNER=DinoDevCli
NEXT_PUBLIC_GITHUB_REPO=dino
NEXT_PUBLIC_CONTACT_EMAIL=dinodevcli@gmail.com
```

## Deploy

Push to `main` → [Deploy website](../../.github/workflows/deploy-website.yml) →  
**https://dinodevcli.github.io/dino/**

## Assets

- Hero demo is static CLI shots (`components/CliShots.tsx`, golden excerpts) — no GIF / typing loop
- `public/assets/cli-compare.png` — optional static compare capture (also in `docs/assets/`)
- `public/favicon.svg` — lettermark D
