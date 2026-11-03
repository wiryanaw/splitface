import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // A static site: `npm run build` writes plain HTML, CSS and JS to out/ for any host
  output: "export",
  images: { unoptimized: true },
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
