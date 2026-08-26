"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Seal } from "@/components/Seal";
import { GITHUB, siteHash } from "@/lib/site";

type NavItem =
  | { kind: "hash"; href: string; label: string }
  | { kind: "internal"; href: string; label: string }
  | { kind: "external"; href: string; label: string };

const LINKS: NavItem[] = [
  { kind: "hash", href: siteHash("demo"), label: "Demo" },
  { kind: "hash", href: siteHash("tiers"), label: "Free vs Proof Pack" },
  { kind: "internal", href: "/docs", label: "Docs" },
  { kind: "external", href: GITHUB.base, label: "GitHub" },
];

export function Nav({ active: _active = "home" }: { active?: "home" | "docs" }) {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`sticky top-0 z-50 transition-colors ${
        scrolled
          ? "border-b border-border bg-surface/95 backdrop-blur-sm"
          : "border-b border-transparent bg-transparent"
      }`}
    >
      <nav
        className="mx-auto flex max-w-page items-center justify-between px-gutter py-4"
        aria-label="Primary"
      >
        <Link
          href="/"
          className="flex items-center gap-2 text-text hover:text-seal"
        >
          <Seal size={22} />
          <span className="font-display text-lg tracking-tight">Dino</span>
        </Link>
        <ul className="flex flex-wrap items-center justify-end gap-1 sm:gap-5">
          {LINKS.map((item) => {
            const className =
              "px-2 py-1 font-body text-sm text-text-muted hover:text-text";

            if (item.kind === "external") {
              return (
                <li key={item.label}>
                  <a
                    href={item.href}
                    className={className}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {item.label}
                  </a>
                </li>
              );
            }

            if (item.kind === "internal") {
              return (
                <li key={item.label}>
                  <Link href={item.href} className={className}>
                    {item.label}
                  </Link>
                </li>
              );
            }

            return (
              <li key={item.label}>
                <a href={item.href} className={className}>
                  {item.label}
                </a>
              </li>
            );
          })}
        </ul>
      </nav>
    </header>
  );
}
