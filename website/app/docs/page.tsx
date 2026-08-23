import Link from "next/link";
import { Footer } from "@/components/Footer";
import { Container, MonoLabel } from "@/components/Layout";
import { Nav } from "@/components/Nav";
import { DOC_LINKS } from "@/lib/content";
import { GITHUB } from "@/lib/site";

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav active="docs" />

      <main className="py-section">
        <Container>
          <MonoLabel accent># docs</MonoLabel>
          <h1 className="mt-4 text-4xl font-bold tracking-tightest">
            Documentation
          </h1>
          <p className="mt-4 max-w-xl text-muted">
            Same documents as the repository — contracts, CLI, integration,
            simulation.
          </p>

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
