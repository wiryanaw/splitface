// The catalog. To publish a face on Connect IQ, paste its store page link into `store`;
// while it is empty the card shows "Connect IQ soon".
export interface Face {
  id: string;
  name: string;
  file: string;
  store: string;
  text: string;
  tags: string[];
  // Spans two columns on wide screens; two featured faces keep the ten in full rows of three
  featured?: boolean;
}

export const FACES: Face[] = [
  {
    id: "running-track",
    name: "Running Track",
    file: "RunningTrack",
    store: "",
    featured: true,
    text: "Your steps run a lap around a stadium track, from the start line to your goal.",
    tags: ["Steps", "Heart rate", "Battery", "Track colors"],
  },
  {
    id: "orbit",
    name: "Orbit",
    file: "Orbit",
    store: "",
    text: "The hour sun and the minute planet orbit the center while the outer ring fills with steps.",
    tags: ["Steps", "Heart rate", "Battery", "Date"],
  },
  {
    id: "topo-map",
    name: "Topo Map",
    file: "TopoMap",
    store: "",
    text: "Contour lines climb to a goal marker that shows your daily step target.",
    tags: ["Step goal", "Heart rate", "Battery", "Map colors"],
  },
  {
    id: "liquid-battery",
    name: "Liquid Battery",
    file: "LiquidBattery",
    store: "",
    text: "The screen fills with liquid up to your battery level, and the type changes tone at the waterline.",
    tags: ["Battery level", "Steps", "Heart rate", "Date"],
  },
  {
    id: "oversize-type",
    name: "Oversize Type",
    file: "OversizeType",
    store: "",
    text: "Giant cropped numerals, minutes laid over the hour, with the round screen doing the cropping.",
    tags: ["Steps", "Battery", "Heart rate", "Hour colors"],
  },
  {
    id: "matchday",
    name: "Matchday",
    file: "Matchday",
    store: "",
    text: "Kick off on a striped pitch with the time on the scoreboard.",
    tags: ["Steps", "Heart rate", "Battery", "Pitch colors"],
  },
  {
    id: "pool-lanes",
    name: "Pool Lanes",
    file: "PoolLanes",
    store: "",
    featured: true,
    text: "Lane ropes over sunlit water, with the distance of your latest swim.",
    tags: ["Last swim", "Steps", "Heart rate", "Water colors"],
  },
  {
    id: "race-bib",
    name: "Race Bib",
    file: "RaceBib",
    store: "",
    text: "A paper race bib pinned at a tilt, with every number tilted along with it.",
    tags: ["Steps", "Heart rate", "Battery", "Bib colors"],
  },
  {
    id: "summit",
    name: "Summit",
    file: "Summit",
    store: "",
    text: "Your hiker climbs the trail as the day's steps add up, and plants the flag at your goal.",
    tags: ["Steps", "Floors climbed", "Heart rate", "Trail colors"],
  },
  {
    id: "flight-path",
    name: "Flight Path",
    file: "FlightPath",
    store: "",
    text: "Home and destination times, with a plane flying the route as you walk.",
    tags: ["Two time zones", "Steps", "Heart rate", "Your cities"],
  },
];

export const MODELS = [
  { id: "fr165", name: "Forerunner 165" },
  { id: "fr165m", name: "Forerunner 165 Music" },
] as const;

export type ModelId = (typeof MODELS)[number]["id"];
