# Publish to GitHub

Organisation: **[DinoDevCli](https://github.com/DinoDevCli)** · Repo: **`dino`**

## 1. Authenticate (once)

```bash
gh auth login
```

## 2. Create repo and push

From project root (`devsecops/`):

```bash
gh repo create DinoDevCli/dino --public --source=. --remote=origin --push
```

If the repo already exists:

```bash
git remote add origin https://github.com/DinoDevCli/dino.git
git push -u origin main
```

## 3. Website env (Vercel / local)

```
NEXT_PUBLIC_GITHUB_OWNER=DinoDevCli
NEXT_PUBLIC_GITHUB_REPO=dino
```

Copy `website/.env.example` → `website/.env.local` for local dev.

## 4. Vercel

- Import `DinoDevCli/dino`
- Root directory: `website`
- Set env vars above

Landing-page buttons link to `github.com/DinoDevCli/dino` (releases, docs, issues).
