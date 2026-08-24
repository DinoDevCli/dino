export function Container({
  children,
  narrow = false,
  className = "",
}: {
  children: React.ReactNode;
  narrow?: boolean;
  className?: string;
}) {
  return (
    <div
      className={`mx-auto w-full px-gutter ${
        narrow ? "max-w-narrow" : "max-w-content"
      } ${className}`}
    >
      {children}
    </div>
  );
}

export function Section({
  id,
  children,
  className = "",
  bordered = true,
}: {
  id?: string;
  children: React.ReactNode;
  className?: string;
  bordered?: boolean;
}) {
  return (
    <section
      id={id}
      className={`py-section ${bordered ? "border-t border-border" : ""} ${className}`}
    >
      {children}
    </section>
  );
}

export function MonoLabel({
  children,
  accent = false,
}: {
  children: React.ReactNode;
  accent?: boolean;
}) {
  return (
    <span
      className={`font-mono text-sm tracking-wider ${
        accent ? "text-accent" : "text-muted"
      }`}
    >
      {children}
    </span>
  );
}

export function Label({
  children,
  as: Tag = "p",
  className = "",
}: {
  children: React.ReactNode;
  as?: "p" | "h1" | "h2" | "h3";
  className?: string;
}) {
  return (
    <Tag
      className={`font-mono text-sm text-accent ${className}`}
    >
      {children}
    </Tag>
  );
}

export function Display({
  children,
  as: Tag = "h2",
  size = "section",
  className = "",
}: {
  children: React.ReactNode;
  as?: "h1" | "h2" | "h3" | "p";
  size?: "hero" | "section" | "compact";
  className?: string;
}) {
  const scale =
    size === "hero"
      ? "text-4xl leading-[1.12] tracking-tightest md:text-5xl"
      : size === "compact"
        ? "text-xl leading-snug tracking-tight md:text-2xl"
        : "text-3xl leading-snug tracking-tight md:text-4xl";
  return (
    <Tag className={`font-bold text-foreground ${scale} ${className}`}>
      {children}
    </Tag>
  );
}
