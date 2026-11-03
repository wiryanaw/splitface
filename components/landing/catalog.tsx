"use client";

import { useState } from "react";
import { SegmentedControl, SegmentedControlItem } from "@/components/base/segmented-control/segmented-control";
import { FACES, MODELS, type ModelId } from "./faces";
import { FaceCard } from "./face-card";

// The catalog grid, with one watch model picker that every Download button follows
export function Catalog() {
  const [model, setModel] = useState<ModelId>("fr165");

  return (
    <section id="faces" className="flex flex-col gap-10 py-24">
      <div className="flex flex-wrap items-end justify-between gap-6">
        <div className="flex max-w-xl flex-col gap-3">
          <span className="font-mono text-caption-1-medium uppercase text-text-secondary">The catalog</span>
          <h2 className="text-display-2-bold">Pick a face, any face.</h2>
          <p className="text-body-regular text-text-secondary">
            Hover a face to watch it move: steps fill the lap, the battery drains, the plane flies. Get it from Connect IQ
            for one tap installs and color settings, or download the file and copy it to your watch yourself.
          </p>
        </div>
        <div className="flex flex-col items-start gap-2">
          <span className="font-mono text-caption-1-medium uppercase text-text-tertiary">Your watch</span>
          <SegmentedControl
            aria-label="Your watch"
            selectedKeys={[model]}
            onSelectionChange={(keys) => {
              const [next] = [...keys];
              if (next) setModel(next as ModelId);
            }}
          >
            {MODELS.map((m) => (
              <SegmentedControlItem key={m.id} id={m.id}>
                {m.name}
              </SegmentedControlItem>
            ))}
          </SegmentedControl>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {FACES.map((face, i) => (
          <FaceCard key={face.id} face={face} number={i + 1} model={model} />
        ))}
      </div>
    </section>
  );
}
