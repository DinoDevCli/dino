import Link from "next/link";
import { Footer } from "@/components/Footer";
import { Nav } from "@/components/Nav";
import { Seal } from "@/components/Seal";
import { DOC_LINKS, TIERS } from "@/lib/content";
import { earlyAccessMailto, GITHUB } from "@/lib/site";

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-ink text-text">
      <Nav active="docs" />

      <main className="section-y">
        <div className="mx-auto max-w-page px-gutter">
          <p className="eyebrow">Documentation</p>
          <h1 className="display mt-4 text-3xl md:text-4xl">
            Engine, Proof Pack, contracts
          </h1>
          <p className="mt-5 max-w-content leading-relaxed text-text-muted">
            Same documents as the repository. Landing file:{" "}
            <a
              href={GITHUB.docsIndex}
              className="font-mono text-seal hover:text-seal-hover"
              target="_blank"
              rel="noopener noreferrer"
            >
              docs/index.md
            </a>
            .
          </p>

          <h2 className="display mt-14 text-2xl">{TIERS.title}</h2>
          <div className="mt-8 grid gap-8 md:grid-cols-2">
            <div>
              <h3 className="font-display text-xl">{TIERS.free.header}</h3>
              <p className="mt-2 text-sm text-text-muted">{TIERS.free.subhead}</p>
              <ul className="mt-4 space-y-2 text-sm text-text">
                {TIERS.free.items.map((item) => (
                  <li key={item} className="flex gap-2">
                    <Seal size={14} className="mt-1 shrink-0" muted />
                    <span>{item.replace(/`/g, "")}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="font-display text-xl text-seal">{TIERS.pack.header}</h3>
              <p className="mt-2 text-sm text-text-muted">{TIERS.pack.subhead}</p>
              <ul className="mt-4 space-y-2 text-sm text-text">
                {TIERS.pack.items.map((item) => (
                  <li key={item} className="flex gap-2">
                    <Seal size={14} className="mt-1 shrink-0" />
                    <span>{item.replace(/`/g, "")}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <p className="mt-8">
            <a href={earlyAccessMailto()} className="btn-ghost">
              {TIERS.requestKey}
            </a>
          </p>

          <ul className="mt-14 border-t border-border">
            {DOC_LINKS.map((doc) => (
              <li key={doc.path} className="border-b border-border">
                <a
                  href={`${GITHUB.base}/blob/main/${doc.path}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-baseline justify-between gap-6 py-5 hover:text-seal"
                >
                  <span className="font-medium">{doc.label}</span>
                  <span className="font-mono text-xs text-text-muted">{doc.path}</span>
                </a>
              </li>
            ))}
          </ul>

          <p className="mt-10 font-mono text-sm text-text-muted">
            <Link href="/" className="hover:text-seal">
              ← Home
            </Link>
          </p>
        </div>
      </main>

      <Footer />
    </div>
  );
}
