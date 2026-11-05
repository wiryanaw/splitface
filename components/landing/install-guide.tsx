"use client";

import { RiDownloadLine, RiSmartphoneLine } from "@remixicon/react";
import { Chip } from "@/components/base/badges/chip";
import { Tab, TabList, TabPanel, Tabs } from "@/components/base/tabs/tabs";

interface Step {
  title: string;
  body: string;
}

const STORE_STEPS: Step[] = [
  {
    title: "Get the Connect IQ app",
    body: "Install the Connect IQ Store app on your phone (App Store or Google Play) and sign in with the Garmin account your watch is paired with.",
  },
  {
    title: "Install the face",
    body: "Tap Connect IQ on any face above to open its store page, or search for the face's name in the app, then tap Install. It syncs to your watch over Bluetooth.",
  },
  {
    title: "Pick it and make it yours",
    body: "On the watch, hold UP, choose Watch Face, select the new face and press START. To change its colors or cities, open the Connect IQ app, go to My Device, then My Watch Faces, and tap Settings.",
  },
];

const MANUAL_STEPS: Step[] = [
  {
    title: "Download the file",
    body: "Pick your watch above the catalog, then tap Download on a face. You get a .prg file made for the Forerunner 165 or the 165 Music.",
  },
  {
    title: "Copy it to the watch",
    body: "Plug the watch into your computer with its charging cable. On a Mac, open a file transfer app such as OpenMTP; Windows shows the watch in File Explorer. Copy the file into the GARMIN/APPS folder.",
  },
  {
    title: "Pick the face",
    body: "Unplug the watch. Hold UP on the watch face, choose Watch Face, then select the new face and press START.",
  },
];

function Steps({ steps }: { steps: Step[] }) {
  return (
    <ol className="grid gap-4 sm:grid-cols-3">
      {steps.map((step, i) => (
        <li
          key={step.title}
          className="flex flex-col gap-3 rounded-3xl border border-border-button-default bg-background-primary-default p-6"
        >
          <span className="text-display-4-bold text-accent-500">{i + 1}</span>
          <h3 className="text-title-3-bold">{step.title}</h3>
          <p className="text-body-regular text-text-secondary">{step.body}</p>
        </li>
      ))}
    </ol>
  );
}

// The two ways to get a face: from the Connect IQ Store, or as a file copied over USB
export function InstallGuide() {
  return (
    <section id="install" className="flex flex-col gap-10 border-t border-separator-border py-24">
      <div className="flex max-w-2xl flex-col gap-3">
        <span className="font-mono text-caption-1-medium uppercase text-text-secondary">Install guide</span>
        <h2 className="text-display-2-bold">Two ways to get a face on your wrist.</h2>
        <p className="text-body-regular text-text-secondary">
          The Connect IQ Store is the easiest: one tap, color settings, and updates when a face improves. Or download the
          file and copy it to your watch yourself.
        </p>
      </div>

      <Tabs defaultSelectedKey="store" className="flex flex-col gap-8">
        <TabList aria-label="How to install">
          <Tab id="store" icon={RiSmartphoneLine}>
            Connect IQ Store
          </Tab>
          <Tab id="manual" icon={RiDownloadLine}>
            Manual download
          </Tab>
        </TabList>

        <TabPanel id="store" className="flex flex-col gap-6 outline-none">
          <div className="flex flex-wrap items-center gap-2">
            <Chip variant="caption" color="orange">
              Recommended
            </Chip>
            <span className="text-body-regular text-text-secondary">Settings and updates included.</span>
          </div>
          <Steps steps={STORE_STEPS} />
        </TabPanel>

        <TabPanel id="manual" className="flex flex-col gap-6 outline-none">
          <Steps steps={MANUAL_STEPS} />
          <p className="rounded-2xl border border-dashed border-border-button-default p-5 text-body-regular text-text-secondary">
            Faces copied over by hand use their default colors and don&apos;t update on their own, because settings and
            updates come through the Connect IQ app. Install from the store to choose colors, cities and time zones.
          </p>
        </TabPanel>
      </Tabs>
    </section>
  );
}
