export function Tile({
  label,
  title,
  body,
  dimmed = false,
  icon,
}: {
  label: string;
  title: string;
  body: string;
  dimmed?: boolean;
  icon?: React.ReactNode;
}) {
  return (
    <div
      className={`flex flex-col gap-3 border border-border bg-surface p-6 ${
        dimmed ? "opacity-60" : ""
      }`}
    >
      <div className="flex items-center gap-3">
        {icon ? (
          <span className="flex h-8 w-8 items-center justify-center border border-border-strong font-mono text-xs text-accent">
            {icon}
          </span>
        ) : null}
        <span className="font-mono text-sm text-accent">{label}</span>
      </div>
      <p className="font-medium text-foreground">{title}</p>
      <p className="text-sm leading-relaxed text-muted">{body}</p>
    </div>
  );
}

export function EngineFlow({
  steps,
}: {
  steps: { step: string; title: string; detail: string; accent: boolean }[];
}) {
  return (
    <div className="mt-12 flex flex-col gap-3 md:flex-row md:items-stretch md:gap-0">
      {steps.map((s, i) => (
        <div key={s.step} className="flex flex-1 items-stretch md:min-w-0">
          <div
            className={`flex w-full flex-col gap-2 border border-border bg-surface p-5 ${
              s.accent ? "" : "opacity-55"
            }`}
          >
            <span
              className={`font-mono text-xs uppercase tracking-wider ${
                s.accent ? "text-accent" : "text-muted"
              }`}
            >
              {s.step}
            </span>
            <p className="font-mono text-sm font-medium text-foreground">
              {s.title}
            </p>
            <p className="text-xs text-muted">{s.detail}</p>
          </div>
          {i < steps.length - 1 ? (
            <div
              className="hidden shrink-0 items-center px-2 text-border-strong md:flex"
              aria-hidden
            >
              →
            </div>
          ) : null}
        </div>
      ))}
    </div>
  );
}
