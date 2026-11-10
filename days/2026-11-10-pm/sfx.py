import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.08,.05)
add(whoosh(.9,180,1100,400,.6,1.0),.1,.16); add(thud(105,48,.32,.25,12),.95,.33)
for i in range(7): add(tick(.5),1.0+i*.11,.12)
txt(.45,.08); txt(.6,.08); txt(1.0,.05)
for a in (2.7,6.0,9.3):
    for i in range(4): add(tick(.7),a-.5+i*.09,.14)
    add(whoosh(.8,300,2000,700,.5,1.0),a,.14); add(clack(.6),a+.85,.22)
    txt(a+.6,.08); txt(a+.75,.06)
for a in (5.55,8.85,12.0): add(whoosh(.7,300,1800,600,.4,1.0),a,.12)
txt(12.2,.08); txt(12.35,.07)
n=0;t=12.1
while t<13.55:
    add(tick(.8),t,.12+.1*(t-12.1),(-1)**n*.3); n+=1; t+=max(.025,.16-(t-12.1)*.1)
add(whoosh(1.4,150,2600,800,.6,1.0),12.2,.14)
add(slap(.2),13.6,.35); add(thud(72,32,.7,.4,6),13.6,.65); add(clack(1.0),13.61,.3)
add(whoosh(.9,300,2600,900,.4,.9),13.65,.18)
txt(14.0,.09); txt(14.15,.08)
add(whoosh(.9,180,900,300,.5,1.0),15.2,.18); add(scrape(.7),15.45,.12)
endcard(15.95)
master('sfx.wav')
