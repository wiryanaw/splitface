import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // A static site: `npm run build` writes plain HTML, CSS and JS to out/ for any host
  output: "export",
  images: { unoptimized: true },
  // GitHub Pages serves the site under /wrist-catalog; the deploy workflow sets BASE_PATH
  basePath: process.env.BASE_PATH || "",
  env: { NEXT_PUBLIC_BASE_PATH: process.env.BASE_PATH || "" },
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
