const owner = process.env.NEXT_PUBLIC_GITHUB_OWNER ?? "DinoDevCli";
const repo = process.env.NEXT_PUBLIC_GITHUB_REPO ?? "dino";

const base = `https://github.com/${owner}/${repo}`;
const blob = (path: string) => `${base}/blob/main/${path}`;

/** Interim contact — override via NEXT_PUBLIC_CONTACT_EMAIL */
const DEFAULT_CONTACT = "noahpeitz95@gmail.com";

export const GITHUB = {
  owner,
  repo,
  base,
  readme: `${base}#install`,
  /** Works as soon as main is pushed; replace with /releases/latest after first GitHub Release. */
  downloadZip: `${base}/archive/refs/heads/main.zip`,
  releases: `${base}/releases/latest`,
  issuesNew: `${base}/issues/new`,
  teamIssue: `${base}/issues/new?title=Team%20Pack%20Inquiry&labels=sales`,
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

export function contactHref(subject = "Dino — Team / Large Teams"): string {
  const email = GITHUB.contactEmail;
  return `mailto:${email}?subject=${encodeURIComponent(subject)}`;
}
