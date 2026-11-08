import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.04)
add(whoosh(1.6,200,700,250,.4,1.2),.2,.05,-.4); add(whoosh(1.4,220,800,260,.4,1.2),.9,.04,.4)
txt(.3,.08); txt(.42,.07); txt(.54,.08); txt(.95,.05)
# books surface: soft splash + low thud
for a in (2.2,5.6,9.0):
    add(whoosh(.8,1800,4200,1200,.25,.7),a+.1,.10); add(thud(110,50,.3,.12,14),a+.15,.22)
    add(shimmer(.8,5200,.4),a+.15,.05)
    txt(a+.6,.07); txt(a+.75,.06)
for a in (4.9,8.3,11.7):
    add(whoosh(.8,900,300,150,.4,1.0),a,.10)
# hero: the drop falls and hits
add(whoosh(.7,300,2600,3200,.85,1.0),11.95,.14)
add(thud(80,34,.8,.35,5.5),12.6,.75); add(slap(.18),12.6,.2)
add(whoosh(2.0,4000,900,200,.1,.6),12.62,.22); add(shimmer(1.4,6000,.6),12.65,.12)
for i,s in enumerate((12.95,13.1,13.25)): add(clack(.3),s,.2,(-.5,0,.5)[i])
txt(13.1,.09); txt(13.25,.08)
add(whoosh(.9,600,220,120,.4,1.0),15.0,.16)
endcard(15.8)
master('sfx.wav')
