import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.05)
txt(.3,.08); txt(.45,.08); txt(.85,.05)
# surges through the tunnel
for a in (2.0,5.4,8.8):
    add(whoosh(1.0,180,1400,500,.5,1.0),a,.18)
for a in (2.45,5.85,9.25):
    add(whoosh(.9,600,2200,900,.6,.9),a,.07); add(thud(100,46,.35,.2,12),a+.85,.3)
    txt(a+.55,.08); txt(a+.7,.06)
# hero hyperspeed
add(whoosh(1.7,150,3200,900,.6,.9),12.2,.28)
for i in range(22):
    q=i/21; s=12.25+1.5*q**0.8
    add(tick(.6),s,.06,(-1)**i*.4)
add(thud(78,34,.7,.4,6),13.8,.7); add(slap(.18),13.8,.25); add(shimmer(1.2,6000,.6),13.8,.15)
txt(14.0,.09); txt(14.15,.08)
add(whoosh(.9,180,900,300,.5,1.0),15.0,.18)
endcard(15.8)
master('sfx.wav')
