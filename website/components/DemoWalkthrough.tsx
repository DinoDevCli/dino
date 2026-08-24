export type DemoArtifact = {
  name: string;
  json: string;
  emphasize?: boolean;
};

export type DemoStep = {
  id: string;
  label: string;
  command: string;
  note?: string;
  artifacts: DemoArtifact[];
};

export function DemoWalkthrough({ steps }: { steps: DemoStep[] }) {
  return (
    <div className="mx-auto flex max-w-[800px] flex-col gap-16">
      {steps.map((step) => (
        <div key={step.id} className="flex flex-col gap-4">
          <p className="font-mono text-xs text-muted"># {step.label}</p>
          <pre className="overflow-x-auto border border-border bg-black p-4 font-mono text-sm leading-relaxed text-foreground">
            <code>{step.command}</code>
          </pre>
          {step.note ? (
            <p className="font-mono text-sm text-foreground">{step.note}</p>
          ) : null}
          {step.artifacts.map((art) => (
            <div key={art.name}>
              <p className="mb-2 font-mono text-[11px] uppercase tracking-[0.14em] text-muted">
                {art.name}
              </p>
              <pre className="overflow-x-auto border border-border bg-[#111118] p-4 font-mono text-xs leading-relaxed text-muted md:text-sm">
                <code>
                  {art.emphasize ? highlightCompare(art.json) : art.json}
                </code>
              </pre>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

function highlightCompare(json: string) {
  const parts = json.split(
    /("changed": true|"pipeline_version_diff")/g,
  );
  return parts.map((part, i) => {
    if (part === '"changed": true' || part === '"pipeline_version_diff"') {
      return (
        <span key={i} className="text-accent">
          {part}
        </span>
      );
    }
    return <span key={i}>{part}</span>;
  });
}
