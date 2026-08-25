import Link from "next/link";
import { Footer } from "@/components/Footer";
import { Container, Display, Label } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { CLI_EARLY_ACCESS, CLI_GROUPS, DOC_LINKS, SUPPORT } from "@/lib/content";
import { GITHUB } from "@/lib/site";

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav active="docs" />

      <main className="py-section">
        <Container>
          <Label as="h1">Documentation</Label>
          <Display size="compact" className="mt-3">
            Engine, Proof Pack, contracts, Early Access
          </Display>
          <p className="mt-6 leading-relaxed text-muted">
            Same documents as the repository. Landing file:{" "}
            <a
              href={GITHUB.docsIndex}
              className="font-mono text-foreground hover:text-accent"
              target="_blank"
              rel="noopener noreferrer"
            >
              docs/index.md
            </a>
            .
          </p>

          <Label as="h2" className="mt-12">
            {CLI_GROUPS.title}
          </Label>
          <div className="mt-4 space-y-4 font-mono text-xs leading-relaxed text-muted">
            <div>
              <p className="text-foreground">Core Workflow</p>
              {CLI_GROUPS.core.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </div>
            <div>
              <p className="text-foreground">Pipeline Operations</p>
              {CLI_GROUPS.pipeline.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </div>
            <div>
              <p className="text-foreground">System & Packs</p>
              {CLI_GROUPS.system.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </div>
            <div>
              <p className="text-foreground">Notable forms</p>
              {CLI_GROUPS.forms.map((line) => (
                <p key={line}>{line}</p>
              ))}
            </div>
          </div>
          <pre className="mt-8 overflow-x-auto border border-border bg-black px-4 py-3 font-mono text-xs leading-relaxed text-muted whitespace-pre-wrap">
            {CLI_EARLY_ACCESS}
          </pre>

          <ul className="mt-12 border-t border-border">
            {DOC_LINKS.map((doc) => (
              <li key={doc.path} className="border-b border-border">
                <a
                  href={`${GITHUB.base}/blob/main/${doc.path}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-baseline justify-between gap-6 py-5 hover:text-accent"
                >
                  <span className="font-medium">{doc.label}</span>
                  <span className="font-mono text-xs text-muted">{doc.path}</span>
                </a>
              </li>
            ))}
          </ul>

          <p className="mt-10 leading-relaxed text-muted">
            {SUPPORT}{" "}
            <a
              href={GITHUB.issuesNew}
              className="text-foreground hover:text-accent"
              target="_blank"
              rel="noopener noreferrer"
            >
              Issue
            </a>
            {" · "}
            <a
              href={GITHUB.discussions}
              className="text-foreground hover:text-accent"
              target="_blank"
              rel="noopener noreferrer"
            >
              Discussion
            </a>
          </p>

          <p className="mt-10 font-mono text-sm text-muted">
            <Link href="/" className="hover:text-accent">
              ← Home
            </Link>
          </p>
        </Container>
      </main>

      <Footer />
    </div>
  );
}
