import type { CSSProperties } from "react";
import { RiCupLine } from "@remixicon/react";
import { ButtonLink } from "@/components/base/buttons/button";

export const TIP_URL = "https://trakteer.id/Wiryanaw";

// A small floating tip button in the corner; it opens Trakteer in a new tab
export function TipButton() {
  return (
    <div
      className="landing-rise fixed end-4 bottom-4 z-50 sm:end-6 sm:bottom-6"
      style={{ "--delay": "600ms" } as CSSProperties}
    >
      <ButtonLink
        href={TIP_URL}
        target="_blank"
        rel="noopener"
        leadingIcon={RiCupLine}
        className="rounded-full shadow-xl"
      >
        Buy me a coffee
      </ButtonLink>
    </div>
  );
}
