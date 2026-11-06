import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.04)
txt(.3,.08); txt(.45,.07); txt(.7,.05)
for a in (2.0,5.6,9.2):
    add(click(1.0),a-.02,.12); add(slap(.08),a,.08)            # shutter + flash
    add(scrape(.7),a+.12,.09)                                   # print ejects
    add(whoosh(.5,300,1100,500,.5,1.0),a+.25,.08)
    add(tick(.6),a+.85,.06)
    for k in range(4): add(flip(.18),a+.95+k*.17,.035,(-1)**k*.3)  # shaking the print
    txt(a+.55,.08); add(scratch(.55),a+1.55,.07)               # handwriting
    txt(a+1.4,.06)
    add(whoosh(.55,600,1900,500,.5,1.0),a+3.05,.11)             # tossed aside
# hero
add(whoosh(.6,200,900,400,.5,1.0),12.85,.1)
add(click(1.0),13.42,.14); add(thud(80,36,.55,.35,7),13.45,.6); add(slap(.2),13.45,.22)
add(shimmer(.9),13.47,.06); add(whoosh(.8,200,1600,600,.5,1.0),13.5,.16)
add(whoosh(.7,300,1200,500,.5,1.0),13.95,.07)
txt(13.55,.08); txt(13.7,.07)
add(whoosh(.6,500,1800,700,.5,1.0),15.35,.12)
# end shot
add(click(1.0),15.53,.12); add(scrape(.8),15.65,.09); add(tick(.7),16.45,.07)
endcard(16.5)
master('sfx.wav')
