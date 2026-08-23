import { Button } from "@/components/Button";
import { DemoWalkthrough } from "@/components/DemoWalkthrough";
import { Footer } from "@/components/Footer";
import { Container, MonoLabel, Section } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { ArchitectureFlow } from "@/components/Tiles";
import {
  DASHBOARD,
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
    /(\bproof_index\.json\b|\bcompare\.json\b|\bproof\.json\b|\bexport\.v1\b|\bchanged: true\/false\b|\bPath \/ HTTP \/ S3\b)/g,
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

      {/* Identity */}
      <section className="relative isolate overflow-hidden border-b border-border">
        <div className="hero-grid absolute inset-0 -z-10" aria-hidden />
        <Container className="flex min-h-[42vh] flex-col items-start justify-center py-20 md:py-28">
          <div className="max-w-hero">
            <p className="mb-4 font-mono text-xs text-muted">{HERO.prompt}</p>
            <h1 className="text-4xl font-bold leading-[1.12] tracking-tightest text-foreground md:text-5xl lg:text-6xl">
              {HERO.title}
            </h1>
            <p className="mt-5 font-mono text-xs text-muted">{HERO.meta}</p>
          </div>
        </Container>
      </section>

      {/* 1–2. Problem + How (paired layout) */}
      <Section id="problem" bordered={false}>
        <Container className="grid grid-cols-1 gap-14 border-t border-border pt-section md:grid-cols-2 md:gap-16">
          <div>
            <MonoLabel>{PROBLEM.label}</MonoLabel>
            <div className="mt-5 space-y-3 text-base leading-relaxed text-foreground md:text-lg">
              {PROBLEM.lines.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </div>
          </div>
          <div id="how">
            <MonoLabel>{HOW.label}</MonoLabel>
            <p className="mt-5 leading-relaxed text-muted">
              <MonoBody text={HOW.body} />
            </p>
          </div>
        </Container>
      </Section>

      {/* 3. Product Architecture */}
      <Section id="product">
        <Container>
          <MonoLabel>{PRODUCT.label}</MonoLabel>
          <h2 className="mt-3 text-2xl font-bold tracking-tight md:text-3xl">
            {PRODUCT.title}
          </h2>
          <div className="mt-5 max-w-narrow space-y-3 leading-relaxed text-muted">
            {PRODUCT.lines.map((line) => (
              <p key={line}>{line}</p>
            ))}
          </div>

          <ArchitectureFlow flow={PRODUCT.flow} blocks={PRODUCT.blocks} />

          <div className="mt-12 max-w-narrow border-l-2 border-accent pl-5">
            <div className="space-y-2 text-base leading-relaxed text-foreground">
              {PRODUCT.noDashboard.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </div>
            <p className="mt-5 font-mono text-xs text-muted md:text-sm">
              {PRODUCT.roles}
            </p>
          </div>
        </Container>
      </Section>

      {/* Dashboard Integration */}
      <Section id="dashboard">
        <Container narrow>
          <MonoLabel>{DASHBOARD.label}</MonoLabel>
          <h2 className="mt-3 text-2xl font-bold tracking-tight md:text-3xl">
            {DASHBOARD.title}
          </h2>
          <div className="mt-5 space-y-3 leading-relaxed text-muted">
            {DASHBOARD.lines.map((line) => (
              <p key={line}>
                <MonoBody text={line} />
              </p>
            ))}
          </div>
          <p className="mt-6 border border-border bg-black px-4 py-3 font-mono text-xs leading-relaxed text-muted md:text-sm">
            {DASHBOARD.example}
          </p>
        </Container>
      </Section>

      {/* 4. Demo */}
      <Section id="demo">
        <Container narrow>
          <h2 className="font-mono text-sm text-muted"># {DEMO_COPY.title}</h2>
          <p className="mt-2 text-sm text-muted">{DEMO_COPY.intro}</p>
          <div className="mt-12">
            <DemoWalkthrough steps={DEMO_STEPS} />
          </div>
          <p className="mt-8 font-mono text-xs text-muted">
            {DEMO_COPY.resultNote}
          </p>
          <p className="mt-3 text-sm text-muted">{DEMO_COPY.dashboardNote}</p>
        </Container>
      </Section>

      {/* Early Access */}
      <Section id="early-access">
        <Container className="grid grid-cols-1 gap-10 md:grid-cols-2 md:gap-16">
          <div>
            <MonoLabel accent>{EARLY.label}</MonoLabel>
            <h2 className="mt-4 text-2xl font-bold tracking-tight md:text-3xl">
              {EARLY.title}
            </h2>
            <p className="mt-4 leading-relaxed text-muted">{EARLY.body}</p>
            <p className="mt-4 font-mono text-xs leading-relaxed text-muted">
              {EARLY.note}
            </p>
            <div className="mt-8">
              <Button href={earlyAccessMailto()} variant="secondary">
                {EARLY.email}
              </Button>
            </div>
          </div>
          <div className="flex flex-col justify-center gap-3 border border-border bg-black p-8 font-mono text-sm">
            <p className="text-muted">$ scope</p>
            <p className="text-foreground">engine + artifacts</p>
            <p className="text-muted">dashboards = your team</p>
          </div>
        </Container>
      </Section>

      <Footer />
    </div>
  );
}
