import Link from "next/link";

type Variant = "primary" | "secondary" | "ghost";

const styles: Record<Variant, string> = {
  primary:
    "bg-accent text-white hover:bg-accent-hover border border-accent",
  secondary:
    "border border-border font-mono text-sm text-muted hover:border-foreground hover:text-foreground",
  ghost: "font-mono text-muted hover:text-foreground",
};

export function Button({
  href,
  children,
  variant = "primary",
  external = false,
}: {
  href: string;
  children: React.ReactNode;
  variant?: Variant;
  external?: boolean;
}) {
  const className = `inline-flex items-center justify-center px-5 py-2.5 text-sm transition ${styles[variant]}`;
  const useAnchor =
    external ||
    href.startsWith("mailto:") ||
    href.startsWith("http") ||
    href.startsWith("#") ||
    href.includes("/#");

  if (useAnchor) {
    return (
      <a
        href={href}
        className={className}
        target={href.startsWith("http") ? "_blank" : undefined}
        rel={href.startsWith("http") ? "noopener noreferrer" : undefined}
      >
        {children}
      </a>
    );
  }
  return (
    <Link href={href} className={className}>
      {children}
    </Link>
  );
}
