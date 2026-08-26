"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
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
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <header
      className={`sticky top-0 z-50 transition-colors ${
        scrolled || open
          ? "border-b border-border bg-ink/95 backdrop-blur-sm"
          : "border-b border-transparent bg-transparent"
      }`}
    >
      <nav
        className="mx-auto flex max-w-page items-center justify-between gap-4 px-gutter py-4"
        aria-label="Primary"
      >
        <Link
          href="/"
          className="shrink-0 font-display text-xl tracking-tight text-text hover:text-seal"
          onClick={() => setOpen(false)}
        >
          Dino
        </Link>

        <ul className="hidden items-center gap-6 md:flex">
          {LINKS.map((item) => (
            <li key={item.label}>
              <NavLink item={item} className="whitespace-nowrap font-body text-sm text-text-muted hover:text-text" />
            </li>
          ))}
        </ul>

        <button
          type="button"
          className="inline-flex items-center justify-center border border-border px-3 py-1.5 font-body text-sm text-text md:hidden"
          aria-expanded={open}
          aria-controls="mobile-nav"
          onClick={() => setOpen((v) => !v)}
        >
          {open ? "Close" : "Menu"}
        </button>
      </nav>

      {open ? (
        <ul
          id="mobile-nav"
          className="border-t border-border px-gutter py-3 md:hidden"
        >
          {LINKS.map((item) => (
            <li key={item.label} className="border-b border-border last:border-b-0">
              <NavLink
                item={item}
                className="block whitespace-nowrap py-3 font-body text-base text-text"
                onNavigate={() => setOpen(false)}
              />
            </li>
          ))}
        </ul>
      ) : null}
    </header>
  );
}

function NavLink({
  item,
  className,
  onNavigate,
}: {
  item: NavItem;
  className: string;
  onNavigate?: () => void;
}) {
  if (item.kind === "external") {
    return (
      <a
        href={item.href}
        className={className}
        target="_blank"
        rel="noopener noreferrer"
        onClick={onNavigate}
      >
        {item.label}
      </a>
    );
  }

  if (item.kind === "internal") {
    return (
      <Link href={item.href} className={className} onClick={onNavigate}>
        {item.label}
      </Link>
    );
  }

  return (
    <a href={item.href} className={className} onClick={onNavigate}>
      {item.label}
    </a>
  );
}
