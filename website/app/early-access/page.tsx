import { Button } from "@/components/Button";
import { Footer } from "@/components/Footer";
import { Container, MonoLabel, Section } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { EARLY } from "@/lib/content";
import { GITHUB, earlyAccessMailto } from "@/lib/site";

export default function EarlyAccessPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav active="early-access" />

      <Section bordered={false}>
        <Container>
          <div className="grid grid-cols-1 gap-12 md:grid-cols-2 md:gap-16">
            <div>
              <MonoLabel accent>{EARLY.label}</MonoLabel>
              <h1 className="mt-4 text-4xl font-bold tracking-tightest md:text-5xl">
                {EARLY.title}
              </h1>
              <p className="mt-6 leading-relaxed text-muted">{EARLY.body}</p>

              <div className="mt-10 space-y-3 font-mono text-sm text-muted">
                <p>
                  → 01. Email{" "}
                  <a
                    href={earlyAccessMailto()}
                    className="text-accent hover:underline"
                  >
                    {EARLY.email}
                  </a>
                </p>
                <p>→ 02. Name your team / project</p>
                <p>→ 03. Receive a Team Key</p>
                <p>
                  → 04.{" "}
                  <code className="text-foreground">
                    dino upgrade --pack proof --key …
                  </code>
                </p>
                <p>→ 05. Seal your first pipeline</p>
              </div>

              <div className="mt-10 flex flex-wrap gap-4">
                <Button href={earlyAccessMailto()} external>
                  {EARLY.email} →
                </Button>
                <Button href={GITHUB.earlyAccessIssue} variant="secondary" external>
                  GitHub Issue
                </Button>
              </div>
            </div>

            <div className="flex flex-col justify-center gap-6 border border-border bg-surface p-10 md:p-12">
              <div>
                <p className="font-mono text-xs text-accent">Free forever</p>
                <p className="mt-2 font-medium">Leakage scan</p>
                <p className="text-sm text-muted">MIT · no account · no cloud</p>
              </div>
              <div className="h-px bg-border" />
              <div>
                <p className="font-mono text-xs text-accent">Early Access · 60 days</p>
                <p className="mt-2 font-medium">Full Proof pack</p>
                <p className="text-sm text-muted">
                  proof · export · index · compare · metrics · layout
                </p>
              </div>
              <div className="h-px bg-border" />
              <a
                href={earlyAccessMailto()}
                className="text-2xl font-bold text-accent hover:underline"
              >
                {EARLY.email} →
              </a>
            </div>
          </div>
        </Container>
      </Section>

      <Section>
        <Container narrow>
          <MonoLabel># after unlock</MonoLabel>
          <div className="mt-8 overflow-x-auto border border-border-strong bg-code-bg p-6">
            <pre className="font-mono text-sm leading-relaxed text-foreground">
              <code>{`dino upgrade --pack proof --key YOUR_TEAM_KEY
dino proof doctor
dino proof run --command "python train.py" --scan ./src --export ./archive`}</code>
            </pre>
          </div>
          <div className="mt-8">
            <Button href="/demo" variant="secondary">
              See Live Demo →
            </Button>
          </div>
        </Container>
      </Section>

      <Footer />
    </div>
  );
}
