import type { CSSProperties } from "react";
import { RiArrowDownLine } from "@remixicon/react";
import { ButtonLink } from "@/components/base/buttons/button";
import { Catalog } from "@/components/landing/catalog";
import { FaceRail } from "@/components/landing/face-rail";
import { HeroWatch } from "@/components/landing/hero-watch";
import { FACES } from "@/components/landing/faces";
import { InstallGuide } from "@/components/landing/install-guide";
import { TipButton } from "@/components/landing/tip-button";
import { MakerNote } from "@/components/landing/maker-note";
import { SiteFooter, SiteHeader } from "@/components/landing/site-chrome";
import "@/styles/landing.css";

const FACTS = [
  // The count follows the catalog, so it stays right as faces are added
  { value: String(FACES.length), label: "Faces" },
  { value: "$0", label: "Forever" },
  { value: "51", label: "Garmin watches" },
];

export default function Home() {
  return (
    <>
      <div className="mx-auto max-w-[1180px] px-4 sm:px-6">
        <SiteHeader />

        {/* Centered like a poster: label, headline, actions, then the big screen in a warm glow */}
        <section className="flex flex-col items-center gap-8 pt-16 pb-20 text-center lg:pt-24">
          <span className="landing-rise font-mono text-eyebrow-medium uppercase text-accent-500">
            51 Garmin watches<span className="hidden sm:inline"> · Watch faces</span>
          </span>
          <h1 className="landing-rise max-w-[18ch] text-hero-bold text-balance" style={{ "--delay": "80ms" } as CSSProperties}>
            Give your watch a better face.
          </h1>
          <p
            className="landing-rise max-w-[40ch] text-title-3-regular text-text-primary"
            style={{ "--delay": "160ms" } as CSSProperties}
          >
            Hand built Garmin watch faces with smooth type and colors you can make your own. Every one is free.
          </p>
          <div className="landing-rise flex flex-wrap justify-center gap-3" style={{ "--delay": "220ms" } as CSSProperties}>
            <ButtonLink href="#faces" trailingIcon={RiArrowDownLine} className="rounded-full">
              Browse the faces
            </ButtonLink>
            <ButtonLink href="#install" variant="secondary" className="rounded-full">
              How to install
            </ButtonLink>
          </div>

          <div className="landing-rise relative mt-6" style={{ "--delay": "300ms" } as CSSProperties}>
            <div className="landing-glow pointer-events-none absolute -inset-[45%]" aria-hidden />
            <div className="relative">
              <HeroWatch />
            </div>
          </div>

          <dl className="landing-rise mt-4 grid w-full max-w-md grid-cols-3" style={{ "--delay": "360ms" } as CSSProperties}>
            {FACTS.map((fact) => (
              <div key={fact.label} className="flex flex-col items-center gap-1">
                <dt className="order-2 font-mono text-caption-1-medium uppercase text-text-primary">{fact.label}</dt>
                <dd className="text-title-1-bold">{fact.value}</dd>
              </div>
            ))}
          </dl>
        </section>
      </div>

      <FaceRail />

      <div className="mx-auto max-w-[1180px] px-4 sm:px-6">
        <Catalog />
        <InstallGuide />
        <MakerNote />
        <TipButton />
        <SiteFooter />
      </div>
    </>
  );
}
