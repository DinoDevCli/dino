import { Button } from "@/components/Button";
import { Footer } from "@/components/Footer";
import { Container, Heading, MonoLabel, Section } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { EngineFlow, Tile } from "@/components/Tiles";
import {
  FLOW,
  HERO,
  PROBLEM_SOLUTION,
  QUICKSTART,
  USPS,
} from "@/lib/content";
import { GITHUB } from "@/lib/site";

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav active="home" />

      {/* Hero */}
      <section className="relative isolate overflow-hidden">
        <div className="hero-grid absolute inset-0 -z-10" aria-hidden />
        <Container className="flex min-h-[75vh] flex-col items-start justify-center py-section">
          <MonoLabel accent>{HERO.badge}</MonoLabel>
          <Heading as="h1">
            <span className="mt-4 block text-foreground">{HERO.line1}</span>
            <span className="block text-accent">{HERO.line2}</span>
          </Heading>
          <p className="mt-6 max-w-[600px] text-xl leading-relaxed text-muted">
            {HERO.subtitle}
          </p>
          <div className="mt-12 flex flex-wrap gap-4">
            <Button href="/demo">▶ Live Demo</Button>
            <Button href="/early-access" variant="secondary">
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

      {/* Problem ↔ Solution */}
      <Section>
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

      {/* Engine flow */}
      <Section>
        <Container>
          <MonoLabel accent># engine</MonoLabel>
          <h2 className="mt-4 text-3xl font-bold tracking-tighter">
            How Dino works
          </h2>
          <p className="mt-2 font-mono text-sm text-muted">
            pipeline → seal → export → proof_index.json → dashboard
          </p>
          <EngineFlow steps={FLOW} />
        </Container>
      </Section>

      {/* USPs */}
      <Section>
        <Container>
          <MonoLabel accent># capabilities</MonoLabel>
          <h2 className="mt-4 text-3xl font-bold tracking-tighter">
            Technical surface
          </h2>
          <div className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {USPS.map((usp) => (
              <Tile
                key={usp.label}
                label={usp.label}
                title={usp.title}
                body={usp.body}
                icon={usp.icon}
              />
            ))}
          </div>
        </Container>
      </Section>

      {/* Quickstart teaser */}
      <Section>
        <Container narrow>
          <MonoLabel accent># quickstart</MonoLabel>
          <h2 className="mt-4 text-3xl font-bold tracking-tighter">
            Install. Seal. Export.
          </h2>
          <div className="mt-10 overflow-x-auto border border-border-strong bg-code-bg p-6">
            <pre className="font-mono text-sm leading-relaxed text-foreground">
              <code>{QUICKSTART}</code>
            </pre>
          </div>
          <div className="mt-8 flex flex-wrap gap-4">
            <Button href="/demo">Watch Live Demo</Button>
            <Button href="/early-access" variant="secondary">
              Request Early Access
            </Button>
          </div>
        </Container>
      </Section>

      <Footer />
    </div>
  );
}
