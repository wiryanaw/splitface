"use client";

import { useEffect, useState } from "react";
import { cx } from "@/utils/cx";
import { FACES } from "./faces";
import { Watch, still } from "./watch";

const INTERVAL = 2800;

// The big screen that flips through every face with a round wipe, like changing faces on the wrist
export function HeroWatch() {
  const [current, setCurrent] = useState(0);
  const [previous, setPrevious] = useState<number | null>(null);
  const [cycle, setCycle] = useState(0);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const timer = window.setInterval(() => {
      setCurrent((c) => {
        setPrevious(c);
        return (c + 1) % FACES.length;
      });
    }, INTERVAL);
    return () => window.clearInterval(timer);
  }, [cycle]);

  function show(index: number) {
    if (index === current) return;
    setPrevious(current);
    setCurrent(index);
    // Restart the timer so a picked face gets its full turn
    setCycle((n) => n + 1);
  }

  return (
    <div className="flex flex-col items-center gap-6">
      <Watch className="w-[min(420px,82vw)]">
        {previous !== null && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={still(FACES[previous].id)} alt="" className="absolute inset-0 size-full" />
        )}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          key={current}
          src={still(FACES[current].id)}
          alt={`${FACES[current].name} watch face`}
          className="landing-wipe absolute inset-0 size-full"
        />
      </Watch>
      <div className="flex items-baseline gap-3" aria-live="polite">
        <span className="font-mono text-caption-1-medium uppercase text-text-primary">Now showing</span>
        <span className="min-w-[9ch] text-title-3-bold">{FACES[current].name}</span>
      </div>
      <div className="flex gap-1.5" role="group" aria-label="Choose a face to preview">
        {FACES.map((face, i) => (
          <button
            key={face.id}
            type="button"
            aria-label={face.name}
            aria-current={i === current}
            onClick={() => show(i)}
            className={cx(
              "h-1 cursor-pointer rounded-full transition-[width,background-color] duration-150 ease-out",
              "outline-none focus-visible:ring-2 focus-visible:ring-border-focus-ring",
              i === current ? "w-8 bg-accent-500" : "w-4 bg-separator-border hover:bg-separator-border-strong",
            )}
          />
        ))}
      </div>
    </div>
  );
}
