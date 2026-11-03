import type { Metadata } from "next";
import { Bricolage_Grotesque, IBM_Plex_Mono } from "next/font/google";
import "@/styles/globals.css";

// The theme reads its typeface from --font-display and code type from --font-mono-source
const display = Bricolage_Grotesque({
  variable: "--font-display",
  subsets: ["latin"],
  axes: ["opsz"],
});

const mono = IBM_Plex_Mono({
  variable: "--font-mono-source",
  subsets: ["latin"],
  weight: ["400", "500"],
});

// Where the site is published, for absolute links in social previews
const SITE = "https://wiryanaw.github.io/wrist-catalog";
const TITLE = "Splitface · Free Garmin watch faces";
const DESCRIPTION = "Free watch faces for the Garmin Forerunner 165 and 165 Music, for the run, the swim and the trip.";

export const metadata: Metadata = {
  metadataBase: new URL(SITE),
  title: TITLE,
  description: DESCRIPTION,
  openGraph: {
    type: "website",
    url: SITE,
    siteName: "Splitface",
    title: TITLE,
    description: DESCRIPTION,
    images: [{ url: `${SITE}/og.png`, width: 1200, height: 630, alt: "Splitface watch faces for the Garmin Forerunner 165" }],
  },
  twitter: {
    card: "summary_large_image",
    title: TITLE,
    description: DESCRIPTION,
    images: [`${SITE}/og.png`],
  },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`dark ${display.variable} ${mono.variable} h-full antialiased`}>
      <body className="min-h-full bg-background-full text-text-primary">{children}</body>
    </html>
  );
}
