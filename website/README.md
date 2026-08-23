# Website

Landing page for Dino — aligned with the root [README](../README.md).

## Local

```bash
cp .env.example .env.local
npm install
npm run dev
```

→ http://localhost:3000

## Env

```
NEXT_PUBLIC_GITHUB_OWNER=DinoDevCli
NEXT_PUBLIC_GITHUB_REPO=dino
```

Optional: `NEXT_PUBLIC_CONTACT_EMAIL` (default `noahpeitz95@gmail.com`).

## Deploy

### Live (GitHub Pages)

Push to `main` → [Deploy website](../../.github/workflows/deploy-website.yml) →  
**https://dindevcli.github.io/dino/**

Uses `NEXT_PUBLIC_BASE_PATH=/dino` in CI only.

### Vercel (optional custom domain)

- Import `DinoDevCli/dino`, root directory **`website`**
- Env: `NEXT_PUBLIC_GITHUB_*`, optional Lemon checkout URLs (no `BASE_PATH`)
- `vercel login && cd website && npx vercel --prod`

## Copy

| File | Role |
|------|------|
| `lib/content.ts` | Copy, modules, pricing, FAQ |
| `lib/site.ts` | GitHub URLs, CTAs |
