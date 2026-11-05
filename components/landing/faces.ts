// The catalog. To publish a face on Connect IQ, paste its store page link into `store`;
// while it is empty the card shows "Connect IQ soon".
export interface Face {
  id: string;
  name: string;
  file: string;
  store: string;
  text: string;
  tags: string[];
  // Spans two columns on wide screens; pick featured faces so the grid ends on a full row of three
  featured?: boolean;
}

export const FACES: Face[] = [
  {
    id: "running-track",
    name: "Running Track",
    file: "RunningTrack",
    store: "https://apps.garmin.com/apps/64832ee9-d122-47be-8388-79e2a62d62f6",
    featured: true,
    text: "Your steps run a lap around a stadium track, from the start line to your goal.",
    tags: ["Steps", "Heart rate", "Battery", "Track colors"],
  },
  {
    id: "orbit",
    name: "Orbit",
    file: "Orbit",
    store: "https://apps.garmin.com/apps/65185275-f363-4d9b-8419-69ea7226631f",
    text: "The hour sun and the minute planet orbit the center while the outer ring fills with steps.",
    tags: ["Steps", "Heart rate", "Battery", "Date"],
  },
  {
    id: "topo-map",
    name: "Topo Map",
    file: "TopoMap",
    store: "https://apps.garmin.com/apps/69c908c5-4fc2-4b8d-9dba-3aaaac4898b1",
    text: "Contour lines climb to a goal marker that shows your daily step target.",
    tags: ["Step goal", "Heart rate", "Battery", "Map colors"],
  },
  {
    id: "liquid-battery",
    name: "Liquid Battery",
    file: "LiquidBattery",
    store: "https://apps.garmin.com/apps/fca880eb-8b10-4829-864c-3b6ef1791aa0",
    text: "The screen fills with liquid up to your battery level, and the type changes tone at the waterline.",
    tags: ["Battery level", "Steps", "Heart rate", "Date"],
  },
  {
    id: "oversize-type",
    name: "Oversize Type",
    file: "OversizeType",
    store: "https://apps.garmin.com/apps/aa9b0839-404b-4016-b293-3f32e7d02091",
    text: "Giant cropped numerals, minutes laid over the hour, with the round screen doing the cropping.",
    tags: ["Steps", "Battery", "Heart rate", "Hour colors"],
  },
  {
    id: "matchday",
    name: "Matchday",
    file: "Matchday",
    store: "https://apps.garmin.com/apps/5cf27847-a5c6-4e78-947d-d7791bcd1349",
    text: "Kick off on a striped pitch with the time on the scoreboard.",
    tags: ["Steps", "Heart rate", "Battery", "Pitch colors"],
  },
  {
    id: "pool-lanes",
    name: "Pool Lanes",
    file: "PoolLanes",
    store: "https://apps.garmin.com/apps/c8fe0a01-f8a7-4578-b011-a76a31626821",
    featured: true,
    text: "Lane ropes over sunlit water, with the distance of your latest swim.",
    tags: ["Last swim", "Steps", "Heart rate", "Water colors"],
  },
  {
    id: "race-bib",
    name: "Race Bib",
    file: "RaceBib",
    store: "https://apps.garmin.com/apps/c586bb35-ef06-419a-95ff-bad830ff0871",
    text: "A paper race bib pinned at a tilt, with every number tilted along with it.",
    tags: ["Steps", "Heart rate", "Battery", "Bib colors"],
  },
  {
    id: "summit",
    name: "Summit",
    file: "Summit",
    store: "https://apps.garmin.com/apps/9269827e-36fd-4054-a7ed-f7658d650576",
    text: "Your hiker climbs the trail as the day's steps add up, and plants the flag at your goal.",
    tags: ["Steps", "Floors climbed", "Heart rate", "Trail colors"],
  },
  {
    id: "flight-path",
    name: "Flight Path",
    file: "FlightPath",
    store: "https://apps.garmin.com/apps/faf54bc5-598c-48d1-9f70-79cb883a0305",
    text: "Home and destination times, with a plane flying the route as you walk.",
    tags: ["Two time zones", "Steps", "Heart rate", "Your cities"],
  },
];
