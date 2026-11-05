import { asset } from "./watch";

const NAV_LINK = "transition-colors duration-150 hover:text-text-primary";

// The header every page shares: the logo home, then links to the home page's sections and the privacy page
export function SiteHeader() {
  return (
    <header className="flex items-center justify-between border-b border-separator-border py-5">
      <a href={asset("/")} className="flex items-center gap-2.5">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={asset("/splitface-mark.png")} alt="" width={28} height={28} className="size-7" />
        <span className="text-title-3-bold">Splitface</span>
      </a>
      <nav className="flex items-center gap-6 font-mono text-caption-1-medium uppercase text-text-secondary">
        <a href={asset("/#faces")} className={NAV_LINK}>
          Faces
        </a>
        <a href={asset("/#install")} className={NAV_LINK}>
          Install
        </a>
        <a href={asset("/privacy/")} className={NAV_LINK}>
          Privacy
        </a>
      </nav>
    </header>
  );
}

// The footer every page shares; the bottom padding on phones leaves room for the floating tip button
export function SiteFooter() {
  return (
    <footer className="flex flex-wrap justify-between gap-3 border-t border-separator-border pt-8 pb-24 sm:pb-8 font-mono text-caption-1-medium uppercase text-text-secondary">
      <span>Splitface · Free Garmin watch faces</span>
      <span>
        Designed by{" "}
        <a
          href="https://wiryanaw.com/"
          target="_blank"
          rel="noopener"
          className="text-text-primary outline-none transition-colors duration-150 hover:text-accent-500 focus-visible:ring-2 focus-visible:ring-border-focus-ring"
        >
          Wiryana
        </a>{" "}
        · <a href={asset("/privacy/")} className={NAV_LINK}>Privacy</a> · © 2026
      </span>
    </footer>
  );
}
