import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.05)
# box rises in
add(whoosh(1.1,180,900,300,.45,.9),.0,.18); add(thud(80,38,.45,.15,10),.9,.35)
txt(.2,.07,-.3); txt(.35,.06,-.3)
txt(2.25,.06,-.4)
# three books dropped in: fall whoosh, landing thud + knock, checkbox tick
for i,d in enumerate([2.35,4.35,6.35]):
    add(whoosh(.55,600,1600,700,.7,1.0),d-.05,.12,.1)
    add(thud(100-i*6,44,.4,.3,12),d+.55,.55); add(clack(.7),d+.56,.25)
    add(tick(.8),d+.6,.3,-.4)
    txt(d+.15,.05,-.4)
# flaps fold: side, side, front, back
for tt,p in [(8.55,-.4),(8.7,.4),(9.05,.0),(9.25,.0)]:
    add(flip(.45),tt,.22,p); add(slap(.14),tt+.32,.4,p)
txt(9.0,.06,-.3)
# tape run
add(scratch(.55),9.85,.35,sweep(np.zeros(int(.55*SR)),-.5,.5)); add(scrape(.5),9.85,.12)
# label slap + stamp
add(whoosh(.35,900,2200,900,.6,1.0),10.1,.12); add(slap(.18),10.67,.75); 
add(thud(95,42,.35,.35,14),10.95,.6); add(clack(.6),10.96,.3)
# box leaves
add(whoosh(.9,250,1400,400,.5,1.0),12.05,.25,sweep(np.zeros(int(.9*SR)),-.2,.8))
txt(12.45,.07,-.3); add(thud(90,40,.35,.2,12),12.75,.4)
# airmail wipe
add(whoosh(.8,300,2200,600,.5,1.0),14.1,.22,sweep(np.zeros(int(.8*SR)),-.8,.8))
endcard(14.7)
master('sfx.wav')
