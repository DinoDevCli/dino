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

## Deploy (Vercel)

- Root: `website`
- Framework: Next.js (static export)
- Env as above

## Copy

| File | Role |
|------|------|
| `lib/content.ts` | Copy, modules, pricing, FAQ |
| `lib/site.ts` | GitHub URLs, CTAs |
