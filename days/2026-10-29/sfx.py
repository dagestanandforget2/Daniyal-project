import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.05)
for i in range(4): add(thud(100,40,.4,.3,10),.15+i*.18+.45,.35,-.3+.2*i); add(clack(.5),.15+i*.18+.45,.12)
txt(.3,.06,-.3); txt(.55,.07,-.3); txt(.67,.05,-.3)
add(whoosh(.8,250,1200,400,.6,1.0),2.0,.14)
LAND=[2.75,5.65,8.55,11.45]
for i,L in enumerate(LAND):
    if i>0: add(whoosh(.7,300,1400,600,.6,1.0),L-.95,.12)
    add(whoosh(.45,1500,600,300,.5,1.0),L-.45,.07)
    add(thud(105,40,.45,.35,9),L,.6); add(slap(.14),L,.25)
    txt(L+.05,.06,-.2); txt(L+.2,.05,-.2)
for a in [5.25,8.15,11.05]: add(tick(1),a+.45,.25,-.4)
add(whoosh(1.4,200,900,300,.5,1.0),13.0,.16)
for i in range(4): add(clack(.8),13.55+i*.16+.25,.2,-.3+.2*i)
txt(13.45,.07,-.3); txt(13.6,.06,-.3)
endcard(15.35)
master('sfx.wav')
