import { CodePanel } from "@/components/CodePanel";
import { Footer } from "@/components/Footer";
import { Nav } from "@/components/Nav";
import { Seal } from "@/components/Seal";
import { TerminalCard } from "@/components/TerminalCard";
import {
  EARLY,
  HERO,
  HOW,
  PROBLEM,
  QUICKSTART,
  TIERS,
  WHY,
} from "@/lib/content";
import { earlyAccessMailto, GITHUB, siteHash } from "@/lib/site";

function Container({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={`mx-auto max-w-page px-gutter ${className}`}>{children}</div>
  );
}

function InlineCodeBits({ text }: { text: string }) {
  const parts = text.split(/(`[^`]+`)/g);
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith("`") && part.endsWith("`")) {
          return (
            <code key={i} className="font-mono text-[0.92em] text-text">
              {part.slice(1, -1)}
            </code>
          );
        }
        return <span key={i}>{part}</span>;
      })}
    </>
  );
}

export default function Home() {
  return (
    <div className="min-h-screen bg-ink text-text">
      <Nav />

      {/* Hero */}
      <section className="section-y border-b border-border pt-10 md:pt-16">
        <Container>
          <p className="eyebrow">{HERO.eyebrow}</p>
          <h1 className="display mt-5 max-w-[22ch] text-[2.15rem] sm:text-5xl md:text-[3.35rem]">
            {HERO.title}
          </h1>
          <p className="mt-6 max-w-[38rem] text-lg leading-relaxed text-text-muted">
            {HERO.subhead}
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <a href={siteHash("quickstart")} className="btn-primary">
              {HERO.primaryCta}
            </a>
            <a
              href={GITHUB.base}
              className="btn-ghost"
              target="_blank"
              rel="noopener noreferrer"
            >
              {HERO.secondaryCta}
            </a>
          </div>

          <div id="demo" className="mt-14 scroll-mt-24">
            <TerminalCard />
          </div>
        </Container>
      </section>

      {/* Problem */}
      <section className="section-y border-b border-border">
        <Container className="max-w-content">
          <div className="space-y-4 text-lg leading-relaxed text-text-muted">
            {PROBLEM.paragraphs.map((p) => (
              <p key={p}>{p}</p>
            ))}
          </div>
        </Container>
      </section>

      {/* How it works */}
      <section className="section-y border-b border-border">
        <Container>
          <h2 className="display text-3xl md:text-4xl">{HOW.title}</h2>
          <ol className="mt-12 grid gap-8 md:grid-cols-4 md:gap-4">
            {HOW.steps.map((step, i) => (
              <li key={step.label} className="relative">
                <div className="flex items-center gap-2">
                  <Seal size={20} muted />
                  <span className="font-display text-xl text-text">{step.label}</span>
                </div>
                <p className="mt-3 text-sm leading-relaxed text-text-muted">
                  <InlineCodeBits text={step.detail} />
                </p>
                {i < HOW.steps.length - 1 ? (
                  <span
                    className="absolute right-0 top-2 hidden text-text-muted md:block"
                    aria-hidden
                  >
                    →
                  </span>
                ) : null}
              </li>
            ))}
          </ol>
        </Container>
      </section>

      {/* Free vs Proof Pack */}
      <section id="tiers" className="section-y border-b border-border scroll-mt-24">
        <Container>
          <h2 className="display text-3xl md:text-4xl">{TIERS.title}</h2>
          <div className="mt-12 grid gap-10 md:grid-cols-2 md:gap-12">
            <div>
              <h3 className="font-display text-2xl text-text">{TIERS.free.header}</h3>
              <p className="mt-3 text-text-muted">{TIERS.free.subhead}</p>
              <ul className="mt-6 space-y-3 text-text">
                {TIERS.free.items.map((item) => (
                  <li key={item} className="leading-relaxed">
                    <InlineCodeBits text={item} />
                  </li>
                ))}
              </ul>
              <p className="mt-8 text-sm text-text-muted">{TIERS.free.footer}</p>
            </div>
            <div>
              <h3 className="font-display text-2xl text-seal">{TIERS.pack.header}</h3>
              <p className="mt-3 text-text-muted">{TIERS.pack.subhead}</p>
              <ul className="mt-6 space-y-3 text-text">
                {TIERS.pack.items.map((item) => (
                  <li key={item} className="leading-relaxed">
                    <InlineCodeBits text={item} />
                  </li>
                ))}
              </ul>
              <p className="mt-8 text-sm text-text-muted">{TIERS.pack.footer}</p>
            </div>
          </div>
          <div className="mt-12 flex justify-center">
            <a href={earlyAccessMailto()} className="btn-ghost">
              {TIERS.requestKey}
            </a>
          </div>
        </Container>
      </section>

      {/* Quickstart */}
      <section id="quickstart" className="section-y border-b border-border scroll-mt-24">
        <Container>
          <h2 className="display text-3xl md:text-4xl">{QUICKSTART.title}</h2>
          <div className="mt-10 grid gap-8 md:grid-cols-2">
            <CodePanel
              label={QUICKSTART.free.label}
              code={QUICKSTART.free.code}
              note={QUICKSTART.free.note}
            />
            <CodePanel
              label={QUICKSTART.pack.label}
              code={QUICKSTART.pack.code}
              note="Request a Team Key:"
              noteHref="dinodevcli@gmail.com"
            />
          </div>
        </Container>
      </section>

      {/* Why Dino */}
      <section className="section-y border-b border-border">
        <Container className="max-w-content">
          <h2 className="display text-3xl md:text-4xl">{WHY.title}</h2>
          <p className="mt-5 text-lg leading-relaxed text-text-muted">{WHY.intro}</p>
          <ul className="mt-8 space-y-3">
            {WHY.seals.map((item) => (
              <li key={item} className="flex items-start gap-3 text-text">
                <Seal size={18} className="mt-1 shrink-0" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
          <p className="mt-8 text-text-muted">{WHY.close}</p>
        </Container>
      </section>

      {/* Early Access CTA */}
      <section id="early-access" className="section-y scroll-mt-24">
        <Container>
          <div className="mx-auto max-w-content border border-seal/40 bg-surface px-6 py-12 text-center md:px-12">
            <h2 className="display text-3xl text-text">{EARLY.title}</h2>
            <p className="mt-4 text-text-muted">{EARLY.line}</p>
            <a href={earlyAccessMailto()} className="btn-primary mt-8">
              {EARLY.button}
            </a>
            <p className="mt-6 text-sm text-text-muted">{EARLY.note}</p>
          </div>
        </Container>
      </section>

      <Footer />
    </div>
  );
}
