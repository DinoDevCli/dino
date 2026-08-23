import Link from "next/link";
import { CopyButton } from "@/components/CopyButton";
import {
  ABOUT,
  ARCH_FLOW,
  CLI_EXAMPLES,
  CONTRACT_FOOTNOTE,
  EARLY_ACCESS,
  ENGINE_POINTS,
  EXPORT_CONTRACTS,
  FAQ,
  GUARANTEES,
  ICPS,
  INDEX_FEATURES,
  INTEGRATE,
  MODULES,
  NAV,
  PAINPOINTS,
  QUICKSTART,
  SECTIONS,
  SITE,
  WHY_LOCAL_FIRST,
} from "@/lib/content";
import { GITHUB, earlyAccessMailto } from "@/lib/site";

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
      className={cls.trim()}
    >
      {children}
    </a>
  );
}

export default function Home() {
  return (
    <div className="min-h-screen">
      <div className="border-border bg-foreground/[0.03] border-b px-6 py-3 text-center font-mono text-xs tracking-[0.12em] uppercase md:px-10">
        {EARLY_ACCESS.banner}
      </div>
      <header className="px-6 pt-10 pb-20 md:px-10 md:pt-14 md:pb-32">
        <div className="mx-auto max-w-6xl">
          <nav
            className="flex items-center justify-between"
            aria-label="Primary"
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
            <p className="text-muted-foreground font-mono text-xs tracking-[0.2em] uppercase">
              Dino
            </p>
            <h1 className="text-4xl leading-[1.05] tracking-tight text-balance md:text-6xl lg:text-7xl">
              {SITE.tagline}
            </h1>
            <p className="text-muted-foreground max-w-2xl text-lg leading-relaxed text-pretty">
              {SITE.subtitle}
            </p>
            <p className="text-muted-foreground max-w-2xl text-sm leading-relaxed">
              {SITE.earlyAccessCta}
            </p>
            <div className="flex flex-wrap gap-3">
              <ExternalLink href={GITHUB.earlyAccessIssue} primary>
                Request Early Access
              </ExternalLink>
              <ExternalLink href={earlyAccessMailto()}>
                Email
              </ExternalLink>
              <ExternalLink href={GITHUB.base}>GitHub</ExternalLink>
              <a
                href="#quickstart"
                className="border-border hover:border-foreground border px-6 py-3 font-mono text-xs tracking-[0.15em] uppercase"
              >
                Quickstart
              </a>
            </div>
          </div>
        </div>
      </header>

      <main>
        <SectionShell id="quickstart" compact>
          <SectionHeader
            label={SECTIONS.quickstart.label}
            title={SECTIONS.quickstart.title}
          />
          <div className="border-border flex flex-col border-t border-l">
            {QUICKSTART.map((ex) => (
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
        </SectionShell>

        <SectionShell id="flow" compact>
          <SectionHeader
            label={SECTIONS.flow.label}
            title={SECTIONS.flow.title}
          />
          <pre className="border-border text-foreground overflow-x-auto border px-6 py-8 font-mono text-sm leading-relaxed tracking-wide md:text-base">
            <code>{ARCH_FLOW}</code>
          </pre>
        </SectionShell>

        <SectionShell id="why-local" compact>
          <SectionHeader
            label={SECTIONS.whyLocal.label}
            title={SECTIONS.whyLocal.title}
          />
          <div className="border-border grid border-t border-l sm:grid-cols-3">
            {WHY_LOCAL_FIRST.map((p) => (
              <GridCard key={p.title} title={p.title} body={p.body} />
            ))}
          </div>
        </SectionShell>

        <SectionShell id="engine" compact>
          <SectionHeader
            label={SECTIONS.about.label}
            title={SECTIONS.about.title}
          />
          <div className="max-w-4xl space-y-4 text-lg leading-relaxed text-pretty md:text-xl">
            {ABOUT.map((paragraph) => (
              <p key={paragraph}>{paragraph}</p>
            ))}
          </div>
          <div className="border-border grid border-t border-l sm:grid-cols-3">
            {ENGINE_POINTS.map((p) => (
              <GridCard key={p.title} title={p.title} body={p.body} />
            ))}
          </div>
        </SectionShell>

        <SectionShell compact>
          <SectionHeader
            label={SECTIONS.audience.label}
            title={SECTIONS.audience.title}
          />
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
          <SectionHeader
            label={SECTIONS.features.label}
            title={SECTIONS.features.title}
          />
          <div className="border-border grid border-t border-l sm:grid-cols-2 lg:grid-cols-3">
            {MODULES.map((m) => (
              <GridCard key={m.title} title={m.title} body={m.body} />
            ))}
          </div>
        </SectionShell>

        <SectionShell id="export" compact>
          <SectionHeader
            label={SECTIONS.export.label}
            title={SECTIONS.export.title}
          />
          <div className="border-border grid border-t border-l sm:grid-cols-3">
            {EXPORT_CONTRACTS.map((c) => (
              <GridCard key={c.title} title={c.title} body={c.body} />
            ))}
          </div>
        </SectionShell>

        <SectionShell id="index" compact>
          <SectionHeader
            label={SECTIONS.index.label}
            title={SECTIONS.index.title}
          />
          <div className="border-border grid border-t border-l sm:grid-cols-2 lg:grid-cols-4">
            {INDEX_FEATURES.map((f) => (
              <GridCard key={f.title} title={f.title} body={f.body} />
            ))}
          </div>
        </SectionShell>

        <SectionShell id="integrate" compact>
          <SectionHeader
            label={SECTIONS.integrate.label}
            title={SECTIONS.integrate.title}
          />
          <div className="border-border grid border-t border-l sm:grid-cols-3">
            {INTEGRATE.map((i) => (
              <GridCard key={i.title} title={i.title} body={i.body} />
            ))}
          </div>
        </SectionShell>

        <SectionShell id="contract" compact>
          <SectionHeader
            label={SECTIONS.contract.label}
            title={SECTIONS.contract.title}
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
              Proof Contract ↗
            </a>
          </p>
        </SectionShell>

        <SectionShell id="cli" compact>
          <SectionHeader
            label={SECTIONS.cli.label}
            title={SECTIONS.cli.title}
          />
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
            {SECTIONS.cliHint}
          </p>
          <p className="text-muted-foreground text-sm leading-relaxed">
            <Link
              href="/docs"
              className="text-foreground underline underline-offset-4"
            >
              {SECTIONS.docsHint}
            </Link>{" "}
            ·{" "}
            <a
              href={GITHUB.docs.cliReference}
              target="_blank"
              rel="noopener noreferrer"
              className="text-foreground underline underline-offset-4"
            >
              {SECTIONS.cliRef}
            </a>
          </p>
        </SectionShell>

        <SectionShell id="early-access" compact>
          <SectionHeader
            label={SECTIONS.earlyAccess.label}
            title={SECTIONS.earlyAccess.title}
          />
          <ul className="text-muted-foreground max-w-3xl space-y-3 font-mono text-sm leading-relaxed">
            {EARLY_ACCESS.bullets.map((item) => (
              <li key={item} className="flex gap-3">
                <span aria-hidden="true">—</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
          <div className="flex flex-wrap gap-3">
            <ExternalLink href={GITHUB.earlyAccessIssue} primary>
              Request Early Access
            </ExternalLink>
            <ExternalLink href={earlyAccessMailto()}>
              {EARLY_ACCESS.email}
            </ExternalLink>
          </div>
        </SectionShell>

        <SectionShell id="faq" compact>
          <SectionHeader
            label={SECTIONS.faq.label}
            title={SECTIONS.faq.title}
          />
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
        <div className="mx-auto flex max-w-6xl flex-col gap-6">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <span className="font-mono text-sm tracking-[0.3em] uppercase">
              dino{" "}
              <span className="text-muted-foreground tracking-normal normal-case">
                Early Access · MIT · v{SITE.version}
              </span>
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
                    Proof Contract
                  </a>
                </li>
                <li>
                  <a
                    className="hover:text-foreground"
                    href={GITHUB.earlyAccessIssue}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Early Access
                  </a>
                </li>
                <li>
                  <a
                    className="hover:text-foreground"
                    href={`${GITHUB.base}/blob/main/LICENSE`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    MIT
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
              </ul>
            </nav>
          </div>
          <p className="text-muted-foreground font-mono text-xs tracking-wide">
            {SECTIONS.footerLine}
          </p>
        </div>
      </footer>
    </div>
  );
}
