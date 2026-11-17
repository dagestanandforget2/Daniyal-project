import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.05)
w=whoosh(.8,300,1500,600,.5,1.0); add(w,0.0,.16,sweep(w,.3,-.2))
add(thud(100,48,.3,.2,12),1.15,.14)
add(whoosh(.8,250,1600,500,.6,1.0),2.5,.16); add(clack(.8),3.2,.18)
for t in (2.75,2.87,3.05): txt(t)
# slab drops in, camera pushes onto the list
add(whoosh(.9,200,1100,400,.6,1.0),4.6,.18); add(thud(110,50,.3,.2,12),5.25,.2)
# roll call: one tick per name, accelerating
R0,R1=5.35,7.85
for i in range(13): add(tick(.55+.04*i),R0+(R1-R0)*(i/12)**.62,.12+.008*i)
# hit
add(slap(),8.0,.34); add(thud(90,40,.45,.35,11),8.02,.55); add(clack(1.1),8.05,.2)
add(whoosh(1.0,200,2200,500,.7,1.0),8.3,.2)
add(thud(100,46,.3,.2,12),9.4,.2)
for t in (9.55,9.67,9.85): txt(t)
add(whoosh(.8,300,1500,600,.5,1.0),10.75,.15); add(clack(.7),11.3,.14)
for t in (11.15,11.27,11.45): txt(t)
add(whoosh(.8,300,1500,600,.5,1.0),12.5,.15)
for t in (12.85,12.95,13.15): txt(t)
add(whoosh(1.0,200,1200,400,.6,1.0),14.3,.18); add(thud(96,42,.4,.25,12),14.9,.3); add(shimmer(1.2,6200,.5),14.85,.07)
for t in (15.3,15.45): txt(t)
add(click(1),15.8,.25)
for k in range(2): add(tick(.6),16.5+k*1.4,.12)
master('sfx.wav')
