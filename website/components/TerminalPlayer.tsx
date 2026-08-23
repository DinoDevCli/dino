"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

type Props = {
  lines: string[];
  title?: string;
};

export function TerminalPlayer({
  lines,
  title = "dino — fraud pipeline audit",
}: Props) {
  const [playing, setPlaying] = useState(false);
  const [cursor, setCursor] = useState(0);
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  const visible = useMemo(() => lines.slice(0, cursor), [lines, cursor]);
  const done = cursor >= lines.length;

  const stop = useCallback(() => {
    if (timer.current) clearInterval(timer.current);
    timer.current = null;
    setPlaying(false);
  }, []);

  const play = useCallback(() => {
    if (done) setCursor(0);
    setPlaying(true);
  }, [done]);

  useEffect(() => {
    if (!playing) return;
    timer.current = setInterval(() => {
      setCursor((c) => {
        if (c >= lines.length) {
          stop();
          return c;
        }
        return c + 1;
      });
    }, 90);
    return () => {
      if (timer.current) clearInterval(timer.current);
    };
  }, [playing, lines.length, stop]);

  return (
    <div className="overflow-hidden border border-border-strong bg-code-bg">
      <div className="flex items-center gap-3 border-b border-border bg-surface px-4 py-3">
        <div className="flex gap-1.5" aria-hidden>
          <span className="h-2.5 w-2.5 rounded-full bg-[#3a3a42]" />
          <span className="h-2.5 w-2.5 rounded-full bg-[#3a3a42]" />
          <span className="h-2.5 w-2.5 rounded-full bg-[#3a3a42]" />
        </div>
        <span className="font-mono text-xs text-muted">{title}</span>
      </div>

      <div className="relative min-h-[320px] md:min-h-[420px]">
        <pre className="max-h-[420px] overflow-auto p-5 font-mono text-[13px] leading-relaxed text-foreground md:text-sm">
          <code>
            {visible.map((line, i) => (
              <span key={`${i}-${line.slice(0, 24)}`} className="block whitespace-pre-wrap">
                {line.startsWith("$") ? (
                  <>
                    <span className="text-accent">$</span>
                    {line.slice(1)}
                  </>
                ) : (
                  <span className="text-muted">{line}</span>
                )}
              </span>
            ))}
            {playing && !done ? (
              <span className="ml-0.5 inline-block h-4 w-2 animate-pulse bg-accent align-middle" />
            ) : null}
          </code>
        </pre>

        {!playing && cursor === 0 ? (
          <div className="absolute inset-0 flex items-center justify-center bg-code-bg/75">
            <button
              type="button"
              onClick={play}
              className="flex items-center gap-3 border border-border-strong bg-surface px-8 py-4 font-mono text-sm uppercase tracking-wider text-foreground hover:border-accent hover:text-accent"
            >
              <span className="text-accent" aria-hidden>
                ▶
              </span>
              Play demo
            </button>
          </div>
        ) : null}
      </div>

      <div className="flex items-center justify-between border-t border-border px-4 py-3">
        <span className="font-mono text-xs text-muted">
          {done
            ? "complete"
            : playing
              ? `playing · ${cursor}/${lines.length}`
              : cursor > 0
                ? "paused"
                : "ready"}
        </span>
        <div className="flex gap-3">
          {cursor > 0 && !playing ? (
            <button
              type="button"
              onClick={play}
              className="font-mono text-xs uppercase tracking-wider text-accent hover:underline"
            >
              ▶ Resume
            </button>
          ) : null}
          {playing ? (
            <button
              type="button"
              onClick={stop}
              className="font-mono text-xs uppercase tracking-wider text-muted hover:text-foreground"
            >
              Pause
            </button>
          ) : null}
          {done || cursor > 0 ? (
            <button
              type="button"
              onClick={() => {
                stop();
                setCursor(0);
              }}
              className="font-mono text-xs uppercase tracking-wider text-muted hover:text-foreground"
            >
              Reset
            </button>
          ) : null}
        </div>
      </div>
    </div>
  );
}
