#!/bin/bash
# make.sh PROJECT_DIR SECONDS OUT.mp4  -> build, sfx, render in 2 parallel halves, mux, contact sheet (PROJECT_DIR/sheet.jpg)
set -e
D=$(cd "$1" && pwd); T=$2; OUT=$3; F=$((T*30)); H=$((F/2)); TOOLS=$(cd "$(dirname "$0")" && pwd)
python3 $TOOLS/build.py $D
(cd $D && SFXT=$T python3 sfx.py)
python3 $TOOLS/render.py $D 0 $H $D/_a.mp4 > $D/_r1.log 2>&1 &
python3 $TOOLS/render.py $D $H $F $D/_b.mp4 > $D/_r2.log 2>&1 &
wait
printf "file '_a.mp4'\nfile '_b.mp4'\n" > $D/_list.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i $D/_list.txt -i $D/sfx.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
if [ $(stat -c %s "$OUT") -gt 29000000 ]; then ffmpeg -y -loglevel error -i "$OUT" -c:v libx264 -crf 21 -preset medium -pix_fmt yuv420p -c:a copy -movflags +faststart $D/_s.mp4 && mv $D/_s.mp4 "$OUT"; fi
ffmpeg -y -loglevel error -i "$OUT" -vf "fps=10/$T,scale=216:384,tile=5x2" -frames:v 1 $D/sheet.jpg
rm -f $D/_a.mp4 $D/_b.mp4 $D/_list.txt
echo ALLDONE "$OUT"
