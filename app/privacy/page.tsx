import type { Metadata } from "next";
import { SiteFooter, SiteHeader } from "@/components/landing/site-chrome";
import "@/styles/landing.css";

export const metadata: Metadata = {
  title: "Privacy · Splitface",
  description: "Splitface watch faces collect no data. They never go online, and everything they show stays on your watch.",
};

// One question per section. lead is set in bold as the start of the first paragraph.
const SECTIONS: { title: string; lead?: string; body: string[] }[] = [
  {
    title: "Information we collect",
    lead: "None.",
    body: [
      "Splitface collects no personal information, usage data, analytics, crash reports or device identifiers. The faces use no third party analytics, advertising or tracking services, and there are no accounts or sign in.",
    ],
  },
  {
    title: "Health and activity data",
    body: [
      "To show your day, the faces read your steps, step goal, heart rate, floors climbed and battery level from your watch. Pool Lanes also reads the distance of your most recent swim from your watch's activity history.",
      "This is read on the watch only to draw the face. It is never sent off your watch, never seen or stored by us, and never sold or shared.",
    ],
  },
  {
    title: "Location",
    body: [
      "The faces do not use GPS or your location. The cities and time zone in Flight Path are the ones you type into its settings.",
    ],
  },
  {
    title: "Internet access",
    body: [
      "The faces never connect to the internet. They request no permission to go online, so nothing they show can leave your watch.",
    ],
  },
  {
    title: "Settings and installation",
    body: [
      "The faces are installed through Garmin's Connect IQ Store. Your color and city choices are saved by the Connect IQ app as part of each face's settings; we can't see them. Your Garmin account, downloads and the store itself are covered by Garmin's privacy policy.",
    ],
  },
];

export default function Privacy() {
  return (
    <div className="mx-auto max-w-[1180px] px-4 sm:px-6">
      <SiteHeader />
      {/* Centered like the home page hero; the section text stays left aligned in the centered column for easy reading */}
      <main className="mx-auto flex max-w-2xl flex-col gap-10 pt-16 pb-20 lg:pt-24 lg:pb-24">
        <div className="flex flex-col items-center gap-4 text-center">
          <span className="font-mono text-eyebrow-medium uppercase text-accent-500">Privacy</span>
          <h1 className="max-w-[16ch] text-display-2-bold text-balance">We don&apos;t collect your data. At all.</h1>
          <span className="font-mono text-caption-1-medium uppercase text-text-tertiary">Last updated 5 November 2026</span>
        </div>

        <p className="rounded-3xl border border-border-button-default bg-background-secondary-default p-6 text-center text-body-regular text-balance text-text-secondary">
          <strong className="text-body-medium text-text-primary">
            Splitface does not collect, store, transmit or share any personal data.
          </strong>{" "}
          No accounts, no analytics, no ads and no tracking. Everything a face does happens on your watch.
        </p>

        <div className="flex flex-col gap-8">
          {SECTIONS.map((section) => (
            <section key={section.title} className="flex flex-col gap-3">
              <h2 className="text-title-2-bold">{section.title}</h2>
              {section.body.map((paragraph, i) => (
                <p key={paragraph.slice(0, 24)} className="text-body-regular text-text-secondary">
                  {i === 0 && section.lead && <strong className="text-body-medium text-text-primary">{section.lead} </strong>}
                  {paragraph}
                </p>
              ))}
            </section>
          ))}
        </div>
      </main>
      <SiteFooter />
    </div>
  );
}
