#!/bin/bash
# Build the site for GitHub Pages and publish out/ to the gh-pages branch.
# Usage: tools/publish.sh  (from the project folder)
set -e
cd "$(dirname "$0")/.."
export PATH="$HOME/.nvm/versions/node/v20.18.1/bin:$PATH"
BASE_PATH=/wrist-catalog npm run build
touch out/.nojekyll
cd out
git init -q -b gh-pages
git add -A
git commit -q -m "Publish the landing page"
git push -f "$(git -C .. remote get-url origin)" gh-pages
rm -rf .git
