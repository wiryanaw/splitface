"use client";

import { useEffect, useRef, useState } from "react";
import { Focusable } from "react-aria-components";
import { RiDownloadLine, RiExternalLinkLine, RiPauseFill, RiPlayFill } from "@remixicon/react";
import { Button, ButtonLink } from "@/components/base/buttons/button";
import { Chip } from "@/components/base/badges/chip";
import { Tooltip, TooltipTrigger } from "@/components/base/tooltip/tooltip";
import type { Face, ModelId } from "./faces";
import { Watch, asset, loop, still } from "./watch";
import { cx } from "@/utils/cx";

export function FaceCard({ face, number, model }: { face: Face; number: number; model: ModelId }) {
  const ref = useRef<HTMLElement>(null);
  const [awake, setAwake] = useState(false);
  // Playing swaps the still for the looping preview, which restarts from its first frame
  const [playing, setPlaying] = useState(false);

  // The screen wakes once the card is a third of the way into view
  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setAwake(true);
          observer.disconnect();
        }
      },
      { threshold: 0.35 },
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  const PlayIcon = playing ? RiPauseFill : RiPlayFill;

  return (
    <article
      ref={ref}
      data-awake={awake}
      onPointerEnter={(e) => e.pointerType === "mouse" && setPlaying(true)}
      onPointerLeave={(e) => e.pointerType === "mouse" && setPlaying(false)}
      className={cx(
        "group relative flex flex-col gap-6 rounded-3xl border border-border-button-default bg-background-primary-default p-6 pt-14 shadow-card",
        face.featured && "lg:col-span-2 lg:flex-row lg:items-center lg:gap-10 lg:p-10",
      )}
    >
      <div className="absolute inset-x-6 top-6 flex justify-between font-mono text-caption-1-medium uppercase text-text-tertiary">
        <span>No. {String(number).padStart(2, "0")}</span>
        <span>{face.featured ? "Free · Featured" : "Free"}</span>
      </div>

      <div className={cx("flex flex-col items-center gap-4", face.featured && "lg:flex-1")}>
        {/* On a computer hovering the card plays it; on a touch screen tapping the screen plays or pauses */}
        <button
          type="button"
          onClick={() => setPlaying((p) => !p)}
          aria-pressed={playing}
          aria-label={`${playing ? "Pause" : "Play"} the ${face.name} preview`}
          className="cursor-pointer rounded-full outline-none focus-visible:ring-2 focus-visible:ring-border-focus-ring"
        >
          <Watch className={cx("w-[min(240px,64vw)]", face.featured && "lg:w-[320px]")}>
            <div className="landing-screen size-full" style={{ transitionDelay: `${(number % 3) * 120}ms` }}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={playing ? loop(face.id) : still(face.id)} alt={`${face.name} watch face`} className="size-full" />
            </div>
          </Watch>
        </button>
        <span
          aria-hidden
          className={cx(
            "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 font-mono text-caption-2-medium uppercase",
            "transition-colors duration-150 ease-out",
            playing
              ? "border-transparent bg-background-secondary-default text-text-primary"
              : "border-border-button-default text-text-secondary",
          )}
        >
          <PlayIcon className="size-3" />
          {playing ? (
            "Playing"
          ) : (
            <>
              <span className="hidden [@media(hover:hover)]:inline">Hover to play</span>
              <span className="[@media(hover:hover)]:hidden">Tap to play</span>
            </>
          )}
        </span>
      </div>

      <div className={cx("flex flex-col gap-6", face.featured ? "lg:flex-1" : "flex-1")}>
        <div className="flex flex-col gap-2">
          <h3 className={cx("text-title-2-bold", face.featured && "lg:text-display-4-bold")}>{face.name}</h3>
          <p className="text-body-regular text-text-secondary">{face.text}</p>
        </div>

        <div className="flex flex-wrap gap-1.5">
          {face.tags.map((tag) => (
            <Chip key={tag} variant="caption" color="gray">
              {tag}
            </Chip>
          ))}
        </div>

        <div className="mt-auto grid grid-cols-2 gap-2">
          {face.store ? (
            <ButtonLink href={face.store} target="_blank" rel="noopener" trailingIcon={RiExternalLinkLine}>
              Connect IQ
            </ButtonLink>
          ) : (
            <TooltipTrigger delay={0}>
              <Focusable>
                <Button variant="secondary" aria-disabled className="cursor-default opacity-60">
                  Connect IQ soon
                </Button>
              </Focusable>
              <Tooltip>Coming soon to the Connect IQ Store</Tooltip>
            </TooltipTrigger>
          )}
          <ButtonLink
            href={asset(`/downloads/${face.file}-${model}.prg`)}
            download
            variant={face.store ? "secondary" : "primary"}
            leadingIcon={RiDownloadLine}
          >
            Download
          </ButtonLink>
        </div>
      </div>
    </article>
  );
}
