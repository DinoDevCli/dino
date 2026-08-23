/** Horizontal product core — diagram only */
export function ArchitectureFlow({
  flow,
  blocks,
}: {
  flow: string;
  blocks: { step: string; title: string; detail: string }[];
}) {
  return (
    <div className="mt-8">
      <p className="font-mono text-xs text-muted md:text-sm">{flow}</p>
      <div className="mt-8 flex flex-col gap-3 md:flex-row md:items-stretch md:gap-0">
        {blocks.map((b, i) => (
          <div key={b.step} className="flex min-w-0 flex-1 items-stretch">
            <div className="flex w-full flex-col gap-2 border border-border bg-background p-5">
              <span className="font-mono text-xs uppercase tracking-wider text-muted">
                {b.step}
              </span>
              <p className="font-mono text-sm text-foreground">{b.title}</p>
              <p className="font-mono text-xs text-muted">{b.detail}</p>
            </div>
            {i < blocks.length - 1 ? (
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
    </div>
  );
}
