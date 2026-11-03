"use client";

import { Accordion, AccordionItem } from "@/components/base/accordion/accordion";

const STEPS = [
  {
    id: "connect",
    title: "1. Connect the watch",
    body: "Plug the watch into your computer with its charging cable. On a Mac, open a file transfer app such as OpenMTP; Windows shows the watch in File Explorer.",
  },
  {
    id: "copy",
    title: "2. Copy the file",
    body: "Pick your watch above the catalog so the Download button gives you the right file, then copy it into the GARMIN/APPS folder on the watch.",
  },
  {
    id: "pick",
    title: "3. Pick the face",
    body: "Unplug the watch. Hold UP on the watch face, choose Watch Face, then select the new face and press START.",
  },
];

// How to sideload a downloaded face; Connect IQ installs skip all of this
export function InstallGuide() {
  return (
    <section id="install" className="grid gap-10 border-t border-separator-border py-24 lg:grid-cols-[1fr_1.4fr]">
      <div className="flex flex-col gap-3">
        <span className="font-mono text-caption-1-medium uppercase text-text-secondary">Install guide</span>
        <h2 className="text-display-2-bold">Three steps from download to wrist.</h2>
        <p className="text-body-regular text-text-secondary">
          Only needed for downloads. Faces from Connect IQ install from the phone app, colors included.
        </p>
      </div>
      <div className="flex flex-col gap-6">
        <Accordion defaultExpandedKeys={["connect"]} className="w-full">
          {STEPS.map((step) => (
            <AccordionItem key={step.id} id={step.id} title={step.title}>
              <p>{step.body}</p>
            </AccordionItem>
          ))}
        </Accordion>
        <p className="rounded-2xl border border-dashed border-border-button-default p-5 text-body-regular text-text-secondary">
          Downloaded faces use their default colors, because settings are changed through the Connect IQ app. Install from
          Connect IQ to choose colors, cities and time zones.
        </p>
      </div>
    </section>
  );
}
