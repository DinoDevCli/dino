"use client";

import { useEffect, useState } from "react";
import { DEMO } from "@/lib/content";
import { siteBasePath } from "@/lib/site";

function asset(path: string): string {
  const base = siteBasePath();
  return `${base}${path.startsWith("/") ? path : `/${path}`}`;
}

export function TerminalCard() {
  const [playing, setPlaying] = useState(true);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const apply = () => setPlaying(!mq.matches);
    apply();
    mq.addEventListener("change", apply);
    return () => mq.removeEventListener("change", apply);
  }, []);

  const gif = asset(DEMO.gifSrc);
  const poster = asset(DEMO.posterSrc);

  return (
    <figure className="mx-auto w-full max-w-[720px]">
      <div className="certificate-frame">
        <div className="certificate-frame__inner">
          {playing ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={gif}
              alt={DEMO.alt}
              width={960}
              height={540}
              className="h-full w-full object-cover"
            />
          ) : (
            <button
              type="button"
              onClick={() => setPlaying(true)}
              className="absolute inset-0 flex h-full w-full items-center justify-center bg-ink"
              aria-label="Play demo recording"
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={poster}
                alt=""
                width={960}
                height={540}
                className="absolute inset-0 h-full w-full object-cover opacity-70"
                aria-hidden
              />
              <span className="relative z-10 border border-seal bg-surface px-4 py-2 font-mono text-xs tracking-wide text-seal">
                Play
              </span>
            </button>
          )}
        </div>
      </div>
      <figcaption className="mt-3 text-center font-mono text-xs text-text-muted">
        {DEMO.caption}
      </figcaption>
    </figure>
  );
}
