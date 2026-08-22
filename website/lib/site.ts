const owner = process.env.NEXT_PUBLIC_GITHUB_OWNER ?? "DinoDevCli";
const repo = process.env.NEXT_PUBLIC_GITHUB_REPO ?? "dino";

const base = `https://github.com/${owner}/${repo}`;
const blob = (path: string) => `${base}/blob/main/${path}`;

export const GITHUB = {
  owner,
  repo,
  base,
  readme: `${base}#installation`,
  /** Works as soon as main is pushed; replace with /releases/latest after first GitHub Release. */
  downloadZip: `${base}/archive/refs/heads/main.zip`,
  releases: `${base}/releases/latest`,
  issuesNew: `${base}/issues/new`,
  teamIssue: `${base}/issues/new?title=Team%20Pack%20Anfrage&labels=sales`,
  docs: {
    proofContract: blob("docs/PROOF_CONTRACT.md"),
    cliReference: blob("docs/CLI_E2E_REFERENCE.md"),
    examples: blob("docs/EXAMPLES.md"),
    techStatus: blob("docs/TECH_STATUS_NOW.md"),
    readme: blob("README.md"),
  },
  contactEmail: process.env.NEXT_PUBLIC_CONTACT_EMAIL ?? "",
};

export function contactHref(): string {
  if (GITHUB.contactEmail) {
    return `mailto:${GITHUB.contactEmail}?subject=Dino%20Team%20Pack`;
  }
  return GITHUB.teamIssue;
}
