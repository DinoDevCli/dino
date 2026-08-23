import { Button } from "@/components/Button";
import { Footer } from "@/components/Footer";
import { Container, Heading, MonoLabel, Section } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { TerminalPlayer } from "@/components/TerminalPlayer";
import { EngineFlow, UspList } from "@/components/Tiles";
import {
  DEMO_LINES,
  EARLY,
  FLOW,
  HERO,
  PROBLEM_SOLUTION,
  QUICKSTART,
  USPS,
  USP_WIDE,
} from "@/lib/content";
import { GITHUB, earlyAccessMailto } from "@/lib/site";

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav active="home" />

      {/* 1. Hero */}
      <section className="relative isolate overflow-hidden">
        <div className="hero-grid absolute inset-0 -z-10" aria-hidden />
        <Container className="flex min-h-[70vh] flex-col items-start justify-center py-section">
          <span className="font-mono text-sm uppercase tracking-wider text-accent">
            {HERO.badge}
          </span>
          <Heading as="h1">
            <span className="mt-4 block text-foreground">{HERO.line1}</span>
            <span className="block text-accent">{HERO.line2}</span>
          </Heading>
          <p className="mt-6 max-w-[600px] text-xl leading-relaxed text-muted">
            {HERO.subtitle}
          </p>
          <div className="mt-12 flex flex-wrap gap-4">
            <Button href="#demo">▶ Live Demo</Button>
            <Button href="#early-access" variant="secondary">
              Early Access →
            </Button>
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
        </Container>
      </section>

      {/* 2. Problem ↔ Solution */}
      <Section id="problem">
        <Container className="grid grid-cols-1 gap-12 md:grid-cols-5 md:gap-16">
          <div className="md:col-span-2">
            <MonoLabel>{PROBLEM_SOLUTION.problemLabel}</MonoLabel>
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
            <MonoLabel accent>{PROBLEM_SOLUTION.solutionLabel}</MonoLabel>
            <h2 className="mt-4 text-3xl font-bold tracking-tighter">
              {PROBLEM_SOLUTION.solutionTitle}
            </h2>
            <p className="mt-4 leading-relaxed text-muted">
              {PROBLEM_SOLUTION.solutionBody}
            </p>
          </div>
        </Container>
      </Section>

      {/* 3. Engine flow */}
      <Section id="engine">
        <Container>
          <h2 className="text-3xl font-bold tracking-tighter">How Dino works</h2>
          <p className="mt-2 font-mono text-sm text-muted">
            pipeline → seal → export → proof_index.json → dashboard
          </p>
          <EngineFlow steps={FLOW} />
        </Container>
      </Section>

      {/* 4. USPs — spec list */}
      <Section id="capabilities">
        <Container>
          <UspList items={USPS} wide={USP_WIDE} />
        </Container>
      </Section>

      {/* 5. Live Demo */}
      <Section id="demo">
        <Container narrow>
          <h2 className="text-3xl font-bold tracking-tighter">Live Demo</h2>
          <p className="mt-2 text-muted">Two runs. One compare. The proof.</p>
          <div className="mt-12">
            <TerminalPlayer lines={DEMO_LINES} />
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
        </Container>
      </Section>

      {/* 6. Quickstart */}
      <Section id="quickstart">
        <Container narrow>
          <h2 className="text-3xl font-bold tracking-tighter">Quickstart</h2>
          <p className="mt-2 text-muted">Install. Run. Get proofs.</p>
          <div className="mt-12 overflow-x-auto border border-border bg-code-bg p-6">
            <pre className="font-mono text-sm leading-relaxed text-foreground">
              <code>{QUICKSTART}</code>
            </pre>
          </div>
        </Container>
      </Section>

      {/* 7. Early Access */}
      <Section id="early-access">
        <Container className="grid grid-cols-1 gap-12 md:grid-cols-2 md:gap-16">
          <div>
            <MonoLabel accent>{EARLY.label}</MonoLabel>
            <h2 className="mt-4 text-3xl font-bold tracking-tighter">
              {EARLY.title}
            </h2>
            <p className="mt-4 leading-relaxed text-muted">{EARLY.body}</p>
            <div className="mt-8 space-y-2 font-mono text-sm text-muted">
              <p>
                → 01. Email{" "}
                <a
                  href={earlyAccessMailto()}
                  className="text-accent hover:underline"
                >
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
        </Container>
      </Section>

      <Footer />
    </div>
  );
}
