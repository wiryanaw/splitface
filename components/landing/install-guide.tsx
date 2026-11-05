import { Compatible } from "./compatible";

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

// Getting a face from the Connect IQ Store, in three steps, then the watches it runs on
export function InstallGuide() {
  return (
    <section id="install" className="flex flex-col gap-10 border-t border-separator-border py-24">
      <div className="flex max-w-2xl flex-col gap-3">
        <span className="font-mono text-caption-1-medium uppercase text-text-secondary">Install guide</span>
        <h2 className="text-display-2-bold">Three steps to a new face.</h2>
        <p className="text-body-regular text-text-secondary">
          Every face is on the Connect IQ Store, with color settings and updates whenever a face improves.
        </p>
      </div>

      <ol className="grid gap-4 sm:grid-cols-3">
        {STORE_STEPS.map((step, i) => (
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

      <Compatible />
    </section>
  );
}
