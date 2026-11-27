import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.04)
w=whoosh(.6,300,1700,600,.4,1.0); add(w,0.0,.15,sweep(w,.3,-.2))
add(thud(92,44,.35,.2,12),0.15,.12)
add(whoosh(.8,250,1400,500,.6,1.0),2.6,.14); txt(2.75); txt(2.85)
# hero: the page edges riffle while the counter races to 328
add(whoosh(.7,300,1500,600,.5,1.0),4.4,.14); txt(4.55); txt(4.65)
ts=[4.55+1.05*((i/22.0)**(1/2.2)) for i in range(22)]
for i,tt in enumerate(ts): add(flip(.25),tt,.05+.03*i/22,[-.4,.4][i%2]); add(tick(.7),tt,.04)
w=whoosh(.9,400,2600,900,.6,1.0); add(w,5.0,.16,sweep(w,-.4,.4))
add(thud(96,42,.42,.3,12),5.6,.46); add(slap(),5.6,.28); add(clack(1.0),5.62,.12)
add(shimmer(1.0,6200,.5),5.65,.05)
txt(5.8); txt(5.9)
add(whoosh(.8,300,1300,500,.5,1.0),8.2,.13); add(scratch(.6),8.65,.04); txt(8.4); txt(8.5)
add(whoosh(.8,300,1300,500,.5,1.0),10.45,.12); add(scratch(.6),10.85,.04); txt(10.6); txt(10.7)
add(whoosh(.9,200,1200,400,.6,1.0),12.35,.14); add(thud(90,46,.3,.15,13),12.9,.08); txt(12.85); txt(12.95)
endcard(15.0)
master('sfx.wav')
