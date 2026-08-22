import Link from "next/link";
import { DOC_LINKS } from "@/lib/content";
import { GITHUB } from "@/lib/site";

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <p className="text-muted-foreground font-mono text-xs tracking-[0.2em] uppercase">
      {children}
    </p>
  );
}

export default function DocsPage() {
  return (
    <div className="min-h-screen">
      <header className="border-border border-b px-6 py-8 md:px-10">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <Link
            href="/"
            className="font-mono text-sm tracking-[0.3em] uppercase hover:opacity-80"
          >
            dino
          </Link>
          <Link
            href="/"
            className="text-muted-foreground font-mono text-xs tracking-[0.15em] uppercase hover:text-foreground"
          >
            ← Home
          </Link>
        </div>
      </header>

      <main className="px-6 py-20 md:px-10 md:py-28">
        <div className="mx-auto flex max-w-6xl flex-col gap-10">
          <div className="flex flex-col gap-4">
            <SectionLabel>Documentation</SectionLabel>
            <h1 className="text-3xl leading-tight tracking-tight md:text-4xl">
              Docs
            </h1>
            <p className="text-muted-foreground max-w-2xl text-sm leading-relaxed">
              Same documents as the repository — proof contract, CLI, examples.
            </p>
          </div>

          <ul className="border-border border-t">
            {DOC_LINKS.map((doc) => (
              <li key={doc.path} className="border-border border-b">
                <a
                  href={`${GITHUB.base}/blob/main/${doc.path}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-muted-foreground flex items-baseline justify-between gap-4 py-6 font-mono text-sm"
                >
                  <span>{doc.label}</span>
                  <span className="text-muted-foreground text-xs">↗</span>
                </a>
              </li>
            ))}
            <li className="border-border border-b">
              <a
                href={GITHUB.readme}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-muted-foreground flex items-baseline justify-between gap-4 py-6 font-mono text-sm"
              >
                <span>README</span>
                <span className="text-muted-foreground text-xs">↗</span>
              </a>
            </li>
          </ul>

          <div className="flex flex-wrap gap-3">
            <a
              href={GITHUB.base}
              target="_blank"
              rel="noopener noreferrer"
              className="border-foreground bg-foreground text-background hover:bg-foreground/90 border px-6 py-3 font-mono text-xs tracking-[0.15em] uppercase"
            >
              GitHub
            </a>
            <a
              href={`${GITHUB.base}#install`}
              target="_blank"
              rel="noopener noreferrer"
              className="border-border hover:border-foreground border px-6 py-3 font-mono text-xs tracking-[0.15em] uppercase"
            >
              Install
            </a>
          </div>
        </div>
      </main>
    </div>
  );
}
