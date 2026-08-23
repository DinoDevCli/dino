import { Button } from "@/components/Button";
import { DemoWalkthrough } from "@/components/DemoWalkthrough";
import { Footer } from "@/components/Footer";
import { Container, MonoLabel, Section } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { TerminalPlayer } from "@/components/TerminalPlayer";
import { EngineFlow, UspList } from "@/components/Tiles";
import {
  DEMO_COPY,
  DEMO_LINES,
  DEMO_STEPS,
  EARLY,
  FLOW,
  HERO,
  PROBLEM_SOLUTION,
  QUICKSTART,
  USPS,
  USP_WIDE,
} from "@/lib/content";
import { GITHUB, earlyAccessMailto, siteHash } from "@/lib/site";

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav active="home" />

      {/* 1. Hero — static CLI prompt */}
      <section className="relative isolate overflow-hidden">
        <div className="hero-grid absolute inset-0 -z-10" aria-hidden />
        <Container className="flex min-h-[70vh] flex-col items-start justify-center py-section">
          <p className="font-mono text-sm text-muted">{HERO.prompt}</p>
          <h1 className="mt-4 text-5xl font-bold leading-[1.1] tracking-tightest text-foreground md:text-6xl lg:text-7xl">
            {HERO.title}
          </h1>
          <p className="mt-6 max-w-[560px] text-lg leading-relaxed text-muted md:text-xl">
            {HERO.subtitle}
          </p>
          <div className="mt-12 flex flex-wrap gap-4">
            <Button href={siteHash("demo")}>Live Demo</Button>
            <Button href={siteHash("early-access")} variant="secondary">
              Early Access →
            </Button>
          </div>
          <p className="mt-16 font-mono text-sm text-muted">{HERO.meta}</p>
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

      {/* 3. Engine */}
      <Section id="engine">
        <Container>
          <h2 className="text-3xl font-bold tracking-tighter">How Dino works</h2>
          <p className="mt-2 font-mono text-sm text-muted">
            pipeline → seal → export → proof_index.json → dashboard
          </p>
          <EngineFlow steps={FLOW} />
        </Container>
      </Section>

      {/* 4. USPs */}
      <Section id="capabilities">
        <Container>
          <UspList items={USPS} wide={USP_WIDE} />
        </Container>
      </Section>

      {/* 5. Demo walkthrough (primary) */}
      <Section id="demo">
        <Container narrow>
          <h2 className="text-3xl font-bold tracking-tighter">
            {DEMO_COPY.title}
          </h2>
          <p className="mt-2 text-muted">{DEMO_COPY.intro}</p>
          <div className="mt-12">
            <DemoWalkthrough steps={DEMO_STEPS} />
          </div>
          <p className="mt-8 font-mono text-xs text-muted">
            {DEMO_COPY.resultNote}{" "}
            <a
              href={`${GITHUB.base}/tree/main/tests/simulation`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent hover:underline"
            >
              make demo ↗
            </a>
          </p>
        </Container>
      </Section>

      {/* 6. Slow replay (secondary) */}
      <Section id="replay">
        <Container narrow>
          <p className="font-mono text-sm text-muted">{DEMO_COPY.replayLabel}</p>
          <p className="mt-2 text-sm text-muted">{DEMO_COPY.replayHint}</p>
          <div className="mt-8">
            <TerminalPlayer
              lines={DEMO_LINES}
              intervalMs={400}
              pauseOnComments
            />
          </div>
        </Container>
      </Section>

      {/* 7. Quickstart */}
      <Section id="quickstart">
        <Container narrow>
          <h2 className="text-3xl font-bold tracking-tighter">Quickstart</h2>
          <p className="mt-2 text-muted">Install. Seal. Export.</p>
          <div className="mt-10 overflow-x-auto border border-border bg-black p-6">
            <pre className="font-mono text-sm leading-relaxed text-foreground">
              <code>{QUICKSTART}</code>
            </pre>
          </div>
        </Container>
      </Section>

      {/* 8. Early Access */}
      <Section id="early-access">
        <Container className="grid grid-cols-1 gap-12 md:grid-cols-2 md:gap-16">
          <div>
            <MonoLabel accent>{EARLY.label}</MonoLabel>
            <h2 className="mt-4 text-3xl font-bold tracking-tighter">
              {EARLY.title}
            </h2>
            <p className="mt-4 leading-relaxed text-muted">{EARLY.body}</p>
            <div className="mt-8 space-y-2 font-mono text-sm text-muted">
              <p>→ 01. Email {EARLY.email}</p>
              <p>→ 02. Name your team / project</p>
              <p>→ 03. Receive a Team Key</p>
              <p>→ 04. Upgrade & start sealing</p>
            </div>
            <div className="mt-10 flex flex-wrap gap-4">
              <Button href={earlyAccessMailto()}>Request Team Key</Button>
              <Button href={GITHUB.base} variant="secondary" external>
                GitHub ↗
              </Button>
            </div>
          </div>
          <div className="flex flex-col justify-center gap-4 border border-border bg-black p-8 font-mono text-sm">
            <p className="text-muted">$ mail —subject &quot;Early Access Request&quot;</p>
            <p className="text-foreground">{EARLY.email}</p>
            <a
              href={earlyAccessMailto()}
              className="mt-2 inline-flex w-fit border border-border px-4 py-2 text-muted hover:border-accent hover:text-accent"
            >
              open mailto →
            </a>
          </div>
        </Container>
      </Section>

      <Footer />
    </div>
  );
}
