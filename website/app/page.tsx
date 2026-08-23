import { Button } from "@/components/Button";
import { DemoWalkthrough } from "@/components/DemoWalkthrough";
import { Footer } from "@/components/Footer";
import { Container, MonoLabel, Section } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { EngineFlow, UspList } from "@/components/Tiles";
import {
  DEMO_COPY,
  DEMO_STEPS,
  EARLY,
  FLOW,
  HERO,
  PROBLEM_SOLUTION,
  USPS,
} from "@/lib/content";
import { earlyAccessMailto } from "@/lib/site";

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav />

      {/* 1. Hero — documentary CLI */}
      <section className="relative isolate overflow-hidden">
        <div className="hero-grid absolute inset-0 -z-10" aria-hidden />
        <Container className="flex min-h-[65vh] flex-col items-start justify-center py-section">
          <div className="max-w-hero">
            <p className="mb-3 font-mono text-xs text-muted">{HERO.prompt}</p>
            <h1 className="text-4xl font-bold tracking-tight text-foreground md:text-5xl">
              {HERO.title}
            </h1>
            <p className="mt-4 text-lg text-muted">{HERO.subtitle}</p>
            <p className="mt-3 font-mono text-xs text-muted">{HERO.meta}</p>
          </div>
        </Container>
      </section>

      {/* 2. Problem / Context */}
      <Section id="problem">
        <Container className="grid grid-cols-1 gap-12 md:grid-cols-2 md:gap-20">
          <div>
            <MonoLabel>{PROBLEM_SOLUTION.problemLabel}</MonoLabel>
            <h2 className="mt-4 text-2xl font-bold tracking-tight md:text-3xl">
              {PROBLEM_SOLUTION.problemTitle}
            </h2>
            <p className="mt-4 leading-relaxed text-muted">
              {PROBLEM_SOLUTION.problemBody}
            </p>
          </div>
          <div>
            <MonoLabel accent>{PROBLEM_SOLUTION.solutionLabel}</MonoLabel>
            <h2 className="mt-4 text-2xl font-bold tracking-tight md:text-3xl">
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
          <h2 className="text-2xl font-bold tracking-tight md:text-3xl">
            Engine
          </h2>
          <p className="mt-2 font-mono text-xs text-muted">
            Seal → Export → Index → Dashboard
          </p>
          <EngineFlow steps={FLOW} />
        </Container>
      </Section>

      {/* 4. USPs */}
      <Section id="capabilities">
        <Container>
          <h2 className="text-2xl font-bold tracking-tight md:text-3xl">
            Spec
          </h2>
          <UspList items={USPS} />
        </Container>
      </Section>

      {/* 5. Demo walkthrough (primary) */}
      <Section id="demo">
        <Container narrow>
          <h2 className="text-2xl font-bold tracking-tight md:text-3xl">
            {DEMO_COPY.title}
          </h2>
          <p className="mt-2 text-muted">{DEMO_COPY.intro}</p>
          <div className="mt-12">
            <DemoWalkthrough steps={DEMO_STEPS} />
          </div>
          <p className="mt-8 font-mono text-xs text-muted">
            {DEMO_COPY.resultNote}
          </p>
        </Container>
      </Section>

      {/* 6. Early Access */}
      <Section id="early-access">
        <Container narrow>
          <MonoLabel accent>{EARLY.label}</MonoLabel>
          <h2 className="mt-4 text-2xl font-bold tracking-tight md:text-3xl">
            {EARLY.title}
          </h2>
          <p className="mt-4 leading-relaxed text-muted">{EARLY.body}</p>
          <div className="mt-8">
            <Button href={earlyAccessMailto()} variant="secondary">
              {EARLY.email}
            </Button>
          </div>
        </Container>
      </Section>

      <Footer />
    </div>
  );
}
