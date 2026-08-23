/** Horizontal product core — engine blocks + consumer endpoint */
export function ArchitectureFlow({
  flow,
  blocks,
}: {
  flow: string;
  blocks: {
    step: string;
    title: string;
    detail: string;
    consumer?: boolean;
  }[];
}) {
  return (
    <div className="mt-10">
      <p className="overflow-x-auto font-mono text-xs text-muted md:text-sm">
        {flow}
      </p>
      <div className="mt-8 flex flex-col gap-3 lg:flex-row lg:items-stretch lg:gap-0">
        {blocks.map((b, i) => (
          <div
            key={b.step}
            className={`flex min-w-0 flex-1 items-stretch ${
              i === 1
                ? "lg:mt-5"
                : i === 3
                  ? "lg:mt-2"
                  : i === 4
                    ? "lg:mt-8"
                    : ""
            }`}
          >
            <div
              className={`flex w-full flex-col gap-2 border border-border p-5 ${
                b.consumer ? "bg-surface" : "bg-black"
              }`}
            >
              <span
                className={`font-mono text-[11px] uppercase tracking-[0.14em] ${
                  b.consumer ? "text-accent" : "text-muted"
                }`}
              >
                {b.step}
              </span>
              <p className="font-mono text-sm text-foreground">{b.title}</p>
              <p className="font-mono text-[11px] leading-relaxed text-muted">
                {b.detail}
              </p>
            </div>
            {i < blocks.length - 1 ? (
              <div
                className="hidden shrink-0 items-center px-1.5 font-mono text-sm text-muted lg:flex"
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
