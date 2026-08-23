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
            className={`flex w-full flex-col gap-2 border border-border bg-surface p-6 ${
              s.accent ? "" : "opacity-60"
            }`}
          >
            <span
              className={`font-mono text-sm ${
                s.accent ? "text-accent" : "text-muted"
              }`}
            >
              {s.step}
            </span>
            <p className="font-medium text-foreground">{s.title}</p>
            <p className="text-sm text-muted">{s.detail}</p>
          </div>
          {i < steps.length - 1 ? (
            <div
              className="hidden shrink-0 items-center px-2 text-2xl text-border md:flex"
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

/** Blueprint USP list — typography only, no icons */
export function UspList({
  items,
  wide,
}: {
  items: { label: string; title: string; body: string }[];
  wide: { label: string; title: string; body: string };
}) {
  return (
    <div className="mt-12 grid grid-cols-1 gap-x-16 gap-y-8 sm:grid-cols-2">
      {items.map((usp) => (
        <div key={usp.label}>
          <h3 className="font-mono text-sm text-accent">{usp.label}</h3>
          <p className="mt-1 font-medium text-foreground">{usp.title}</p>
          <p className="text-sm text-muted">{usp.body}</p>
        </div>
      ))}
      <div className="col-span-1 border-t border-border pt-8 sm:col-span-2">
        <h3 className="font-mono text-sm text-accent">{wide.label}</h3>
        <p className="mt-1 font-medium text-foreground">{wide.title}</p>
        <p className="text-sm text-muted">{wide.body}</p>
      </div>
    </div>
  );
}
