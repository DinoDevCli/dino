import { DemoWalkthrough } from "@/components/DemoWalkthrough";
import { Footer } from "@/components/Footer";
import { Container, Display, Label, Section } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { ArchitectureFlow } from "@/components/Tiles";
import {
  CODESPACES,
  DEMO_COPY,
  DEMO_STEPS,
  EARLY,
  HERO,
  HOW,
  LICENSING,
  PROBLEM,
  PRODUCT,
  QUICKSTART,
  ROADMAP_DEV,
} from "@/lib/content";
import { earlyAccessMailto, GITHUB } from "@/lib/site";

function MonoBody({ text }: { text: string }) {
  const parts = text.split(
    /(\bproof_index\.json\b|\bcompare\.json\b|\bproof\.json\b|\bexport\.v1\b|\bchanged: true\/false\b|\bchanged: true\b|\bPath \/ HTTP \/ S3\b|\btests\/simulation\/golden\b|\bexamples\/superset\/drift_dashboard\.yaml\b|\b--dev\b)/g,
  );
  return (
    <>
      {parts.map((part, i) => {
        if (
          [
            "proof_index.json",
            "compare.json",
            "proof.json",
            "export.v1",
            "changed: true/false",
            "changed: true",
            "Path / HTTP / S3",
            "tests/simulation/golden",
            "examples/superset/drift_dashboard.yaml",
            "--dev",
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

      <section className="relative isolate overflow-hidden border-b border-border">
        <div className="hero-grid absolute inset-0 -z-10" aria-hidden />
        <Container className="flex min-h-[48vh] flex-col justify-center py-24 md:py-28">
          <Label>{HERO.kicker}</Label>
          <div className="hero-rule mt-4" aria-hidden />
          <Display as="h1" size="hero" className="mt-5">
            {HERO.title}
          </Display>
          <p className="mt-6 max-w-[36rem] leading-relaxed text-muted">
            <MonoBody text={HERO.definition} />
          </p>
          <Label as="h2" className="mt-14">
            {QUICKSTART.label}
          </Label>
          <div className="mt-4 border border-border border-l-2 border-l-accent bg-black px-4 py-3">
            <p className="overflow-x-auto font-mono text-sm text-foreground">
              {QUICKSTART.line}
            </p>
            <p className="mt-2 font-mono text-xs text-muted">{QUICKSTART.hint}</p>
          </div>
          <p className="mt-5 font-mono text-xs text-accent/80">{HERO.meta}</p>
        </Container>
      </section>

      <Section id="problem">
        <Container>
          <Label as="h2">{PROBLEM.title}</Label>
          <Display size="compact" className="mt-3">
            {PROBLEM.lead}
          </Display>
          <div className="mt-5 space-y-3 leading-relaxed text-muted">
            {PROBLEM.lines.map((line) => (
              <p key={line}>{line}</p>
            ))}
          </div>
        </Container>
      </Section>

      <Section id="how">
        <Container>
          <Label as="h2">{HOW.title}</Label>
          <Display size="compact" className="mt-3">
            {HOW.lead}
          </Display>
          <p className="mt-5 leading-relaxed text-muted">
            <MonoBody text={HOW.body} />
          </p>
        </Container>
      </Section>

      <Section id="engine">
        <Container>
          <Label as="h2">{PRODUCT.title}</Label>
          <Display as="p" size="compact" className="mt-3 font-mono">
            {PRODUCT.lead}
          </Display>
          <p className="mt-5 leading-relaxed text-muted">
            {PRODUCT.determinism}
          </p>
          <ArchitectureFlow blocks={PRODUCT.blocks} />
          <Label as="h3" className="mt-12">
            {PRODUCT.wiringTitle}
          </Label>
          <div className="mt-4 space-y-2 leading-relaxed text-muted">
            {PRODUCT.wiring.map((line) => (
              <p key={line}>
                <MonoBody text={line} />
              </p>
            ))}
          </div>
        </Container>
      </Section>

      <Section id="demo">
        <Container>
          <Label as="h2">{DEMO_COPY.title}</Label>
          <Display as="p" size="compact" className="mt-3">
            {DEMO_COPY.intro}
          </Display>
          <a
            href={GITHUB.codespaces}
            className="codespaces-btn mt-8"
            target="_blank"
            rel="noopener noreferrer"
          >
            {CODESPACES.cta}
          </a>
          <p className="mt-4 max-w-[36rem] text-sm leading-relaxed text-muted">
            {CODESPACES.body}
          </p>
          <div className="mt-12">
            <DemoWalkthrough steps={DEMO_STEPS} />
          </div>
          <p className="mt-8 text-sm leading-relaxed text-muted">
            <MonoBody text={ROADMAP_DEV} />
          </p>
          <p className="mt-12 font-mono text-xs text-muted">{DEMO_COPY.source}</p>
        </Container>
      </Section>

      <Section id="early-access">
        <Container>
          <div className="cta-panel">
            <Label as="h2">{EARLY.title}</Label>
            <Display size="compact" className="mt-3">
              {EARLY.subtitle}
            </Display>
            <p className="mt-5 leading-relaxed text-muted">{EARLY.flow}</p>
            <ol className="mt-6 space-y-2 text-sm leading-relaxed text-muted">
              {EARLY.steps.map((step, i) => (
                <li key={step} className="flex gap-3">
                  <span className="font-mono text-accent">{i + 1}.</span>
                  <span>{step}</span>
                </li>
              ))}
            </ol>
            <a href={earlyAccessMailto()} className="mailto-cta mt-10">
              <span className="cta-label">{EARLY.cta}</span>
              <span className="cta-email">{EARLY.email}</span>
            </a>
            <ul className="mt-8 space-y-2 text-sm text-muted">
              {EARLY.benefits.map((item) => (
                <li key={item}>— {item}</li>
              ))}
            </ul>
            <p className="mt-6 text-sm leading-relaxed text-muted">{EARLY.note}</p>
          </div>
        </Container>
      </Section>

      <Section id="licensing">
        <Container>
          <Label as="h2">{LICENSING.title}</Label>
          <Display size="compact" className="mt-3">
            {LICENSING.lead}
          </Display>
          <div className="mt-5 space-y-3 leading-relaxed text-muted">
            {LICENSING.lines.map((line) => (
              <p key={line}>{line}</p>
            ))}
          </div>
        </Container>
      </Section>

      <Footer />
    </div>
  );
}
