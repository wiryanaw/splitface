"use client";

import { useEffect, useState, type CSSProperties } from "react";
import { RiCupLine, RiSubtractLine } from "@remixicon/react";
import { Button, ButtonLink } from "@/components/base/buttons/button";

export const TIP_URL = "https://trakteer.id/Wiryanaw";
const MINIMIZED_KEY = "splitface-tip-minimized";

// A floating tip button in the corner; it opens Trakteer in a new tab.
// On phones a visitor can shrink it to a round icon, and that choice is remembered on their device.
export function TipButton() {
  const [minimized, setMinimized] = useState(false);

  useEffect(() => {
    try {
      setMinimized(localStorage.getItem(MINIMIZED_KEY) === "1");
    } catch {}
  }, []);

  function minimize() {
    setMinimized(true);
    try {
      localStorage.setItem(MINIMIZED_KEY, "1");
    } catch {}
  }

  const label = (
    <ButtonLink
      href={TIP_URL}
      target="_blank"
      rel="noopener"
      leadingIcon={RiCupLine}
      className={minimized ? "tip-shine rounded-full shadow-xl max-sm:hidden" : "tip-shine rounded-full shadow-xl"}
    >
      Buy me a coffee
    </ButtonLink>
  );

  return (
    <div
      className="landing-rise fixed end-4 bottom-4 z-50 sm:end-6 sm:bottom-6"
      style={{ "--delay": "600ms" } as CSSProperties}
    >
      {minimized ? (
        <>
          <ButtonLink
            href={TIP_URL}
            target="_blank"
            rel="noopener"
            iconOnly
            leadingIcon={RiCupLine}
            aria-label="Buy me a coffee"
            className="tip-shine size-12 rounded-full shadow-xl sm:hidden"
          />
          {label}
        </>
      ) : (
        <div className="relative">
          {label}
          <Button
            variant="secondary"
            size="xs"
            iconOnly
            leadingIcon={RiSubtractLine}
            aria-label="Minimize the tip button"
            onClick={minimize}
            className="absolute -end-2 -top-2 rounded-full shadow-md sm:hidden"
          />
        </div>
      )}
    </div>
  );
}
