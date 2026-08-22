# Publish to GitHub

## 1. Authenticate

```bash
gh auth login
```

## 2. Create repo and push

From `devsecops/` (project root):

```bash
git remote add origin https://github.com/noahp/dino.git   # or gh repo create
git push -u origin main
```

If the repo does not exist yet:

```bash
gh repo create dino --public --source=. --remote=origin --push
```

Update `website/.env.local` (or Vercel env) with your GitHub owner/repo:

```
NEXT_PUBLIC_GITHUB_OWNER=your-username
NEXT_PUBLIC_GITHUB_REPO=dino
```

## 3. Vercel (optional)

- Import GitHub repo
- Root directory: `website`
- Framework: Next.js

Buttons on the landing page link to GitHub releases, docs, and issues.
