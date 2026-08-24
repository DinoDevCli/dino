const owner = process.env.NEXT_PUBLIC_GITHUB_OWNER ?? "DinoDevCli";
const repo = process.env.NEXT_PUBLIC_GITHUB_REPO ?? "dino";

const base = `https://github.com/${owner}/${repo}`;
const blob = (path: string) => `${base}/blob/main/${path}`;

/** Public contact — Early Access (same as website mailto) */
const DEFAULT_CONTACT = "dinodevcli@gmail.com";

export const GITHUB = {
  owner,
  repo,
  base,
  readme: `${base}#install`,
  downloadZip: `${base}/archive/refs/heads/main.zip`,
  releases: `${base}/releases/latest`,
  earlyAccessIssue: `${base}/issues/new?title=${encodeURIComponent("Early Access Request")}`,
  issues: `${base}/issues`,
  issuesNew: `${base}/issues/new`,
  discussions: `${base}/discussions`,
  codespaces: `https://codespaces.new/${owner}/${repo}`,
  docsIndex: blob("docs/index.md"),
  docs: {
    proofContract: blob("docs/PROOF_CONTRACT.md"),
    cliReference: blob("docs/CLI_E2E_REFERENCE.md"),
    examples: blob("docs/EXAMPLES.md"),
    techStatus: blob("docs/TECH_STATUS_NOW.md"),
    readme: blob("README.md"),
  },
  contactEmail:
    process.env.NEXT_PUBLIC_CONTACT_EMAIL?.trim() || DEFAULT_CONTACT,
};

export const EARLY_ACCESS_EMAIL = "dinodevcli@gmail.com";

/** Base path for GitHub Pages (`/dino` in CI, empty locally). */
export function siteBasePath(): string {
  return process.env.NEXT_PUBLIC_BASE_PATH?.replace(/\/$/, "") ?? "";
}

/** Same-page section jump that works with static export + basePath. */
export function siteHash(id: string): string {
  const hash = id.replace(/^#/, "");
  return `${siteBasePath()}/#${hash}`;
}

export function earlyAccessMailto(): string {
  const subject = encodeURIComponent("Early Access Request");
  const body = encodeURIComponent("Team name:\n");
  return `mailto:${EARLY_ACCESS_EMAIL}?subject=${subject}&body=${body}`;
}

export function contactHref(subject = "Dino — contact"): string {
  const email = GITHUB.contactEmail;
  return `mailto:${email}?subject=${encodeURIComponent(subject)}`;
}
