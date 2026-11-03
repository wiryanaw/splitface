# Wrist Catalog landing page

Next.js + BoardUI, exported as a static site. Fonts: Bricolage Grotesque and IBM Plex Mono.

## Preview and build

Needs Node 20.18 or newer (`.nvmrc`):

```bash
nvm use && npm install && npm run build
```

`npm run build` writes the finished site to `out/`. Upload that folder to any static host
(Netlify, Vercel, GitHub Pages or your own server). For live editing, `npm run dev`.

## Publishing

Live at https://wiryanaw.github.io/wrist-catalog/ (GitHub Pages, served from the `gh-pages`
branch). After changing the page, commit as usual, then run `tools/publish.sh`: it builds with
the `/wrist-catalog` base path and pushes the result to `gh-pages` as a new commit. Pages
updates within a minute or two.

## Where things are

- `components/landing/faces.ts`: the ten faces. Paste a face's Connect IQ Store link into its
  `store` field and its card shows "Connect IQ" instead of "Connect IQ soon".
- `public/faces/`: the round previews. `public/downloads/`: the watch files.
- `public/bezel.png`: the watch case, from `tools/make_bezel.py`.
- `styles/landing.css`: the page's animations. BoardUI theme tokens are in `styles/theme.css`
  (accent ramp set to orange, type families to Bricolage Grotesque and IBM Plex Mono).

## BoardUI

`.mcp.json` registers the BoardUI MCP server for this project; open a new Claude Code session
here to use its tools. `AGENTS.md` and `.cursor/rules/` carry BoardUI's design rules.
`package.json` pins `magic-string` to 0.30 so the Tailwind loader runs on Node 20.18.
