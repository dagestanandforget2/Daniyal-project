import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.05)
# books drop in on their strings
for i in range(4): add(whoosh(.35,1800,900,400,.3,1.0),.2+i*.16,.08,-.6+i*.4); add(click(.8),.55+i*.16,.25,-.6+i*.4)
txt(.35,.07); txt(.55,.06); txt(.75,.06)
# phase 1 pull-back + strikes
w=whoosh(.6,400,1200,500,.6,1.0); add(w,2.45,.12,-.5)
Q=.32
for k in range(6): add(clack(1.0),3.0+Q+k*2*Q,.5*(.92**k),(.5 if k%2==0 else -.5))
add(clack(.6),3.0+Q+12*Q,.22)
for t0 in (3.35,5.3,8.75,10.5): txt(t0,.06)
add(whoosh(.5,400,1200,500,.6,1.0),7.95,.12,-.5)
for k in range(5): add(clack(1.0),8.4+Q+k*2*Q,.55*(.92**k),(.5 if k%2==0 else -.5))
add(clack(.6),8.4+Q+10*Q,.25)
# hero
add(whoosh(.6,300,900,400,.7,1.0),12.45,.15,.6)
HS=13.0+Q
add(whoosh(.35,600,2400,900,.7,1.0),HS-.3,.2,.4)
add(clack(1.4),HS,.8); add(thud(110,44,.5,.35,9),HS,.6); add(slap(.2),HS,.3)
w=whoosh(1.05,500,2600,600,.5,1.0); add(w,HS+.02,.22,sweep(w,-.5,.4))
txt(13.45,.08); txt(13.65,.07)
add(whoosh(.6,1200,2600,900,.4,1.0),14.55,.14)
# sign drops and swings
add(whoosh(.6,300,1400,500,.6,1.0),14.85,.18); add(thud(90,40,.4,.25,12),15.45,.4); add(tick(.7),15.45,.3)
endcard(15.45)
master('sfx.wav')
