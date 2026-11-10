import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.07,.05)
add(whoosh(1.0,160,1000,380,.6,1.0),.05,.16); add(thud(100,46,.34,.22,12),1.0,.32)
for i in range(10): add(tick(.5),.3+i*.2,.08,(-1)**i*.2)
txt(.35,.08); txt(.5,.08); txt(.9,.05)
F=[0.0,5.6,9.3]; O=[2.55,6.35,10.05]; X=[5.45,9.15,12.6]
for i in range(3):
    if i>0:
        add(whoosh(.8,1200,400,200,.6,1.0),F[i],.12)
        for j in range(5): add(tick(.6),F[i]+j*.13,.12)
    add(shimmer(.9,6000,.6),O[i]-.1,.16); add(whoosh(.9,250,1900,600,.45,1.0),O[i],.15); add(clack(.6),O[i]+.95,.18)
    txt(O[i]+.45,.08); txt(O[i]+.6,.06)
    add(whoosh(.7,300,1800,600,.4,1.0),X[i],.12)
n=0;t=12.75
while t<13.7:
    add(tick(.8),t,.12+.14*(t-12.75),(-1)**n*.35); n+=1; t+=max(.03,.17-(t-12.75)*.15)
add(whoosh(1.1,150,2600,800,.7,1.0),12.75,.15)
add(slap(.2),13.75,.35); add(thud(72,32,.7,.4,6),13.75,.65); add(shimmer(1.2,6500,.7),13.78,.2)
add(whoosh(.9,300,2600,900,.4,.9),13.8,.18)
txt(14.05,.09); txt(14.2,.08)
add(whoosh(.9,180,900,300,.5,1.0),15.3,.18)
endcard(15.95)
master('sfx.wav')
