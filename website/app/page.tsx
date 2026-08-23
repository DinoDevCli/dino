import Link from "next/link";
import {
  DEMO,
  EARLY,
  FLOW,
  HERO,
  PROBLEM_SOLUTION,
  QUICKSTART,
  SITE,
  USP_WIDE,
  USPS,
} from "@/lib/content";
import { GITHUB, earlyAccessMailto } from "@/lib/site";

const shell = "mx-auto w-full max-w-content px-6";

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Hero */}
      <section
        className={`${shell} flex min-h-[70vh] flex-col items-start justify-center py-24`}
      >
        <span className="font-mono text-sm uppercase tracking-wider text-accent">
          {HERO.badge}
        </span>
        <h1 className="mt-4 text-5xl font-bold leading-[1.1] tracking-tightest md:text-6xl lg:text-7xl">
          <span className="text-foreground">{HERO.line1}</span>
          <br />
          <span className="text-accent">{HERO.line2}</span>
        </h1>
        <p className="mt-6 max-w-[600px] text-xl leading-relaxed text-muted">
          {HERO.subtitle}
        </p>
        <div className="mt-12 flex flex-wrap gap-4">
          <a
            href="#demo"
            className="bg-accent px-8 py-3 font-medium text-white hover:bg-accent-hover"
          >
            ▶ Live Demo
          </a>
          <a
            href="#early-access"
            className="border border-border px-8 py-3 font-medium text-foreground hover:border-accent hover:text-accent"
          >
            Early Access →
          </a>
        </div>
        <p className="mt-16 font-mono text-sm text-muted">
          <a
            href={GITHUB.base}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-accent"
          >
            {HERO.footnote}
          </a>
        </p>
      </section>

      {/* Problem ↔ Solution */}
      <section
        className={`${shell} grid grid-cols-1 gap-12 border-t border-border py-24 md:grid-cols-5 md:gap-16`}
      >
        <div className="md:col-span-2">
          <span className="font-mono text-sm text-muted">
            {PROBLEM_SOLUTION.problemLabel}
          </span>
          <h2 className="mt-4 text-3xl font-bold tracking-tighter">
            {PROBLEM_SOLUTION.problemTitle}
          </h2>
          <p className="mt-4 leading-relaxed text-muted">
            {PROBLEM_SOLUTION.problemBody}
          </p>
        </div>
        <div className="hidden justify-center md:col-span-1 md:flex">
          <div className="h-full w-px bg-border" aria-hidden />
        </div>
        <div className="md:col-span-2">
          <span className="font-mono text-sm text-accent">
            {PROBLEM_SOLUTION.solutionLabel}
          </span>
          <h2 className="mt-4 text-3xl font-bold tracking-tighter">
            {PROBLEM_SOLUTION.solutionTitle}
          </h2>
          <p className="mt-4 leading-relaxed text-muted">
            {PROBLEM_SOLUTION.solutionBody}
          </p>
        </div>
      </section>

      {/* Engine flow */}
      <section className={`${shell} border-t border-border py-24`}>
        <h2 className="text-3xl font-bold tracking-tighter">How Dino works</h2>
        <div className="mt-12 flex flex-col gap-4 md:flex-row md:items-stretch md:justify-between">
          {FLOW.map((step, i) => (
            <div key={step.step} className="flex flex-1 flex-col gap-4 md:flex-row md:items-center">
              <div
                className={`flex-1 border border-border bg-surface p-6 ${
                  step.accent ? "" : "opacity-60"
                }`}
              >
                <span
                  className={`font-mono text-sm ${
                    step.accent ? "text-accent" : "text-muted"
                  }`}
                >
                  {step.step}
                </span>
                <p className="mt-2 font-medium text-foreground">{step.title}</p>
                <p className="text-sm text-muted">{step.detail}</p>
              </div>
              {i < FLOW.length - 1 ? (
                <span
                  className="hidden text-2xl text-border md:block"
                  aria-hidden
                >
                  →
                </span>
              ) : null}
            </div>
          ))}
        </div>
      </section>

      {/* USPs */}
      <section
        className={`${shell} grid grid-cols-1 gap-x-16 gap-y-8 border-t border-border py-24 sm:grid-cols-2`}
      >
        {USPS.map((usp) => (
          <div key={usp.label}>
            <h3 className="font-mono text-sm text-accent">{usp.label}</h3>
            <p className="mt-1 font-medium text-foreground">{usp.title}</p>
            <p className="text-sm text-muted">{usp.body}</p>
          </div>
        ))}
        <div className="col-span-1 border-t border-border pt-8 sm:col-span-2">
          <h3 className="font-mono text-sm text-accent">{USP_WIDE.label}</h3>
          <p className="mt-1 font-medium text-foreground">{USP_WIDE.title}</p>
          <p className="text-sm text-muted">{USP_WIDE.body}</p>
        </div>
      </section>

      {/* Live Demo */}
      <section
        id="demo"
        className="mx-auto w-full max-w-narrow border-t border-border px-6 py-24"
      >
        <h2 className="text-3xl font-bold tracking-tighter">{DEMO.title}</h2>
        <p className="mt-2 text-muted">{DEMO.subtitle}</p>
        <div className="mt-12 overflow-hidden border border-border bg-code-bg">
          <pre className="overflow-x-auto p-6 font-mono text-sm leading-relaxed text-foreground">
            <code>{DEMO.transcript}</code>
          </pre>
        </div>
        <p className="mt-4 font-mono text-xs text-muted">
          Reproduce:{" "}
          <a
            href={`${GITHUB.base}/tree/main/tests/simulation`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-accent hover:underline"
          >
            make demo
          </a>{" "}
          in tests/simulation
        </p>
      </section>

      {/* Quickstart */}
      <section className="mx-auto w-full max-w-narrow border-t border-border px-6 py-24">
        <h2 className="text-3xl font-bold tracking-tighter">{QUICKSTART.title}</h2>
        <p className="mt-2 text-muted">{QUICKSTART.subtitle}</p>
        <div className="mt-12 overflow-x-auto border border-border bg-code-bg p-6">
          <pre className="font-mono text-sm leading-relaxed text-foreground">
            <code>{QUICKSTART.code}</code>
          </pre>
        </div>
      </section>

      {/* Early Access */}
      <section
        id="early-access"
        className={`${shell} grid grid-cols-1 gap-12 border-t border-border py-24 md:grid-cols-2 md:gap-16`}
      >
        <div>
          <span className="font-mono text-sm text-accent">{EARLY.label}</span>
          <h2 className="mt-4 text-3xl font-bold tracking-tighter">
            {EARLY.title}
          </h2>
          <p className="mt-4 leading-relaxed text-muted">{EARLY.body}</p>
          <div className="mt-8 space-y-2 font-mono text-sm text-muted">
            <p>
              → 01. Email{" "}
              <a href={earlyAccessMailto()} className="text-accent hover:underline">
                {EARLY.email}
              </a>
            </p>
            <p>→ 02. Name your team / project</p>
            <p>→ 03. Receive a Team Key</p>
            <p>→ 04. Upgrade & start sealing</p>
          </div>
        </div>
        <div className="flex items-center justify-center border border-border bg-surface p-12">
          <a
            href={earlyAccessMailto()}
            className="text-center text-2xl font-bold text-accent hover:underline"
          >
            {EARLY.email} →
          </a>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-12">
        <div
          className={`${shell} flex flex-col gap-4 text-sm text-muted sm:flex-row sm:justify-between`}
        >
          <span>
            {SITE.brand} — Local-First Audit Engine
          </span>
          <span className="flex flex-wrap gap-x-4 gap-y-2">
            <span>
              v{SITE.version} · Early Access · MIT
            </span>
            <Link href="/docs" className="hover:text-accent">
              Docs
            </Link>
            <a
              href={GITHUB.base}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-accent"
            >
              GitHub
            </a>
          </span>
        </div>
      </footer>
    </div>
  );
}
