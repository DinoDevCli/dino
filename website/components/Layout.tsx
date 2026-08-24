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

export function Heading({
  children,
  as: Tag = "h2",
  className = "",
}: {
  children: React.ReactNode;
  as?: "h1" | "h2" | "h3";
  className?: string;
}) {
  const size =
    Tag === "h1"
      ? "text-4xl md:text-5xl tracking-tightest leading-[1.1]"
      : Tag === "h2"
        ? "text-2xl tracking-tight"
        : "text-lg tracking-tight";
  return (
    <Tag className={`font-bold text-foreground ${size} ${className}`}>
      {children}
    </Tag>
  );
}
