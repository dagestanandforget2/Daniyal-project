#!/bin/bash
# publish.sh VIDEO.mp4
#   Puts the finished video online and prints its public address on the last line:
#     VIDEO_URL https://raw.githubusercontent.com/<owner>/<repo>/video-drop/<file>.mp4
#
# Why: finished videos used to be committed to tiktok-studio, which grew the repository by
# about 30 MB a day and made every run download every old video. Now each video goes to the
# "video-drop" branch, which holds ONE commit with ONE video and is replaced every time.
# Metricool copies the file the moment the post is scheduled, so the video only has to stay
# online until then. Never commit .mp4 files to tiktok-studio (videos/ is git-ignored).
set -euo pipefail
SRC=$(readlink -f "${1:?usage: tools/publish.sh videos/DATE-slug.mp4}")
[ -s "$SRC" ] || { echo "No such video: $SRC" >&2; exit 1; }
NAME=$(basename "$SRC")
ROOT=$(cd "$(dirname "$0")/.." && pwd)
REMOTE=$(git -C "$ROOT" remote get-url origin)
SLUG=$(echo "$REMOTE" | sed -E 's#^.*github\.com[:/]##; s#\.git$##')

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
git -C "$TMP" init -q -b video-drop
cp "$SRC" "$TMP/$NAME"
printf 'Latest video for Metricool to copy. This branch is replaced on every publish.\n' > "$TMP/README.md"
git -C "$TMP" add -A
git -C "$TMP" -c user.name="dar-al-athari-tasks" -c user.email="autopost-bot@users.noreply.github.com" \
    commit -q -m "video: $NAME"

ok=0
for i in 1 2 3; do
  if git -C "$TMP" push -q --force "$REMOTE" HEAD:refs/heads/video-drop; then ok=1; break; fi
  echo "push attempt $i failed, retrying" >&2
done
[ "$ok" = 1 ] || { echo "Could not push the video" >&2; exit 1; }

URL="https://raw.githubusercontent.com/$SLUG/video-drop/$NAME"
code=$(curl -sIL -o /dev/null -w '%{http_code}' --retry 10 --retry-delay 6 --retry-all-errors -f "$URL" || true)
[ "$code" = 200 ] || { echo "Pushed, but $URL answered $code" >&2; exit 1; }
echo "VIDEO_URL $URL"
