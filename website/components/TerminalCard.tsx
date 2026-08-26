"use client";

import { useEffect, useRef, useState } from "react";
import { DEMO } from "@/lib/content";
import { siteBasePath } from "@/lib/site";
import { Seal } from "@/components/Seal";

function asset(path: string): string {
  const base = siteBasePath();
  return `${base}${path.startsWith("/") ? path : `/${path}`}`;
}

export function TerminalCard() {
  const frameRef = useRef<HTMLDivElement>(null);
  const [inView, setInView] = useState(false);
  const [reduceMotion, setReduceMotion] = useState(false);
  const [playing, setPlaying] = useState(true);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    const apply = () => {
      setReduceMotion(mq.matches);
      setPlaying(!mq.matches);
    };
    apply();
    mq.addEventListener("change", apply);
    return () => mq.removeEventListener("change", apply);
  }, []);

  useEffect(() => {
    const el = frameRef.current;
    if (!el) return;
    const io = new IntersectionObserver(
      ([entry]) => {
        if (entry?.isIntersecting) {
          setInView(true);
          io.disconnect();
        }
      },
      { threshold: 0.35 },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  const gif = asset(DEMO.gifSrc);
  const poster = asset(DEMO.posterSrc);

  return (
    <div className="mx-auto w-full max-w-[720px]">
      <div className="certificate-frame">
        <div ref={frameRef} className="certificate-frame__inner">
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
              <span className="relative z-10 flex h-14 w-14 items-center justify-center rounded-full border border-seal bg-surface/90 text-seal">
                ▶
              </span>
            </button>
          )}

          <div className="pointer-events-none absolute bottom-3 right-3 flex items-center gap-2 rounded bg-ink/80 px-2.5 py-1.5 font-mono text-[10px] tracking-wide text-text">
            <Seal size={18} stamp stamped={inView && !reduceMotion} />
            <span>
              <span className="text-aligned">PROOF_PARTIAL</span>
              {" · "}
              <span className="text-drift">changed: true</span>
            </span>
          </div>
        </div>
      </div>
      <p className="mt-3 text-center font-mono text-xs text-text-muted">
        {DEMO.caption}
      </p>
    </div>
  );
}
