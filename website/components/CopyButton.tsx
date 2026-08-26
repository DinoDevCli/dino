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
      className="border border-seal/40 px-2.5 py-1 font-mono text-[10px] uppercase tracking-[0.14em] text-seal hover:border-seal hover:bg-seal hover:text-ink"
    >
      {copied ? "Copied" : "Copy"}
    </button>
  );
}
