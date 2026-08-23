import { DemoWalkthrough } from "@/components/DemoWalkthrough";
import { Footer } from "@/components/Footer";
import { Container, MonoLabel, Section } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { ArchitectureFlow } from "@/components/Tiles";
import {
  DEMO_COPY,
  DEMO_STEPS,
  EARLY,
  HERO,
  HOW,
  PROBLEM,
  PRODUCT,
} from "@/lib/content";
import { earlyAccessMailto } from "@/lib/site";

function MonoBody({ text }: { text: string }) {
  const parts = text.split(
    /(\bproof_index\.json\b|\bcompare\.json\b|\bproof\.json\b|\bexport\.v1\b|\bchanged: true\/false\b|\bchanged: true\b|\bPath \/ HTTP \/ S3\b)/g,
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

      <section className="relative isolate overflow-hidden">
        <div className="hero-grid absolute inset-0 -z-10" aria-hidden />
        <Container className="flex min-h-[48vh] flex-col justify-center py-24 md:py-32">
          <p className="mb-5 font-mono text-xs text-accent">{HERO.prompt}</p>
          <h1 className="max-w-hero text-4xl font-bold leading-[1.1] tracking-tightest md:text-5xl lg:text-[3.4rem]">
            {HERO.title}
          </h1>
          <p className="mt-6 max-w-hero text-lg leading-relaxed text-foreground md:text-xl">
            <MonoBody text={HERO.definition} />
          </p>
          <p className="mt-4 font-mono text-xs text-muted">{HERO.meta}</p>
        </Container>
      </section>

      <Section id="problem">
        <Container narrow>
          <MonoLabel accent>{PROBLEM.label}</MonoLabel>
          <div className="mt-6 space-y-3 text-lg leading-snug text-foreground">
            {PROBLEM.lines.map((line) => (
              <p key={line}>{line}</p>
            ))}
          </div>
        </Container>
      </Section>

      <Section id="how">
        <Container narrow>
          <MonoLabel>{HOW.label}</MonoLabel>
          <p className="mt-6 text-base leading-relaxed text-muted">
            <MonoBody text={HOW.body} />
          </p>
        </Container>
      </Section>

      <Section id="product">
        <Container>
          <MonoLabel>{PRODUCT.label}</MonoLabel>
          <h2 className="mt-3 text-3xl font-bold tracking-tight">
            {PRODUCT.title}
          </h2>

          <ArchitectureFlow flow={PRODUCT.flow} blocks={PRODUCT.blocks} />

          <div className="mt-12 max-w-narrow">
            <p className="font-mono text-xs uppercase tracking-[0.14em] text-accent">
              {PRODUCT.wiringLabel}
            </p>
            <p className="mt-3 leading-relaxed text-foreground">
              <MonoBody text={PRODUCT.noDashboard} />
            </p>
            <p className="mt-2 font-mono text-sm text-muted">{PRODUCT.roles}</p>
            <div className="mt-6 space-y-2 text-sm leading-relaxed text-muted">
              {PRODUCT.wiring.map((line) => (
                <p key={line}>
                  <MonoBody text={line} />
                </p>
              ))}
            </div>
            <ul className="mt-8 space-y-2 border-t border-border pt-6">
              {PRODUCT.benefits.map((item) => (
                <li
                  key={item}
                  className="flex gap-3 font-mono text-sm text-muted"
                >
                  <span className="text-accent" aria-hidden>
                    →
                  </span>
                  <span>
                    <MonoBody text={item} />
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </Container>
      </Section>

      <Section id="demo">
        <Container narrow>
          <MonoLabel accent># {DEMO_COPY.title}</MonoLabel>
          <p className="mt-3 text-sm text-muted">{DEMO_COPY.intro}</p>
          <div className="mt-12">
            <DemoWalkthrough steps={DEMO_STEPS} />
          </div>
          <p className="mt-8 font-mono text-xs text-muted">
            {DEMO_COPY.resultNote}
          </p>
        </Container>
      </Section>

      <Section id="early-access">
        <Container narrow>
          <MonoLabel accent>{EARLY.label}</MonoLabel>
          <h2 className="mt-4 text-3xl font-bold tracking-tight">
            {EARLY.title}
          </h2>
          <ul className="mt-8 space-y-3">
            {EARLY.benefits.map((item) => (
              <li key={item} className="flex gap-3 text-muted">
                <span className="font-mono text-accent" aria-hidden>
                  →
                </span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
          <p className="mt-6 font-mono text-xs text-muted">{EARLY.note}</p>
          <a href={earlyAccessMailto()} className="mailto-cta mt-8">
            <span className="cta-label">{EARLY.cta}</span>
            <span className="cta-email">{EARLY.email}</span>
          </a>
        </Container>
      </Section>

      <Footer />
    </div>
  );
}
