"use client";

import { useCallback, useState } from "react";

export function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const copy = useCallback(async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 2000);
  }, [text]);

  return (
    <button
      type="button"
      onClick={copy}
      className="border-border text-muted-foreground hover:border-foreground hover:text-foreground border px-3 py-1 font-mono text-[10px] tracking-[0.15em] uppercase"
    >
      {copied ? "Copied" : "Copy"}
    </button>
  );
}
