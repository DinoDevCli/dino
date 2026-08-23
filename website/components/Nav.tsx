import Link from "next/link";
import { GITHUB, siteHash } from "@/lib/site";

type NavItem =
  | { kind: "route"; href: string; label: string }
  | { kind: "hash"; href: string; label: string }
  | { kind: "external"; href: string; label: string };

const LINKS: NavItem[] = [
  { kind: "route", href: "/", label: "Home" },
  { kind: "hash", href: siteHash("demo"), label: "Demo" },
  { kind: "hash", href: siteHash("early-access"), label: "Early Access" },
  { kind: "external", href: GITHUB.base, label: "GitHub" },
];

export function Nav({ active = "home" }: { active?: "home" | "docs" }) {
  return (
    <header className="relative z-20 border-b border-border bg-background/90">
      <nav
        className="mx-auto flex max-w-content items-center justify-between px-gutter py-5"
        aria-label="Primary"
      >
        <Link
          href="/"
          className="font-mono text-sm uppercase tracking-[0.25em] text-foreground hover:text-accent"
        >
          dino
        </Link>
        <ul className="flex items-center gap-1 sm:gap-6">
          {LINKS.map((item) => {
            const isActive = active === "home" && item.kind === "route";
            const className = `px-2 py-1 font-mono text-xs uppercase tracking-wider sm:text-sm ${
              isActive ? "text-accent" : "text-muted hover:text-foreground"
            }`;

            if (item.kind === "hash") {
              return (
                <li key={item.href}>
                  <a href={item.href} className={className}>
                    {item.label}
                  </a>
                </li>
              );
            }

            if (item.kind === "external") {
              return (
                <li key={item.href}>
                  <a
                    href={item.href}
                    className={className}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {item.label} ↗
                  </a>
                </li>
              );
            }

            return (
              <li key={item.href}>
                <Link href={item.href} className={className}>
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </header>
  );
}
