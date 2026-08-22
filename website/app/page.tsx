import Link from "next/link";
import { CopyButton } from "@/components/CopyButton";
import {
  ABOUT,
  CLI_EXAMPLES,
  CONTRACT_FOOTNOTE,
  FAQ,
  GUARANTEES,
  ICPS,
  MODULES,
  NAV,
  PACKS,
  PAINPOINTS,
  SITE,
} from "@/lib/content";
import { GITHUB, contactHref } from "@/lib/site";

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <p className="text-muted-foreground font-mono text-xs tracking-[0.2em] uppercase">
      {children}
    </p>
  );
}

function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="max-w-3xl text-3xl leading-tight tracking-tight text-balance md:text-4xl">
      {children}
    </h2>
  );
}

function SectionShell({
  id,
  children,
  compact = false,
}: {
  id?: string;
  children: React.ReactNode;
  compact?: boolean;
}) {
  return (
    <section
      id={id}
      className={`border-border border-t px-6 md:px-10 ${
        compact ? "py-16 md:py-20" : "py-20 md:py-28"
      }`}
    >
      <div className="mx-auto flex max-w-6xl flex-col gap-10">{children}</div>
    </section>
  );
}

function SectionHeader({
  label,
  title,
}: {
  label: string;
  title?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col gap-4">
      <SectionLabel>{label}</SectionLabel>
      {title ? <SectionTitle>{title}</SectionTitle> : null}
    </div>
  );
}

function GridCard({ title, body }: { title: string; body: string }) {
  return (
    <div className="border-border flex flex-col gap-3 border-r border-b p-6 md:p-8">
      <h3 className="text-base tracking-tight">{title}</h3>
      <p className="text-muted-foreground text-sm leading-relaxed">{body}</p>
    </div>
  );
}

function MonoList({ items }: { items: string[] }) {
  return (
    <ul className="border-border grid border-t sm:grid-cols-2">
      {items.map((item) => (
        <li
          key={item}
          className="border-border flex items-baseline gap-4 border-b px-1 py-5 sm:odd:border-r sm:odd:pr-8 sm:even:pl-8"
        >
          <span
            aria-hidden="true"
            className="text-muted-foreground font-mono text-xs"
          >
            —
          </span>
          <span className="font-mono text-sm leading-relaxed">{item}</span>
        </li>
      ))}
    </ul>
  );
}

function ExternalLink({
  href,
  children,
  primary = false,
  className = "",
}: {
  href: string;
  children: React.ReactNode;
  primary?: boolean;
  className?: string;
}) {
  const base =
    "border px-6 py-3 font-mono text-xs tracking-[0.15em] uppercase inline-block text-center";
  const cls = primary
    ? `${base} border-foreground bg-foreground text-background hover:bg-foreground/90 ${className}`
    : `${base} border-border text-foreground hover:border-foreground ${className}`;
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={cls}
    >
      {children}
    </a>
  );
}

function packHref(tier: "free" | "indie" | "team"): string {
  if (tier === "team") return contactHref();
  if (tier === "indie") return GITHUB.releases;
  return GITHUB.readme;
}

export default function Home() {
  return (
    <div className="min-h-screen">
      <header className="px-6 pt-10 pb-20 md:px-10 md:pt-14 md:pb-32">
        <div className="mx-auto max-w-6xl">
          <nav
            className="flex items-center justify-between"
            aria-label="Hauptnavigation"
          >
            <span className="font-mono text-sm tracking-[0.3em] uppercase">
              dino
            </span>
            <ul className="text-muted-foreground hidden gap-8 font-mono text-xs tracking-[0.15em] uppercase md:flex">
              {NAV.map((item) => (
                <li key={item.href}>
                  {item.href.startsWith("/") ? (
                    <Link className="hover:text-foreground" href={item.href}>
                      {item.label}
                    </Link>
                  ) : (
                    <a className="hover:text-foreground" href={item.href}>
                      {item.label}
                    </a>
                  )}
                </li>
              ))}
            </ul>
          </nav>

          <div className="mt-24 flex max-w-4xl flex-col gap-8 md:mt-40">
            <h1 className="text-4xl leading-[1.05] tracking-tight text-balance md:text-6xl lg:text-7xl">
              {SITE.tagline}
            </h1>
            <p className="text-muted-foreground max-w-2xl text-lg leading-relaxed text-pretty">
              {SITE.subtitle.split("proof.json")[0]}
              <span className="text-foreground font-mono">proof.json</span>.
            </p>
            <div className="flex flex-wrap gap-3">
              <ExternalLink href={GITHUB.releases} primary>
                Download
              </ExternalLink>
              <ExternalLink href={GITHUB.base}>GitHub</ExternalLink>
              <a
                href="#cli"
                className="border-border hover:border-foreground border px-6 py-3 font-mono text-xs tracking-[0.15em] uppercase"
              >
                CLI
              </a>
            </div>
          </div>
        </div>
      </header>

      <main>
        <SectionShell compact>
          <SectionHeader label="Was ist Dino" />
          <div className="max-w-4xl space-y-4 text-lg leading-relaxed text-pretty md:text-xl">
            {ABOUT.map((paragraph) => (
              <p key={paragraph}>{paragraph}</p>
            ))}
          </div>
        </SectionShell>

        <SectionShell compact>
          <SectionHeader label="Für wen" title="ICP & Painpoints" />
          <div className="border-border grid border-t border-l sm:grid-cols-2">
            {ICPS.map((icp) => (
              <GridCard key={icp.title} title={icp.title} body={icp.body} />
            ))}
          </div>
          <div className="border-border grid border-t border-l sm:grid-cols-2 lg:grid-cols-4">
            {PAINPOINTS.map((p) => (
              <GridCard key={p.title} title={p.title} body={p.body} />
            ))}
          </div>
        </SectionShell>

        <SectionShell id="features" compact>
          <SectionHeader label="Features" title="Sieben Module, ein Proof" />
          <div className="border-border grid border-t border-l sm:grid-cols-2 lg:grid-cols-3">
            {MODULES.map((m) => (
              <GridCard key={m.title} title={m.title} body={m.body} />
            ))}
          </div>
        </SectionShell>

        <SectionShell id="contract" compact>
          <SectionHeader
            label="Proof-Contract"
            title="Dino erfüllt den Proof-Contract"
          />
          <MonoList items={GUARANTEES} />
          <p className="text-muted-foreground max-w-3xl text-sm leading-relaxed">
            {CONTRACT_FOOTNOTE}{" "}
            <a
              href={GITHUB.docs.proofContract}
              target="_blank"
              rel="noopener noreferrer"
              className="text-foreground font-mono underline underline-offset-4"
            >
              Proof-Contract ↗
            </a>
          </p>
        </SectionShell>

        <SectionShell id="cli" compact>
          <SectionHeader label="CLI" title="Drei Kommandos" />
          <div className="border-border flex flex-col border-t border-l">
            {CLI_EXAMPLES.map((ex) => (
              <div key={ex.label} className="border-border border-r border-b">
                <div className="border-border flex items-center justify-between border-b px-6 py-3">
                  <p className="text-muted-foreground font-mono text-xs tracking-[0.2em] uppercase">
                    {ex.label}
                  </p>
                  <CopyButton text={ex.code} />
                </div>
                <pre className="text-foreground overflow-x-auto px-6 py-6 font-mono text-sm leading-relaxed">
                  <code>{ex.code}</code>
                </pre>
              </div>
            ))}
          </div>
          <p className="text-muted-foreground text-sm leading-relaxed">
            <Link href="/docs" className="text-foreground underline underline-offset-4">
              Vollständige Docs
            </Link>{" "}
            ·{" "}
            <a
              href={GITHUB.docs.cliReference}
              target="_blank"
              rel="noopener noreferrer"
              className="text-foreground underline underline-offset-4"
            >
              CLI-E2E-Referenz ↗
            </a>
          </p>
        </SectionShell>

        <SectionShell id="pricing" compact>
          <SectionHeader label="Pricing" title="Ein Preis, keine Abos" />
          <div className="border-border grid border-t border-l md:grid-cols-3">
            {PACKS.map((pack) => (
              <div
                key={pack.name}
                className={`border-border flex flex-col gap-8 border-r border-b p-6 md:p-8 ${
                  pack.featured ? "bg-foreground/[0.03]" : ""
                }`}
              >
                <div className="flex flex-col gap-3">
                  <h3 className="font-mono text-xs tracking-[0.2em] uppercase">
                    {pack.name}
                  </h3>
                  <p className="text-4xl tracking-tight">{pack.price}</p>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    {pack.hint}
                  </p>
                </div>
                <ExternalLink
                  href={packHref(pack.tier)}
                  className="mt-auto px-5 py-3"
                >
                  {pack.cta}
                </ExternalLink>
              </div>
            ))}
          </div>
        </SectionShell>

        <SectionShell id="faq" compact>
          <SectionHeader label="FAQ" title="Häufige Fragen" />
          <dl className="border-border border-t">
            {FAQ.map((item) => (
              <div
                key={item.q}
                className="border-border grid gap-3 border-b py-8 md:grid-cols-2 md:gap-10"
              >
                <dt className="text-lg tracking-tight">{item.q}</dt>
                <dd className="text-muted-foreground text-sm leading-relaxed">
                  {item.a}
                </dd>
              </div>
            ))}
          </dl>
        </SectionShell>
      </main>

      <footer className="border-border border-t px-6 py-12 md:px-10">
        <div className="mx-auto flex max-w-6xl flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <span className="font-mono text-sm tracking-[0.3em] uppercase">
            dino
          </span>
          <nav aria-label="Footer">
            <ul className="text-muted-foreground flex flex-wrap gap-x-6 gap-y-3 font-mono text-xs tracking-[0.15em] uppercase">
              <li>
                <Link className="hover:text-foreground" href="/docs">
                  Docs
                </Link>
              </li>
              <li>
                <a
                  className="hover:text-foreground"
                  href={GITHUB.docs.proofContract}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Proof-Contract
                </a>
              </li>
              <li>
                <a
                  className="hover:text-foreground"
                  href={GITHUB.base}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  GitHub
                </a>
              </li>
              <li>
                <a className="hover:text-foreground" href="#pricing">
                  Pricing
                </a>
              </li>
              <li>
                <a
                  className="hover:text-foreground"
                  href={contactHref()}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Contact
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </footer>
    </div>
  );
}
