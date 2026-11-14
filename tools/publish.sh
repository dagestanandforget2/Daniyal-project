#!/bin/bash
# tools/publish.sh OUT_DIR
#   Puts every .mp4 in OUT_DIR online for Metricool to copy and prints one line per video:
#     VIDEO_URL <file> https://raw.githubusercontent.com/<owner>/<repo>/reels-drop/<file>
#
# The "reels-drop" branch holds ONE commit with the latest batch and is replaced on every publish,
# so the repository never grows. Metricool copies each file when the post is scheduled, so the
# videos only have to stay online until the owner says yes. Never commit .mp4 files to trial-reels.
set -euo pipefail
DIR=$(readlink -f "${1:?usage: tools/publish.sh OUT_DIR}")
ls "$DIR"/*.mp4 >/dev/null 2>&1 || { echo "No .mp4 files in $DIR" >&2; exit 1; }
ROOT=$(cd "$(dirname "$0")/.." && pwd)
REMOTE=$(git -C "$ROOT" remote get-url origin)
SLUG=$(echo "$REMOTE" | sed -E 's#^.*github\.com[:/]##; s#\.git$##')

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
git -C "$TMP" init -q -b reels-drop
cp "$DIR"/*.mp4 "$TMP/"
printf 'Latest Trial Reels batch for Metricool to copy. This branch is replaced on every publish.\n' > "$TMP/README.md"
git -C "$TMP" add -A
git -C "$TMP" -c user.name="dar-al-athari-tasks" -c user.email="autopost-bot@users.noreply.github.com" \
    commit -q -m "trial reels batch $(date -u +%Y-%m-%d)"

ok=0
for i in 1 2 3; do
  if git -C "$TMP" push -q --force "$REMOTE" HEAD:refs/heads/reels-drop; then ok=1; break; fi
  echo "push attempt $i failed, retrying" >&2; sleep 4
done
[ "$ok" = 1 ] || { echo "Could not push the videos" >&2; exit 1; }

for f in "$TMP"/*.mp4; do
  n=$(basename "$f")
  URL="https://raw.githubusercontent.com/$SLUG/reels-drop/$n"
  code=$(curl -sIL -o /dev/null -w '%{http_code}' --retry 10 --retry-delay 6 --retry-all-errors -f "$URL" || true)
  [ "$code" = 200 ] || { echo "Pushed, but $URL answered $code" >&2; exit 1; }
  echo "VIDEO_URL $n $URL"
done
