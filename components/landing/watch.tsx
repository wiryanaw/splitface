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

// Files in public/ need the site's base path (empty locally, /splitface on GitHub Pages)
export const asset = (path: string) => `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}${path}`;

// Where a face's images live: the still shown at rest, and the loop that plays on hover
export const still = (id: string) => asset(`/faces/${id}-still.webp`);
export const loop = (id: string) => asset(`/faces/${id}.webp`);
