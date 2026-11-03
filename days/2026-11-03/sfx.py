import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.05)
txt(.3,.07); txt(.5,.06); txt(.65,.06)
# brush strokes: a fast whoosh plus a dry bristle scratch
for t0,d,pn in ((1.05,.5,-.4),(2.75,.42,.4),(5.75,.42,-.4),(8.75,.42,.4)):
    w=whoosh(d+.2,500,2200,800,.5,1.0); add(w,t0-.05,.16,sweep(w,-pn,pn)); add(scratch(d),t0,.22,pn); add(slap(.12),t0+d*.9,.12,pn)
# books spin in and land
for a in (2.87,5.87,8.87):
    add(whoosh(.6,300,1500,600,.6,1.0),a,.14); add(thud(100,45,.35,.2,12),a+.6,.35); txt(a+.3,.06)
# books fly away
for e in (5.5,8.5,10.95): add(whoosh(.5,600,2000,900,.5,1.0),e-.1,.12,.3)
# ink drop falls and floods
add(whoosh(.5,1200,400,300,.8,1.0),11.12,.12)
add(thud(80,36,.6,.4,7),11.62,.8); add(slap(.25),11.62,.4); add(rumble(1.4),11.62,.3)
w=whoosh(1.0,300,1600,400,.4,1.0); add(w,11.64,.2,sweep(w,-.6,.6))
for i,r in enumerate((12.29,12.15,12.43)): add(thud(110,50,.3,.2,13),r+.55,.3,(i-1)*.5)
txt(12.55,.08); txt(12.7,.07)
add(whoosh(.6,1500,500,400,.6,1.0),14.45,.14)
endcard(14.95)
master('sfx.wav')
