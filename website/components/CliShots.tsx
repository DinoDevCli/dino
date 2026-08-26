"use client";

import { useCallback, useState } from "react";
import { CLI_SHOTS, CLI_SHOTS_CAPTION, type CliShot } from "@/lib/cliShots";

function accentBody(body: string, accents: string[] = []) {
  if (!accents.length) return body;
  const escaped = accents
    .slice()
    .sort((a, b) => b.length - a.length)
    .map((a) => a.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const re = new RegExp(`(${escaped.join("|")})`, "g");
  const parts = body.split(re);
  return parts.map((part, i) =>
    accents.includes(part) ? (
      <span key={i} className="text-seal">
        {part}
      </span>
    ) : (
      <span key={i}>{part}</span>
    ),
  );
}

function ShotPanel({ shot }: { shot: CliShot }) {
  return (
    <div className="certificate-frame">
      <div className="certificate-frame__doc">
        <header className="flex items-center justify-between gap-3 border-b border-border px-4 py-2.5">
          <p className="font-mono text-[11px] tracking-wide text-text-muted">
            {shot.title}
          </p>
          <span className="font-mono text-[10px] uppercase tracking-[0.16em] text-seal">
            sealed
          </span>
        </header>
        <div className="space-y-4 px-4 py-4">
          <pre className="overflow-x-auto whitespace-pre-wrap break-words font-mono text-[12px] leading-relaxed text-text sm:text-[13px]">
            <span className="text-seal">$ </span>
            {shot.command}
          </pre>
          <pre className="overflow-x-auto whitespace-pre-wrap break-words border-t border-border pt-4 font-mono text-[12px] leading-relaxed text-text-muted sm:text-[13px]">
            {accentBody(shot.body, shot.accents)}
          </pre>
        </div>
      </div>
    </div>
  );
}

export function CliShots() {
  const [active, setActive] = useState(0);
  const shot = CLI_SHOTS[active] ?? CLI_SHOTS[0];

  const select = useCallback((index: number) => {
    setActive(index);
  }, []);

  return (
    <figure className="mx-auto w-full max-w-[720px]">
      <div
        className="mb-3 flex flex-wrap gap-2"
        role="tablist"
        aria-label="CLI captures"
      >
        {CLI_SHOTS.map((item, index) => {
          const selected = index === active;
          return (
            <button
              key={item.id}
              type="button"
              role="tab"
              aria-selected={selected}
              id={`cli-tab-${item.id}`}
              aria-controls={`cli-panel-${item.id}`}
              onClick={() => select(index)}
              className={`border px-3 py-1.5 font-mono text-xs tracking-wide transition-colors ${
                selected
                  ? "border-seal bg-seal text-ink"
                  : "border-border text-text-muted hover:border-seal hover:text-seal"
              }`}
            >
              {item.tab}
            </button>
          );
        })}
      </div>

      <div
        role="tabpanel"
        id={`cli-panel-${shot.id}`}
        aria-labelledby={`cli-tab-${shot.id}`}
      >
        <ShotPanel shot={shot} />
      </div>

      <figcaption className="mt-3 text-center font-mono text-xs text-text-muted">
        {CLI_SHOTS_CAPTION}
      </figcaption>
    </figure>
  );
}
