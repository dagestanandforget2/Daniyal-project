import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.06)
txt(.25,.08); txt(.4,.07); txt(.95,.05)
# hero: the concertina flings open panel by panel, books pop up
for i in range(3):
    t0=2.75+i*.2
    w=whoosh(.45,500,2200,800,.4,1.0); add(w,t0,.16,-.4+i*.4)
    add(flip(.4),t0+.25,.16,-.4+i*.4)
add(slap(.18),3.35,.3); add(thud(95,42,.38,.25,11),3.35,.45)
for i in range(3):
    add(clack(.6),3.55+i*.16,.12,-.4+i*.4); add(tick(.7),3.6+i*.16,.08)
# camera glides to each book
for t0,p in ((4.35,-.5),(7.3,0.),(10.3,.5)):
    w=whoosh(.7,300,1500,600,.5,1.0); add(w,t0,.16,sweep(w,0,p))
for t0 in (4.75,7.85,10.85):
    txt(t0+.05,.08); txt(t0+.2,.06); add(tick(.6),t0+.35,.05)
# pull back for the finale
add(whoosh(.8,300,1400,500,.5,1.0),13.2,.18)
txt(13.55,.07); txt(13.7,.06)
# books fold down, concertina folds shut, iris opens
for i in range(3): add(flip(.35),14.55+i*.06,.1)
for i in range(3): add(slap(.12),14.95+i*.1,.12)
add(thud(90,40,.35,.2,12),15.35,.3)
add(whoosh(.9,300,1400,500,.5,1.0),15.3,.22)
endcard(15.7)
master('sfx.wav')
