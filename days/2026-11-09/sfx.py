import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.04)
add(whoosh(1.0,180,600,200,.6,1.1),.05,.10); add(thud(90,45,.35,.2,12),.75,.35)
txt(.35,.08); txt(.5,.07); txt(.95,.05)
for i,a in enumerate((2.2,5.6,9.0)):
    pan=(-.5,.5,-.4)[i]
    add(whoosh(.95,300,2400,1800,.8,1.0),a,.13,pan)
    add(clack(1.0),a+.95,.42); add(thud(120,60,.25,.3,16),a+.95,.25)
    add(shimmer(.5,6000,.3),a+.97,.04)
    txt(a+.75,.07); txt(a+.85,.06)
for e in (5.25,8.65,12.05):
    add(whoosh(.6,800,2200,600,.3,1.0),e,.10,.4)
# hero: magnet charges (rising noise buzz), three books snap on at once
add(whoosh(1.0,400,3500,3000,.95,2.5),12.35,.12)
for k in range(10): add(tick(.6),12.4+k*.09,.05)
add(whoosh(.7,300,2600,3200,.85,1.0),12.65,.14)
add(thud(80,34,.8,.35,5.5),13.35,.75); add(slap(.18),13.35,.22)
for i,s in enumerate((13.35,13.38,13.41)): add(clack(.8),s,.25,(-.6,0,.6)[i])
add(shimmer(1.2,6500,.6),13.4,.10)
txt(13.55,.09); txt(13.7,.08)
add(whoosh(.9,600,220,120,.4,1.0),15.05,.16)
endcard(15.8)
master('sfx.wav')
