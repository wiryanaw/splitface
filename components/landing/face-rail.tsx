import { FACES } from "./faces";
import { Watch, still } from "./watch";

// Every face drifting past in one endless row (the list is doubled so the loop is seamless)
export function FaceRail() {
  const row = [...FACES, ...FACES];
  return (
    <div className="relative overflow-hidden border-y border-separator-border py-8" aria-hidden>
      <div className="landing-rail flex w-max gap-8">
        {row.map((face, i) => (
          <Watch key={`${face.id}-${i}`} className="w-28 shrink-0">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={still(face.id)} alt="" loading="lazy" className="size-full" />
          </Watch>
        ))}
      </div>
      {/* Fade the row out at both edges */}
      <div className="pointer-events-none absolute inset-y-0 left-0 w-24 bg-linear-to-r from-background-full to-transparent" />
      <div className="pointer-events-none absolute inset-y-0 right-0 w-24 bg-linear-to-l from-background-full to-transparent" />
    </div>
  );
}
