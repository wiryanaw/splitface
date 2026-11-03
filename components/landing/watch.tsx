import type { CSSProperties, ReactNode } from "react";
import { cx } from "@/utils/cx";

// A face preview as the watch's round screen, with a hairline edge and a soft shadow
export function Watch({ children, className, style }: { children: ReactNode; className?: string; style?: CSSProperties }) {
  return (
    <div
      className={cx("relative aspect-square overflow-hidden rounded-full shadow-card ring-1 ring-border-button-default", className)}
      style={style}
    >
      {children}
    </div>
  );
}

// Where a face's images live: the still shown at rest, and the loop that plays on hover
export const still = (id: string) => `/faces/${id}-still.webp`;
export const loop = (id: string) => `/faces/${id}.webp`;
