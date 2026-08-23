"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

type Props = {
  lines: string[];
  title?: string;
  /** Base ms per line; default 400 (~0.35× vs old 90ms) */
  intervalMs?: number;
  /** Extra linger on lines starting with # */
  pauseOnComments?: boolean;
};

export function TerminalPlayer({
  lines,
  title = "dino — replay",
  intervalMs = 400,
  pauseOnComments = true,
}: Props) {
  const [playing, setPlaying] = useState(false);
  const [cursor, setCursor] = useState(0);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const visible = useMemo(() => lines.slice(0, cursor), [lines, cursor]);
  const done = cursor >= lines.length;

  const clearTimer = useCallback(() => {
    if (timer.current) clearTimeout(timer.current);
    timer.current = null;
  }, []);

  const stop = useCallback(() => {
    clearTimer();
    setPlaying(false);
  }, [clearTimer]);

  const play = useCallback(() => {
    if (done) setCursor(0);
    setPlaying(true);
  }, [done]);

  useEffect(() => {
    if (!playing) return;

    const line = lines[cursor];
    const isComment = pauseOnComments && typeof line === "string" && line.trim().startsWith("#");
    const delay = isComment ? intervalMs * 2.2 : intervalMs;

    timer.current = setTimeout(() => {
      setCursor((c) => {
        if (c >= lines.length) {
          setPlaying(false);
          return c;
        }
        const next = c + 1;
        if (next >= lines.length) setPlaying(false);
        return next;
      });
    }, delay);

    return clearTimer;
  }, [playing, cursor, lines, intervalMs, pauseOnComments, clearTimer]);

  return (
    <div className="overflow-hidden border border-border bg-black">
      <div className="flex items-center gap-3 border-b border-border px-4 py-3">
        <span className="font-mono text-xs text-muted">{title}</span>
      </div>

      <div className="relative min-h-[280px] md:min-h-[360px]">
        <pre className="max-h-[360px] overflow-auto p-5 font-mono text-[13px] leading-relaxed text-foreground md:text-sm">
          <code>
            {visible.map((line, i) => (
              <span
                key={`${i}-${line.slice(0, 24)}`}
                className="block whitespace-pre-wrap"
              >
                {line.startsWith("$") ? (
                  <>
                    <span className="text-muted">$</span>
                    <span className="text-foreground">{line.slice(1)}</span>
                  </>
                ) : line.trim().startsWith("#") ? (
                  <span className="text-muted">{line}</span>
                ) : (
                  <span className="text-muted">{line}</span>
                )}
              </span>
            ))}
          </code>
        </pre>

        {!playing && cursor === 0 ? (
          <div className="absolute inset-0 flex items-center justify-center bg-black/80">
            <button
              type="button"
              onClick={play}
              className="border border-border px-6 py-3 font-mono text-xs uppercase tracking-wider text-muted hover:border-foreground hover:text-foreground"
            >
              ▶ Optional replay
            </button>
          </div>
        ) : null}
      </div>

      <div className="flex items-center justify-between border-t border-border px-4 py-3">
        <span className="font-mono text-xs text-muted">
          {done
            ? "complete"
            : playing
              ? `${cursor}/${lines.length}`
              : cursor > 0
                ? "paused"
                : "ready"}
        </span>
        <div className="flex gap-3">
          {cursor > 0 && !playing ? (
            <button
              type="button"
              onClick={play}
              className="font-mono text-xs uppercase tracking-wider text-muted hover:text-foreground"
            >
              Resume
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
