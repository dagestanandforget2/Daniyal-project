import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.05)
w=whoosh(.8,300,1500,600,.5,1.0); add(w,0.0,.18,sweep(w,-.3,.3))
for i in range(9): add(clack(.4),.25+i*.06,.06,-.6+i*.15)
# scramble
w=whoosh(.7,500,1800,700,.5,1.0); add(w,2.8,.2,sweep(w,.4,-.4))
for i in range(9): add(scrape(.25),2.9+i*.04,.07,-.6+i*.15)
for t in (3.05,3.2,3.45): txt(t)
txt(6.45)
# lock: one tick+clack per volume
L0=6.75;LS=.22;SLAM=L0+8*LS+.32
for k in range(9):
    t0=L0+k*LS+.12; add(tick(1),t0,.18,-.6+k*.15); add(clack(.6),t0+.02,.12,-.6+k*.15)
add(whoosh(.3,2000,500,300,.4,1.0),SLAM-.3,.16)
add(thud(92,40,.45,.35,11),SLAM,.6); add(slap(.16),SLAM,.25); add(shimmer(1.1,6500,.5),SLAM+.08,.08)
for t in (8.95,9.08): txt(t)
w=whoosh(.9,400,1500,600,.5,1.0); add(w,9.9,.18,sweep(w,0,.3))
add(flip(.6),10.2,.1)
for t in (10.55,10.68,10.9): txt(t)
add(flip(.7),12.2,.14)
for t in (12.55,12.68,12.9): txt(t)
add(whoosh(.7,2400,600,300,.3,1.0),14.1,.2)
add(thud(96,42,.4,.25,12),14.6,.45); add(shimmer(1.2,6200,.5),14.65,.08)
for t in (15.0,15.2): txt(t)
add(click(1),15.55,.25)
for k in range(2): add(tick(.6),16.3+k*1.4,.12)
master('sfx.wav')
