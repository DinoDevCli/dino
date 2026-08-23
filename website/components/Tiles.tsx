export function ArchitectureFlow({
  flow,
  blocks,
}: {
  flow: string;
  blocks: { step: string; title: string; detail: string }[];
}) {
  return (
    <div className="mt-10">
      <p className="font-mono text-xs text-accent/80 md:text-sm">{flow}</p>
      <div className="mt-6 grid grid-cols-1 gap-px bg-border sm:grid-cols-2 lg:grid-cols-4">
        {blocks.map((b) => (
          <div
            key={b.step}
            className="flex flex-col gap-2 bg-background p-5 sm:p-6"
          >
            <span className="font-mono text-[11px] uppercase tracking-[0.16em] text-accent">
              {b.step}
            </span>
            <p className="font-mono text-sm text-foreground">{b.title}</p>
            <p className="font-mono text-[11px] leading-relaxed text-muted">
              {b.detail}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
