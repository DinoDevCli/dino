import { CodePanel } from "@/components/CodePanel";
import { Footer } from "@/components/Footer";
import { Nav } from "@/components/Nav";
import { CliShots } from "@/components/CliShots";
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
    <div className={`mx-auto w-full max-w-page px-gutter ${className}`}>
      {children}
    </div>
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

      <section className="hero-field section-y border-b border-border pt-8 md:pt-14">
        <Container>
          <p className="eyebrow">{HERO.eyebrow}</p>
          <div className="section-rule" aria-hidden />
          <h1 className="display mt-5 max-w-[20ch] text-[2rem] leading-[1.15] sm:text-5xl md:text-[3.25rem]">
            {HERO.title}
          </h1>
          <p className="mt-6 max-w-[36rem] text-base leading-relaxed text-text-muted sm:text-lg">
            {HERO.subhead}
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:flex-wrap">
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

          <div id="demo" className="mt-12 scroll-mt-24 md:mt-16">
            <CliShots />
          </div>
        </Container>
      </section>

      <section className="section-y border-b border-border">
        <Container className="max-w-content">
          <div className="space-y-5 text-base leading-relaxed text-text-muted sm:text-lg">
            {PROBLEM.paragraphs.map((p) => (
              <p key={p}>{p}</p>
            ))}
          </div>
        </Container>
      </section>

      <section className="section-y border-b border-border">
        <Container>
          <h2 className="display text-3xl md:text-4xl">{HOW.title}</h2>
          <ol className="mt-10 grid gap-0 sm:grid-cols-2 lg:grid-cols-4">
            {HOW.steps.map((step, i) => (
              <li
                key={step.label}
                className="border-t border-border py-6 pr-0 sm:border-t-0 sm:border-l sm:py-0 sm:pl-5 sm:pr-4 first:sm:border-l-0 first:sm:pl-0"
              >
                <p className="font-mono text-xs tracking-wider text-seal">
                  {String(i + 1).padStart(2, "0")}
                </p>
                <h3 className="mt-2 font-display text-xl text-text">
                  {step.label}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-text-muted">
                  <InlineCodeBits text={step.detail} />
                </p>
              </li>
            ))}
          </ol>
        </Container>
      </section>

      <section
        id="tiers"
        className="section-y border-b border-border scroll-mt-24"
      >
        <Container>
          <h2 className="display text-3xl md:text-4xl">{TIERS.title}</h2>
          <div className="mt-10 grid gap-8 md:grid-cols-2 md:gap-10">
            <div className="tier-col">
              <h3 className="font-display text-2xl text-text">
                {TIERS.free.header}
              </h3>
              <p className="mt-3 text-text-muted">{TIERS.free.subhead}</p>
              <ul className="mt-6 space-y-3 text-text">
                {TIERS.free.items.map((item) => (
                  <li key={item} className="flex gap-3 leading-relaxed">
                    <span className="mt-2 h-1 w-1 shrink-0 bg-text-muted" aria-hidden />
                    <span>
                      <InlineCodeBits text={item} />
                    </span>
                  </li>
                ))}
              </ul>
              <p className="mt-8 text-sm text-text-muted">{TIERS.free.footer}</p>
            </div>
            <div className="tier-col tier-col--pack">
              <h3 className="font-display text-2xl text-seal">
                {TIERS.pack.header}
              </h3>
              <p className="mt-3 text-text-muted">{TIERS.pack.subhead}</p>
              <ul className="mt-6 space-y-3 text-text">
                {TIERS.pack.items.map((item) => (
                  <li key={item} className="flex gap-3 leading-relaxed">
                    <span className="mt-2 h-1 w-1 shrink-0 bg-seal" aria-hidden />
                    <span>
                      <InlineCodeBits text={item} />
                    </span>
                  </li>
                ))}
              </ul>
              <p className="mt-8 text-sm text-text-muted">{TIERS.pack.footer}</p>
            </div>
          </div>
          <div className="mt-10">
            <a href={earlyAccessMailto()} className="btn-ghost">
              {TIERS.requestKey}
            </a>
          </div>
        </Container>
      </section>

      <section
        id="quickstart"
        className="section-y border-b border-border scroll-mt-24"
      >
        <Container>
          <h2 className="display text-3xl md:text-4xl">{QUICKSTART.title}</h2>
          <div className="mt-10 grid gap-6 md:grid-cols-2 md:gap-8">
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

      <section className="section-y border-b border-border">
        <Container className="max-w-content">
          <h2 className="display text-3xl md:text-4xl">{WHY.title}</h2>
          <div className="section-rule" aria-hidden />
          <div className="mt-6 space-y-3 text-base leading-relaxed text-text-muted sm:text-lg">
            {WHY.intro.map((line) => (
              <p key={line}>{line}</p>
            ))}
          </div>

          <p className="eyebrow mt-10">{WHY.captureLabel}</p>
          <dl className="why-grid mt-5">
            {WHY.items.map((item, i) => (
              <div key={item.label} className="why-item">
                <dt>
                  <span className="why-item__num" aria-hidden>
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <span className="why-item__label">{item.label}</span>
                </dt>
                <dd>{item.detail}</dd>
              </div>
            ))}
          </dl>

          <p className="why-close mt-10">{WHY.close}</p>
        </Container>
      </section>

      <section id="early-access" className="section-y scroll-mt-24">
        <Container>
          <div className="border border-seal/35 bg-surface px-5 py-10 sm:px-10 md:px-14 md:py-12">
            <h2 className="display text-3xl text-text">{EARLY.title}</h2>
            <p className="mt-4 max-w-xl text-text-muted">{EARLY.line}</p>
            <div className="mt-8">
              <a href={earlyAccessMailto()} className="btn-primary">
                {EARLY.button}
              </a>
            </div>
            <p className="mt-6 text-sm text-text-muted">{EARLY.note}</p>
          </div>
        </Container>
      </section>

      <Footer />
    </div>
  );
}
