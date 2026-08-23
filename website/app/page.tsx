import { Button } from "@/components/Button";
import { DemoWalkthrough } from "@/components/DemoWalkthrough";
import { Footer } from "@/components/Footer";
import { Container, MonoLabel, Section } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { ArchitectureFlow } from "@/components/Tiles";
import {
  ARCHITECTURE,
  DEMO_COPY,
  DEMO_STEPS,
  EARLY,
  HERO,
  HOW,
  PROBLEM,
} from "@/lib/content";
import { earlyAccessMailto } from "@/lib/site";

function MonoBody({ text }: { text: string }) {
  const parts = text.split(
    /(\bproof\.json\b|\bexport\.v1\b|\bproof_index\.json\b|\bchanged: true\/false\b|\bchanged: true\b|\bchanged: false\b)/g,
  );
  return (
    <>
      {parts.map((part, i) => {
        if (
          [
            "proof.json",
            "export.v1",
            "proof_index.json",
            "changed: true/false",
            "changed: true",
            "changed: false",
          ].includes(part)
        ) {
          return (
            <span key={i} className="font-mono text-foreground">
              {part}
            </span>
          );
        }
        return <span key={i}>{part}</span>;
      })}
    </>
  );
}

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav />

      {/* Identity */}
      <section className="relative isolate overflow-hidden">
        <div className="hero-grid absolute inset-0 -z-10" aria-hidden />
        <Container className="flex flex-col items-start justify-center py-16 md:py-20">
          <div className="max-w-hero">
            <p className="mb-3 font-mono text-xs text-muted">{HERO.prompt}</p>
            <h1 className="text-3xl font-bold tracking-tight text-foreground md:text-4xl">
              {HERO.title}
            </h1>
            <p className="mt-3 font-mono text-xs text-muted">{HERO.meta}</p>
          </div>
        </Container>
      </section>

      {/* 1. Problem */}
      <Section id="problem">
        <Container narrow>
          <MonoLabel>{PROBLEM.label}</MonoLabel>
          <div className="mt-4 space-y-1 text-lg leading-snug text-foreground md:text-xl">
            {PROBLEM.lines.map((line) => (
              <p key={line}>{line}</p>
            ))}
          </div>
        </Container>
      </Section>

      {/* 2. How — mechanics */}
      <Section id="how">
        <Container narrow>
          <MonoLabel>{HOW.label}</MonoLabel>
          <p className="mt-4 leading-relaxed text-muted">
            <MonoBody text={HOW.body} />
          </p>
        </Container>
      </Section>

      {/* 3. Architecture — product core */}
      <Section id="architecture">
        <Container>
          <MonoLabel>{ARCHITECTURE.label}</MonoLabel>
          <ArchitectureFlow
            flow={ARCHITECTURE.flow}
            blocks={ARCHITECTURE.blocks}
          />
        </Container>
      </Section>

      {/* 4. Demo */}
      <Section id="demo">
        <Container narrow>
          <h2 className="font-mono text-sm text-muted">{DEMO_COPY.title}</h2>
          <p className="mt-2 text-sm text-muted">{DEMO_COPY.intro}</p>
          <div className="mt-12">
            <DemoWalkthrough steps={DEMO_STEPS} />
          </div>
          <p className="mt-8 font-mono text-xs text-muted">
            {DEMO_COPY.resultNote}
          </p>
        </Container>
      </Section>

      {/* Early Access — unchanged below demo */}
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
