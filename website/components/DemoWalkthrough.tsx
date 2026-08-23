import { DEMO_RESULT } from "@/lib/content";

export type DemoStep = {
  title: string;
  command: string;
  explanation: string;
  artifactExcerpt: string;
};

export function DemoWalkthrough({ steps }: { steps: DemoStep[] }) {
  return (
    <div className="mx-auto flex max-w-narrow flex-col gap-14">
      {steps.map((step) => (
        <div key={step.title} className="flex flex-col gap-4">
          <p className="font-mono text-xs text-muted"># {step.title}</p>
          <pre className="code-panel overflow-x-auto p-4 font-mono text-sm leading-relaxed text-foreground">
            <code>{step.command}</code>
          </pre>
          <p className="text-sm leading-relaxed text-muted">
            {renderExplanation(step.explanation)}
          </p>
          <pre className="json-panel overflow-x-auto p-4 font-mono text-xs leading-relaxed text-muted md:text-sm">
            <code>{step.artifactExcerpt}</code>
          </pre>
        </div>
      ))}

      <div className="border border-border bg-code-bg p-6">
        <p className="font-mono text-xs text-muted"># result</p>
        <p className="mt-3 font-mono text-lg text-foreground">
          <span className="text-accent">changed</span>: true
        </p>
        <p className="mt-2 font-mono text-sm text-muted">
          pipeline_version_diff: fraud_score_v1 → fraud_score_v2
        </p>
        <pre className="json-panel mt-6 overflow-x-auto p-4 font-mono text-xs leading-relaxed text-muted md:text-sm">
          <code>{DEMO_RESULT}</code>
        </pre>
      </div>
    </div>
  );
}

function renderExplanation(text: string) {
  const parts = text.split(
    /(`[^`]+`|\bproof_hash\b|\bchanged: true\b|\bproof\.json\b|\bproof_index\.json\b|\bpipeline_version_diff\b|\bEMPTY_SCAN_ROOTS\b)/g,
  );
  return parts.map((part, i) => {
    if (!part) return null;
    const isToken =
      (part.startsWith("`") && part.endsWith("`")) ||
      [
        "proof_hash",
        "changed: true",
        "proof.json",
        "proof_index.json",
        "pipeline_version_diff",
        "EMPTY_SCAN_ROOTS",
      ].includes(part);
    if (isToken) {
      const inner = part.startsWith("`") ? part.slice(1, -1) : part;
      return (
        <span key={i} className="font-mono text-foreground">
          {inner}
        </span>
      );
    }
    return <span key={i}>{part}</span>;
  });
}
