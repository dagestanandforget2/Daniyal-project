import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.05)
txt(.3,.07,-.3); txt(.45,.06,-.3)
SL=[2.2,6.35,10.25]; EX=[5.75,9.75,13.55]
add(whoosh(1.6,200,700,300,.7,1.0),0.6,.12)
for i,s in enumerate(SL):
    if i>0: add(whoosh(.75,300,1500,600,.85,1.0),s-.75,.13)
    add(thud(110,40,.45,.4,9),s,.65 if i==0 else .5)
    add(slap(.16),s,.35 if i==0 else .25)
    add(shimmer(.8),s+.2,.10)
    add(whoosh(.6,600,1600,500,.4,1.0),s+.18,.08)
    txt(s+.9,.06,-.2); txt(s+1.05,.05,-.2)
    add(whoosh(.6,1500,500,300,.3,1.0),EX[i],.09,-.4)
for i in range(3): add(clack(.6),13.65+i*.12+.55,.18,-.3+.3*i)
txt(13.95,.07,-.3)
add(whoosh(.7,250,1100,400,.5,1.0),15.25,.12)
endcard(15.75)
master('sfx.wav')
