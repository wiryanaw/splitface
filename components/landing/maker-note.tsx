import { asset } from "./watch";

// A short note about who made the faces, set large and quiet above the footer.
// The photo leads the name like a small tilted sticker, and straightens on hover.
export function MakerNote() {
  return (
    <section className="flex justify-center border-t border-separator-border py-20">
      <p className="max-w-[32ch] text-center text-display-4-medium text-balance text-text-secondary">
        Designed and built by{" "}
        <a
          href="https://wiryanaw.com/"
          target="_blank"
          rel="noopener"
          className="group inline-flex items-baseline gap-2 whitespace-nowrap rounded-md text-text-primary outline-none focus-visible:ring-2 focus-visible:ring-border-focus-ring"
        >
          <img
            src={asset("/wiryana.webp")}
            alt=""
            className="ms-1 size-10 -rotate-6 self-center rounded-lg border-2 border-text-primary object-cover shadow-card transition-transform duration-150 group-hover:rotate-0"
          />
          <span className="text-display-4-semibold transition-colors duration-150 group-hover:text-accent-500">
            Wiryana
          </span>
        </a>
        , a software designer who thinks a watch face deserves the same care as any screen you design.{" "}
        <span className="text-text-primary">More faces are on the way.</span>
      </p>
    </section>
  );
}
