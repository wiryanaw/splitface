"use client";

import { Accordion, AccordionItem } from "@/components/base/accordion/accordion";

// The watches every face supports (version 1.1.0), grouped by family. It mirrors the products
// in each face's manifest.xml, which WatchFaces/tools/set_products.py fills with every round
// AMOLED Garmin; sizes of one model are listed once.
const FAMILIES: { name: string; models: string[] }[] = [
  { name: "Forerunner", models: ["70", "165", "165 Music", "170", "170 Music", "265", "265S", "570", "965", "970"] },
  { name: "fēnix", models: ["8", "8 Pro", "9", "9 Pro", "E"] },
  { name: "Venu", models: ["2", "2 Plus", "2S", "3", "3S", "4"] },
  { name: "vívoactive", models: ["5", "6"] },
  { name: "epix", models: ["Gen 2", "Pro Gen 2"] },
  { name: "Instinct", models: ["3 AMOLED", "Crossover AMOLED"] },
  { name: "MARQ", models: ["Gen 2", "Aviator Gen 2", "Gen 3"] },
  { name: "quatix", models: ["7 Sapphire", "7 Pro", "8", "8 Pro"] },
  { name: "tactix", models: ["7 AMOLED", "8"] },
  { name: "Approach", models: ["S50", "S70", "S72"] },
  { name: "Descent", models: ["G2", "Mk3", "Mk3i"] },
  { name: "D2", models: ["Air X10", "Air X15", "Mach 1", "Mach 1 Pro", "Mach 2", "Mach 2 Pro"] },
];

// Which Garmin watches the faces run on: one quiet row that opens to the list
export function Compatible() {
  return (
    <Accordion className="border-t border-separator-border">
      <AccordionItem
        id="watches"
        title="Compatible watches"
        description="51 round AMOLED Garmin watches, every size. Open to check yours."
      >
        <dl className="grid grid-cols-2 gap-x-6 gap-y-5 pt-2 pb-4 sm:gap-x-10 lg:grid-cols-3">
          {FAMILIES.map((family) => (
            <div key={family.name} className="flex flex-col gap-1">
              <dt className="font-mono text-caption-1-medium uppercase text-text-tertiary">{family.name}</dt>
              <dd className="text-body-regular text-text-primary">{family.models.join(", ")}</dd>
            </div>
          ))}
        </dl>
      </AccordionItem>
    </Accordion>
  );
}
