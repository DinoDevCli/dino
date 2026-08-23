import Link from "next/link";
import { DOC_LINKS, SITE } from "@/lib/content";
import { GITHUB } from "@/lib/site";

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="border-b border-border py-8">
        <div className="mx-auto flex max-w-content items-center justify-between px-6">
          <Link
            href="/"
            className="font-mono text-sm uppercase tracking-wider hover:text-accent"
          >
            {SITE.brand}
          </Link>
          <Link href="/" className="font-mono text-sm text-muted hover:text-accent">
            ← Home
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-content px-6 py-24">
        <span className="font-mono text-sm text-accent"># docs</span>
        <h1 className="mt-4 text-3xl font-bold tracking-tighter md:text-4xl">
          Documentation
        </h1>
        <p className="mt-4 max-w-xl text-muted">
          Same documents as the repository — contracts, CLI, integration, simulation.
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
      </main>

      <footer className="border-t border-border py-12">
        <div className="mx-auto flex max-w-content justify-between px-6 text-sm text-muted">
          <span>{SITE.brand} — Local-First Audit Engine</span>
          <span>
            v{SITE.version} · Early Access · MIT
          </span>
        </div>
      </footer>
    </div>
  );
}
