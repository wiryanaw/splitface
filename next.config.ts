import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // A static site: `npm run build` writes plain HTML, CSS and JS to out/ for any host
  output: "export",
  // Each page is folder/index.html, which GitHub Pages serves at /folder/ without a redirect race
  trailingSlash: true,
  images: { unoptimized: true },
  // Set BASE_PATH only when serving under a folder, like a github.io project URL
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
