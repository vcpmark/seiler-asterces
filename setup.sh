#!/usr/bin/env bash
# Creates the GitHub repo, pushes this folder, turns on GitHub Pages, and prints the live URL.
# Needs the GitHub CLI: https://cli.github.com  (brew install gh / winget install GitHub.cli)
#
#   ./setup.sh                 # repo name defaults to seiler-asterces
#   REPO=will ./setup.sh       # or pick your own
set -euo pipefail
cd "$(dirname "$0")"

REPO="${REPO:-seiler-asterces}"

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) not found. Install it from https://cli.github.com, or follow the manual steps in README.md." >&2
  exit 1
fi
gh auth status >/dev/null 2>&1 || gh auth login
OWNER="${OWNER:-$(gh api user -q .login)}"

# Fill in the absolute share-image URL now that we know the owner.
for f in index.html README.md; do
  sed -i.bak "s/__OWNER__/${OWNER}/g; s/__REPO__/${REPO}/g" "$f" && rm -f "$f.bak"
done

if [ ! -d .git ]; then
  git init -q
  git checkout -q -b main 2>/dev/null || git branch -M main
fi
git add -A
git commit -qm "Seiler Asterces — landing page" || true

if gh repo view "${OWNER}/${REPO}" >/dev/null 2>&1; then
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/${OWNER}/${REPO}.git"
  git push -u origin main
else
  gh repo create "${OWNER}/${REPO}" --public --source=. --remote=origin --push \
    --description "Seiler Asterces — where there is a Will there is a Way"
fi

# GitHub Pages: serve the main branch root.
PAGES_BODY='{"source":{"branch":"main","path":"/"}}'
if ! echo "$PAGES_BODY" | gh api -X POST "repos/${OWNER}/${REPO}/pages" --input - >/dev/null 2>&1; then
  echo "$PAGES_BODY" | gh api -X PUT "repos/${OWNER}/${REPO}/pages" --input - >/dev/null 2>&1 || true
fi

# First video sync (it also runs on every push and every 6 hours).
sleep 3
gh workflow run sync-videos.yml -R "${OWNER}/${REPO}" >/dev/null 2>&1 || true

echo
echo "Repo:  https://github.com/${OWNER}/${REPO}"
echo "Page:  https://${OWNER}.github.io/${REPO}/   (live in a minute or two; videos appear after the first sync run)"
