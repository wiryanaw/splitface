#!/bin/bash
# Build the site for GitHub Pages and publish out/ to the gh-pages branch, as a new commit on
# top of what is already there (no force push).
# Usage: tools/publish.sh  (from the project folder). The next build clears out/ again.
set -e
cd "$(dirname "$0")/.."
export PATH="$HOME/.nvm/versions/node/v20.18.1/bin:$PATH"
REMOTE="$(git remote get-url origin)"
BASE_PATH=/wrist-catalog npm run build
touch out/.nojekyll
cd out
git init -q -b gh-pages
if git fetch -q "$REMOTE" gh-pages 2>/dev/null; then
    # Continue the published history so the push is a plain fast forward
    git reset -q --soft FETCH_HEAD
fi
git add -A
git commit -q -m "Publish the landing page"
git push "$REMOTE" gh-pages
