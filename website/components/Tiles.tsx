export function ArchitectureFlow({
  blocks,
}: {
  blocks: { step: string; title: string; detail: string }[];
}) {
  return (
    <div className="mt-8 grid grid-cols-1 gap-px bg-border sm:grid-cols-2">
      {blocks.map((b) => (
        <div key={b.step} className="flex flex-col gap-2 bg-background p-5">
          <span className="font-mono text-sm text-accent">{b.step}</span>
          <p className="font-mono text-sm text-foreground">{b.title}</p>
          <p className="font-mono text-xs leading-relaxed text-muted">
            {b.detail}
          </p>
        </div>
      ))}
    </div>
  );
}
