const owner = process.env.NEXT_PUBLIC_GITHUB_OWNER ?? "DinoDevCli";
const repo = process.env.NEXT_PUBLIC_GITHUB_REPO ?? "dino";

const base = `https://github.com/${owner}/${repo}`;
const blob = (path: string) => `${base}/blob/main/${path}`;

/** Interim contact — override via NEXT_PUBLIC_CONTACT_EMAIL */
const DEFAULT_CONTACT = "noahpeitz95@gmail.com";

function envUrl(name: string): string {
  const raw = process.env[name]?.trim() ?? "";
  if (!raw) return "";
  try {
    const u = new URL(raw);
    if (u.protocol !== "https:") return "";
    return u.toString();
  } catch {
    return "";
  }
}

export const GITHUB = {
  owner,
  repo,
  base,
  readme: `${base}#install`,
  downloadZip: `${base}/archive/refs/heads/main.zip`,
  releases: `${base}/releases/latest`,
  issuesNew: `${base}/issues/new`,
  teamIssue: `${base}/issues/new?title=Team%20Pack%20Inquiry&labels=sales`,
  docs: {
    proofContract: blob("docs/PROOF_CONTRACT.md"),
    cliReference: blob("docs/CLI_E2E_REFERENCE.md"),
    examples: blob("docs/EXAMPLES.md"),
    techStatus: blob("docs/TECH_STATUS_NOW.md"),
    lemon: blob("docs/LEMON_SQUEEZY.md"),
    readme: blob("README.md"),
  },
  contactEmail:
    process.env.NEXT_PUBLIC_CONTACT_EMAIL?.trim() || DEFAULT_CONTACT,
};

/** Lemon Squeezy hosted checkout URLs (Share → Buy link). Empty until configured. */
export const LEMON = {
  checkoutIndie: envUrl("NEXT_PUBLIC_LEMONSQUEEZY_CHECKOUT_INDIE"),
  checkoutTeam: envUrl("NEXT_PUBLIC_LEMONSQUEEZY_CHECKOUT_TEAM"),
};

export function contactHref(subject = "Dino — Team / Large Teams"): string {
  const email = GITHUB.contactEmail;
  return `mailto:${email}?subject=${encodeURIComponent(subject)}`;
}

export function packCheckoutHref(
  tier: "free" | "indie" | "team" | "large",
): { href: string; lemon: boolean } {
  if (tier === "free") return { href: GITHUB.readme, lemon: false };
  if (tier === "indie") {
    if (LEMON.checkoutIndie) return { href: LEMON.checkoutIndie, lemon: true };
    return {
      href: contactHref("Dino — Indie Pack (€49)"),
      lemon: false,
    };
  }
  if (tier === "team") {
    if (LEMON.checkoutTeam) return { href: LEMON.checkoutTeam, lemon: true };
    return { href: contactHref("Dino — Team Pack"), lemon: false };
  }
  return { href: contactHref("Dino — Large Teams"), lemon: false };
}
