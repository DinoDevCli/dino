# Website

Documentary landing page for Dino — aligned with the root [README](../README.md).

**Story:** local-first audit engine · Free scan forever · Proof pack via Early Access ·  
`early@dinodevcli.dev` · no checkout · dashboards external.

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
NEXT_PUBLIC_CONTACT_EMAIL=early@dinodevcli.dev
```

## Deploy

Push to `main` → [Deploy website](../../.github/workflows/deploy-website.yml) →  
**https://dinodevcli.github.io/dino/**

Uses `NEXT_PUBLIC_BASE_PATH=/dino` in CI only.

## Copy

| File | Role |
|------|------|
| `lib/content.ts` | Documentary copy + Early Access |
| `lib/site.ts` | GitHub URLs, `early@dinodevcli.dev` mailto |
