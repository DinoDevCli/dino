import Link from "next/link";

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/#demo", label: "Demo" },
  { href: "/#early-access", label: "Early Access" },
  { href: "/docs", label: "Docs" },
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
            const isActive =
              (active === "home" && item.href === "/") ||
              (active === "docs" && item.href === "/docs");
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`px-2 py-1 font-mono text-xs uppercase tracking-wider sm:text-sm ${
                    isActive
                      ? "text-accent"
                      : "text-muted hover:text-foreground"
                  }`}
                >
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
