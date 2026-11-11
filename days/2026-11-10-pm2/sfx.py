import os; os.environ['SFXT']='18'
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.06)
w=whoosh(.9,300,1500,600,.5,1.0); add(w,0.0,.2,sweep(w,-.3,.3))
for i in range(7): add(clack(.5),.35+i*.07,.08,.5-i*.15)
R0=3.05;ST=.42;SLAM=R0+6*ST+.55
for k in range(7):
    t0=R0+k*ST; add(scrape(.3),t0,.12,.5-k*.16); add(tick(1),t0,.16)
add(whoosh(.25,2000,500,300,.4,1.0),SLAM-.2,.16)
add(thud(92,40,.45,.35,11),SLAM,.6); add(clack(1),SLAM,.3); add(shimmer(1.1,6500,.5),SLAM+.1,.09)
for t in (6.55,6.7): txt(t)
w=whoosh(1.0,400,1500,600,.5,1.0); add(w,7.7,.2,sweep(w,-.4,.3))
add(flip(.6),8.3,.12); add(shimmer(1.0,6000,.5),9.0,.06)
for t in (8.75,8.9,9.1): txt(t)
add(whoosh(.8,1500,500,300,.4,1.0),11.2,.16); add(clack(.7),11.95,.2)
for t in (11.95,12.1,12.35): txt(t)
add(whoosh(.7,2400,600,300,.3,1.0),14.0,.2)
add(thud(96,42,.4,.25,12),14.55,.45); add(shimmer(1.2,6200,.5),14.6,.08)
for t in (14.9,15.1): txt(t)
add(click(1),15.5,.25)
for k in range(2): add(tick(.6),16.3+k*1.4,.12)
master('sfx.wav')
