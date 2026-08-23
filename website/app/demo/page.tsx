import { Button } from "@/components/Button";
import { Footer } from "@/components/Footer";
import { Container, MonoLabel, Section } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { AsciinemaEmbed } from "@/components/AsciinemaEmbed";
import { TerminalPlayer } from "@/components/TerminalPlayer";
import { DEMO_LINES } from "@/lib/content";
import { GITHUB } from "@/lib/site";

const ASCIINEMA_ID = process.env.NEXT_PUBLIC_ASCIINEMA_ID?.trim() || "";

export default function DemoPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav active="demo" />

      <Section bordered={false}>
        <Container narrow>
          <MonoLabel accent># live demo</MonoLabel>
          <h1 className="mt-4 text-4xl font-bold tracking-tightest md:text-5xl">
            Live Demo
          </h1>
          <p className="mt-4 max-w-xl text-lg leading-relaxed text-muted">
            Two sealed fraud-score runs. One compare.{" "}
            <span className="text-foreground">changed: true</span> — the audit
            signal your CI or dashboard consumes.
          </p>
        </Container>
      </Section>

      <Section>
        <Container narrow>
          <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-xl font-bold tracking-tighter">
                Terminal session
              </h2>
              <p className="mt-1 font-mono text-xs text-muted">
                Run A seed-42 · Run B seed-123 · index compare
              </p>
            </div>
            <a
              href={`${GITHUB.base}/tree/main/tests/simulation`}
              target="_blank"
              rel="noopener noreferrer"
              className="font-mono text-xs text-accent hover:underline"
            >
              make demo ↗
            </a>
          </div>

          {ASCIINEMA_ID ? (
            <AsciinemaEmbed id={ASCIINEMA_ID} />
          ) : (
            <TerminalPlayer lines={DEMO_LINES} />
          )}

          <div className="mt-10 grid grid-cols-1 gap-4 border border-border bg-surface p-6 sm:grid-cols-3">
            <div>
              <p className="font-mono text-xs text-accent">Run A</p>
              <p className="mt-1 font-mono text-sm">fraud_score_v1</p>
              <p className="text-xs text-muted">seed-42</p>
            </div>
            <div>
              <p className="font-mono text-xs text-accent">Run B</p>
              <p className="mt-1 font-mono text-sm">fraud_score_v2</p>
              <p className="text-xs text-muted">seed-123</p>
            </div>
            <div>
              <p className="font-mono text-xs text-accent">Compare</p>
              <p className="mt-1 font-mono text-sm">pipeline_version_diff</p>
              <p className="text-xs text-muted">exit 1 · changed</p>
            </div>
          </div>

          <div className="mt-12 flex flex-wrap gap-4">
            <Button href="/early-access">Request Early Access →</Button>
            <Button href="/" variant="secondary">
              ← Product
            </Button>
          </div>
        </Container>
      </Section>

      <Footer />
    </div>
  );
}
