#!/usr/bin/env bash
# Publishing pipeline for oddesyconsultingandservices.com
#
#   scripts/publish.sh check [new-post-slug ...]   validate posts, build site, check built pages
#   scripts/publish.sh deploy                      push main, then publish public/ to the gh-pages branch
#
# Commit your changes between "check" and "deploy".
set -euo pipefail
cd "$(dirname "$0")/.."
REPO_URL="https://github.com/crasyforu-6666/oddesy-website"

retry() { local n=0; until "$@"; do n=$((n+1)); [ $n -ge 4 ] && return 1; sleep $((2**n)); done; }

case "${1:-}" in
  check)
    shift
    python3 src/validate.py                      # every post meets the baseline
    if [ "$#" -gt 0 ]; then python3 src/validate.py "$@"; fi   # new posts meet the strict rules
    python3 src/build.py
    python3 src/check_site.py
    ;;
  deploy)
    [ -z "$(git status --porcelain)" ] || { echo "Commit your changes first."; exit 1; }
    retry git pull --rebase -q origin main
    python3 src/build.py >/dev/null && python3 src/check_site.py
    retry git push -q origin HEAD:main
    tmp=$(mktemp -d)
    cp -a public/. "$tmp/"
    (
      cd "$tmp"
      git init -q -b gh-pages
      git config user.name "$(git -C "$OLDPWD" config user.name || echo publisher)"
      git config user.email "$(git -C "$OLDPWD" config user.email || echo publisher@localhost)"
      git add -A
      git commit -q -m "Deploy site $(date -u +%Y-%m-%dT%H:%MZ)"
      retry git push -q -f "$REPO_URL" gh-pages:gh-pages
    )
    rm -rf "$tmp"
    echo "Deployed. GitHub Pages updates within a few minutes."
    ;;
  *)
    sed -n '2,9p' "$0"; exit 1 ;;
esac
