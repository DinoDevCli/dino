# Website

Landing Page für Dino — schlicht, technisch, aligned mit dem CLI und dem [README](../README.md).

## Lokal

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

Optional: `NEXT_PUBLIC_CONTACT_EMAIL` für Team/Contact (sonst GitHub Issues).

## Deploy (Vercel)

- Root: `website`
- Framework: Next.js (static export)
- Env wie oben

## Copy

| Datei | Inhalt |
|-------|--------|
| `lib/content.ts` | Texte, Module, Pricing, FAQ |
| `lib/site.ts` | GitHub-URLs, CTAs |
