export function EngineFlow({
  steps,
}: {
  steps: { icon: string; step: string; title: string; detail: string }[];
}) {
  return (
    <div className="mt-12 flex flex-col gap-4 md:flex-row md:items-stretch md:gap-0">
      {steps.map((s, i) => (
        <div
          key={s.step}
          className={`flex items-stretch md:min-w-0 ${
            i === 1 ? "md:mt-6 md:flex-[1.05]" : i === 3 ? "md:mt-3 md:flex-1" : "md:flex-1"
          }`}
        >
          <div className="flex w-full flex-col gap-2 border border-border bg-background p-5">
            <span className="text-base" aria-hidden>
              {s.icon}
            </span>
            <span className="font-mono text-xs uppercase tracking-wider text-accent">
              {s.step}
            </span>
            <p className="font-mono text-sm text-foreground">{s.title}</p>
            <p className="text-sm text-muted">{s.detail}</p>
          </div>
          {i < steps.length - 1 ? (
            <div
              className="hidden shrink-0 items-center px-2 font-mono text-muted md:flex"
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

export function UspList({
  items,
}: {
  items: { label: string; title: string; body: string }[];
}) {
  return (
    <div className="mt-12 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {items.map((usp, i) => (
        <div
          key={usp.label}
          className={`border border-border p-6 ${
            i === 4 ? "sm:col-span-2 lg:col-span-1 lg:col-start-2" : ""
          }`}
        >
          <h3 className="font-mono text-xs uppercase tracking-wider text-muted">
            {usp.label}
          </h3>
          <p className="mt-3 font-mono text-sm text-foreground">{usp.title}</p>
          <p className="mt-2 text-sm text-muted">{usp.body}</p>
        </div>
      ))}
    </div>
  );
}
