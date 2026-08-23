"use client";

import { useEffect, useRef } from "react";

/** Optional official asciinema embed when NEXT_PUBLIC_ASCIINEMA_ID is set. */
export function AsciinemaEmbed({ id }: { id: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.innerHTML = "";
    const script = document.createElement("script");
    script.src = `https://asciinema.org/a/${id}.js`;
    script.id = `asciicast-${id}`;
    script.async = true;
    el.appendChild(script);
  }, [id]);

  return (
    <div className="overflow-hidden border border-border-strong bg-code-bg">
      <div className="flex items-center gap-3 border-b border-border bg-surface px-4 py-3">
        <div className="flex gap-1.5" aria-hidden>
          <span className="h-2.5 w-2.5 rounded-full bg-[#3a3a42]" />
          <span className="h-2.5 w-2.5 rounded-full bg-[#3a3a42]" />
          <span className="h-2.5 w-2.5 rounded-full bg-[#3a3a42]" />
        </div>
        <span className="font-mono text-xs text-muted">asciinema · a/{id}</span>
      </div>
      <div ref={ref} className="min-h-[280px] p-2" />
      <p className="border-t border-border px-4 py-3 font-mono text-xs text-muted">
        <a
          href={`https://asciinema.org/a/${id}`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-accent hover:underline"
        >
          Open on asciinema.org →
        </a>
      </p>
    </div>
  );
}
