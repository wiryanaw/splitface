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

export const metadata: Metadata = {
  title: "Wrist Catalog",
  description: "Ten free watch faces for the Garmin Forerunner 165 and 165 Music.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`dark ${display.variable} ${mono.variable} h-full antialiased`}>
      <body className="min-h-full bg-background-full text-text-primary">{children}</body>
    </html>
  );
}
