import Link from "next/link";
import { CopyButton } from "@/components/CopyButton";
import {
  ACCESS,
  DEMO,
  EARLY_ACCESS,
  ENGINE,
  FAQ,
  FOOTER,
  MOMENT_OF_TRUTH,
  NAV,
  PROBLEM,
  SITE,
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
}: {
  id?: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} className="border-border border-t px-6 py-16 md:px-10 md:py-24">
      <div className="mx-auto flex max-w-6xl flex-col gap-10">{children}</div>
    </section>
  );
}

function CodeBlock({ label, code }: { label: string; code: string }) {
  return (
    <div className="border-border border-r border-b">
      <div className="border-border flex items-center justify-between border-b px-6 py-3">
        <p className="text-muted-foreground font-mono text-xs tracking-[0.2em] uppercase">
          {label}
        </p>
        <CopyButton text={code} />
      </div>
      <pre className="text-foreground overflow-x-auto px-6 py-6 font-mono text-sm leading-relaxed">
        <code>{code}</code>
      </pre>
    </div>
  );
}

function ExternalLink({
  href,
  children,
  primary = false,
}: {
  href: string;
  children: React.ReactNode;
  primary?: boolean;
}) {
  const base =
    "border px-6 py-3 font-mono text-xs tracking-[0.15em] uppercase inline-block text-center";
  const cls = primary
    ? `${base} border-foreground bg-foreground text-background hover:bg-foreground/90`
    : `${base} border-border text-foreground hover:border-foreground`;
  return (
    <a href={href} target="_blank" rel="noopener noreferrer" className={cls}>
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

      <header className="px-6 pt-10 pb-16 md:px-10 md:pt-14 md:pb-28">
        <div className="mx-auto max-w-6xl">
          <nav className="flex items-center justify-between" aria-label="Primary">
            <span className="font-mono text-sm tracking-[0.3em] uppercase">
              {SITE.brand}
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

          <div className="mt-20 flex max-w-4xl flex-col gap-8 md:mt-32">
            <p className="text-muted-foreground font-mono text-xs tracking-[0.2em] uppercase">
              v{SITE.version} · Early Access
            </p>
            <h1 className="text-4xl leading-[1.05] tracking-tight text-balance md:text-6xl lg:text-7xl">
              {SITE.tagline}
            </h1>
            <p className="text-xl leading-relaxed tracking-tight md:text-2xl">
              {SITE.promise}
            </p>
            <p className="text-muted-foreground max-w-2xl text-lg leading-relaxed text-pretty">
              {SITE.subtitle}
            </p>
            <div className="flex flex-wrap gap-3">
              <ExternalLink href={earlyAccessMailto()} primary>
                Request Early Access
              </ExternalLink>
              <a
                href="#demo"
                className="border-border hover:border-foreground border px-6 py-3 font-mono text-xs tracking-[0.15em] uppercase"
              >
                Live Demo
              </a>
              <ExternalLink href={GITHUB.base}>GitHub</ExternalLink>
            </div>
          </div>
        </div>
      </header>

      <main>
        {/* Why now */}
        <SectionShell id="why-now">
          <SectionLabel>Why now</SectionLabel>
          <p className="max-w-3xl text-2xl leading-snug tracking-tight text-balance md:text-3xl">
            {MOMENT_OF_TRUTH}
          </p>
        </SectionShell>

        {/* Problem */}
        <SectionShell id="problem">
          <div className="flex flex-col gap-4">
            <SectionLabel>{PROBLEM.label}</SectionLabel>
            <SectionTitle>{PROBLEM.title}</SectionTitle>
            <p className="text-muted-foreground max-w-3xl text-lg leading-relaxed text-pretty">
              {PROBLEM.body}
            </p>
          </div>
          <div className="border-border grid border-t border-l sm:grid-cols-3">
            {PROBLEM.pains.map((p) => (
              <div
                key={p.title}
                className="border-border flex flex-col gap-3 border-r border-b p-6 md:p-8"
              >
                <h3 className="text-base tracking-tight">{p.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">{p.body}</p>
              </div>
            ))}
          </div>
        </SectionShell>

        {/* Engine */}
        <SectionShell id="engine">
          <div className="flex flex-col gap-4">
            <SectionLabel>{ENGINE.label}</SectionLabel>
            <SectionTitle>{ENGINE.title}</SectionTitle>
          </div>
          <pre className="border-border text-foreground overflow-x-auto border px-6 py-8 font-mono text-sm leading-relaxed tracking-wide md:text-base">
            <code>{ENGINE.flow}</code>
          </pre>
          <div className="border-border grid border-t border-l sm:grid-cols-3">
            {ENGINE.contracts.map((c) => (
              <div
                key={c.id}
                className="border-border flex flex-col gap-3 border-r border-b p-6 md:p-8"
              >
                <h3 className="font-mono text-sm tracking-tight">{c.id}</h3>
                <p className="text-muted-foreground font-mono text-xs">{c.schema}</p>
                <p className="text-muted-foreground text-sm leading-relaxed">{c.body}</p>
              </div>
            ))}
          </div>
          <div className="border-border grid border-t border-l sm:grid-cols-3">
            {ENGINE.localFirst.map((p) => (
              <div
                key={p.title}
                className="border-border flex flex-col gap-3 border-r border-b p-6 md:p-8"
              >
                <h3 className="text-base tracking-tight">{p.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">{p.body}</p>
              </div>
            ))}
          </div>
        </SectionShell>

        {/* Live Demo */}
        <SectionShell id="demo">
          <div className="flex flex-col gap-4">
            <SectionLabel>{DEMO.label}</SectionLabel>
            <SectionTitle>{DEMO.title}</SectionTitle>
            <p className="text-muted-foreground max-w-3xl text-lg leading-relaxed text-pretty">
              {DEMO.intro}
            </p>
          </div>

          <div className="border-border grid border-t border-l sm:grid-cols-2">
            {[DEMO.runA, DEMO.runB].map((run) => (
              <div
                key={run.label}
                className="border-border flex flex-col gap-2 border-r border-b p-6 md:p-8"
              >
                <h3 className="font-mono text-xs tracking-[0.15em] uppercase">
                  {run.label}
                </h3>
                <p className="text-muted-foreground text-sm">{run.detail}</p>
                <p className="font-mono text-sm">
                  proof_hash {run.hash}
                </p>
              </div>
            ))}
          </div>

          <div className="border-border flex flex-col border-t border-l">
            {DEMO.commands.map((ex) => (
              <CodeBlock key={ex.label} label={ex.label} code={ex.code} />
            ))}
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <div className="border-border border">
              <div className="border-border border-b px-6 py-3">
                <p className="text-muted-foreground font-mono text-xs tracking-[0.2em] uppercase">
                  proof.json (excerpt)
                </p>
              </div>
              <pre className="overflow-x-auto px-6 py-6 font-mono text-xs leading-relaxed md:text-sm">
                <code>{DEMO.proofExcerpt}</code>
              </pre>
            </div>
            <div className="border-border border">
              <div className="border-border border-b px-6 py-3">
                <p className="text-muted-foreground font-mono text-xs tracking-[0.2em] uppercase">
                  proof_index.json (excerpt)
                </p>
              </div>
              <pre className="overflow-x-auto px-6 py-6 font-mono text-xs leading-relaxed md:text-sm">
                <code>{DEMO.indexExcerpt}</code>
              </pre>
            </div>
          </div>

          <div className="border-border border">
            <div className="border-border flex items-center justify-between border-b px-6 py-3">
              <p className="text-muted-foreground font-mono text-xs tracking-[0.2em] uppercase">
                compare result
              </p>
              <CopyButton text={DEMO.compareExcerpt} />
            </div>
            <pre className="overflow-x-auto px-6 py-6 font-mono text-xs leading-relaxed md:text-sm">
              <code>{DEMO.compareExcerpt}</code>
            </pre>
            <p className="border-border text-muted-foreground border-t px-6 py-5 text-sm leading-relaxed">
              {DEMO.compareCallout}
            </p>
          </div>

          <p className="text-muted-foreground font-mono text-xs tracking-wide">
            {DEMO.makeHint}{" "}
            <a
              href={`${GITHUB.base}/tree/main/tests/simulation`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-foreground underline underline-offset-4"
            >
              tests/simulation ↗
            </a>
          </p>
        </SectionShell>

        {/* Early Access */}
        <SectionShell id="early-access">
          <div className="flex flex-col gap-4">
            <SectionLabel>{ACCESS.label}</SectionLabel>
            <SectionTitle>{ACCESS.title}</SectionTitle>
          </div>

          <div className="border-border grid border-t border-l sm:grid-cols-2">
            <div className="border-border flex flex-col gap-6 border-r border-b p-6 md:p-10">
              <h3 className="font-mono text-xs tracking-[0.2em] uppercase">
                {ACCESS.free.name}
              </h3>
              <ul className="space-y-3">
                {ACCESS.free.items.map((item) => (
                  <li key={item} className="flex gap-3 text-sm leading-relaxed">
                    <span className="text-muted-foreground font-mono" aria-hidden>
                      —
                    </span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="border-border bg-foreground/[0.03] flex flex-col gap-6 border-r border-b p-6 md:p-10">
              <h3 className="font-mono text-xs tracking-[0.2em] uppercase">
                {ACCESS.early.name}
              </h3>
              <ul className="space-y-3">
                {ACCESS.early.items.map((item) => (
                  <li key={item} className="flex gap-3 text-sm leading-relaxed">
                    <span className="text-muted-foreground font-mono" aria-hidden>
                      —
                    </span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="flex flex-col gap-6">
            <h3 className="font-mono text-xs tracking-[0.2em] uppercase">
              Next steps
            </h3>
            <ol className="border-border max-w-3xl space-y-0 border-t">
              {ACCESS.checklist.map((step, i) => (
                <li
                  key={step}
                  className="border-border flex gap-4 border-b py-5 text-sm leading-relaxed"
                >
                  <span className="text-muted-foreground font-mono text-xs">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <span>{step}</span>
                </li>
              ))}
            </ol>
            <div className="flex flex-wrap gap-3">
              <ExternalLink href={earlyAccessMailto()} primary>
                {ACCESS.cta}
              </ExternalLink>
              <ExternalLink href={GITHUB.earlyAccessIssue}>
                Open GitHub Issue
              </ExternalLink>
            </div>
            <p className="text-muted-foreground text-sm">{ACCESS.note}</p>
          </div>
        </SectionShell>

        {/* FAQ */}
        <SectionShell id="faq">
          <SectionLabel>FAQ</SectionLabel>
          <dl className="border-border border-t">
            {FAQ.map((item) => (
              <div
                key={item.q}
                className="border-border grid gap-3 border-b py-8 md:grid-cols-2 md:gap-10"
              >
                <dt className="text-lg tracking-tight">{item.q}</dt>
                <dd className="text-muted-foreground text-sm leading-relaxed">{item.a}</dd>
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
                  <a className="hover:text-foreground" href="#demo">
                    Demo
                  </a>
                </li>
                <li>
                  <a className="hover:text-foreground" href="#early-access">
                    Early Access
                  </a>
                </li>
                <li>
                  <Link className="hover:text-foreground" href="/docs">
                    Docs
                  </Link>
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
                  <a className="hover:text-foreground" href={earlyAccessMailto()}>
                    {EARLY_ACCESS.email}
                  </a>
                </li>
              </ul>
            </nav>
          </div>
          <p className="text-muted-foreground font-mono text-xs tracking-wide">
            {FOOTER.line}
          </p>
        </div>
      </footer>
    </div>
  );
}
