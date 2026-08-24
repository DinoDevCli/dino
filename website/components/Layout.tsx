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

/** Small orange section label — same on every block */
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
      className={`font-mono text-xs uppercase tracking-[0.16em] text-accent ${className}`}
    >
      {children}
    </Tag>
  );
}

/** Large title under Label — section size by default, hero only for product name */
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
      ? "text-3xl leading-[1.15] tracking-tight md:text-4xl"
      : size === "compact"
        ? "text-lg leading-snug tracking-tight md:text-xl"
        : "text-xl leading-snug tracking-tight md:text-2xl";
  return (
    <Tag className={`font-bold text-foreground ${scale} ${className}`}>
      {children}
    </Tag>
  );
}
