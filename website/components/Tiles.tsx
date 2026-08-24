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
      <div className="mt-6 grid grid-cols-1 gap-px bg-border sm:grid-cols-2">
        {blocks.map((b) => (
          <div key={b.step} className="flex flex-col gap-2 bg-background p-5">
            <span className="font-mono text-[11px] uppercase tracking-[0.14em] text-muted">
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
