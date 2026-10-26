import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.045)
w=whoosh(.8,250,1100,400,.5,1.0); add(w,0.1,.12,sweep(w,-.3,.3))
txt(.2,.07,-.3); txt(.45,.06,-.3)
# three books land on the plinth
for land,g,p in ((1.15,.55,0),(1.55,.45,.35),(1.95,.45,-.35)):
    add(whoosh(.4,600,1800,900,.7,1.0),land-.4,.07,p)
    add(thud(110,50,.38,.25,12),land,g,p); add(slap(.1),land,.1,p)
for t in (2.85,2.95,3.3,6.15,6.2,6.6,9.75,9.85,10.15): txt(t,.05,-.4)
# turntable indexes: wooden drag then a stop knock
for t in (5.3,8.95):
    add(scrape(.95),t,.09); w=whoosh(.9,200,900,300,.5,1.0); add(w,t,.1,sweep(w,.4,-.4))
    add(clack(.5),t+.95,.16)
# hero: crane up while the plate whips a full turn
w=whoosh(1.7,180,1400,300,.55,1.0); add(w,11.55,.2,sweep(w,-.5,.5))
add(scrape(1.6),11.6,.08); add(shimmer(1.4,6000,.35),12.2,.6)
txt(11.9,.08)
add(thud(80,40,.5,.1,8),13.2,.25)
w=whoosh(1.0,300,1600,500,.5,1.0); add(w,13.35,.17)
endcard(14.15)
master('sfx.wav')
