import Link from "next/link";
import { GITHUB } from "@/lib/site";

export function Footer() {
  return (
    <footer className="border-t border-border py-10">
      <div className="mx-auto flex max-w-page flex-wrap items-center justify-center gap-x-4 gap-y-2 px-gutter font-mono text-xs text-text-muted">
        <span>MIT</span>
        <span aria-hidden>·</span>
        <span>Dino</span>
        <span aria-hidden>·</span>
        <a
          href={GITHUB.base}
          className="hover:text-seal"
          target="_blank"
          rel="noopener noreferrer"
        >
          GitHub
        </a>
        <span aria-hidden>·</span>
        <Link href="/docs" className="hover:text-seal">
          Docs
        </Link>
      </div>
    </footer>
  );
}
