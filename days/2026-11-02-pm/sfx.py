import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.06)
txt(.2,.08); txt(.35,.07); txt(.9,.05)
# hero: cloth lifts and folds down
w=whoosh(.8,300,1600,500,.5,1.0); add(w,2.55,.26,sweep(w,.3,-.3))
add(flip(.6),2.75,.18)
add(thud(90,40,.45,.2,10),3.22,.55); add(slap(.18),3.22,.25)
txt(3.45,.08); txt(3.57,.07)
# books drop onto the cloth
for t0 in (5.05,8.35,11.45):
    add(whoosh(.5,2200,700,300,.3,1.0),t0-.45,.16)
    add(thud(100,44,.35,.3,13),t0,.42); add(clack(.6),t0,.12)
    txt(t0+.05,.06)
for t0,p in ((7.45,-.5),(10.6,.5)):
    w=whoosh(.6,500,1900,700,.4,1.0); add(w,t0,.18,sweep(w,0,p*1.5))
# finale gather
for t0,p in ((13.4,-.5),(13.5,.5)): add(whoosh(.5,600,2000,900,.4,1.0),t0,.14,p)
add(clack(.5),14.0,.12); add(clack(.5),14.1,.1)
txt(13.55,.07); txt(13.7,.06)
# books lift away, cloth unfolds, red diamond opens
add(whoosh(.6,700,2400,900,.4,1.0),14.7,.16)
add(flip(.5),14.95,.14)
add(whoosh(.9,300,1400,500,.5,1.0),15.3,.22)
endcard(15.7)
master('sfx.wav')
