import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.05)
w=whoosh(.9,300,1300,500,.5,1.0); add(w,0.05,.14,sweep(w,-.4,.4))
for t in (.15,.5,.75): txt(t,.07,-.3)
# four books drop onto the stack, heaviest first
for land,g in ((1.35,.62),(2.25,.55),(3.1,.48),(3.9,.44)):
    add(whoosh(.42,600,1800,900,.7,1.0),land-.42,.08)
    add(thud(100,44,.42,.28,11),land,g); add(slap(.1),land,.12)
    txt(land+.12,.05,-.4)
for t in (5.75,5.9): add(whoosh(.4,2200,700,300,.3,1.0),t,.09)
# hero: the stack lifts and fans out
for i,t in enumerate((6.25,6.5,6.75,7.0)):
    w=whoosh(1.0,250,1300,450,.5,1.0); add(w,t,.13,sweep(w,.5-.3*i,-.3+.2*i)); add(flip(.45),t+.9,.12)
add(clack(.8),8.15,.2); add(clack(.6),8.3,.14); txt(7.3,.1)
txt(8.0,.06)
w=whoosh(1.1,300,1500,600,.5,1.0); add(w,9.55,.17,sweep(w,-.3,.3))
for t in (9.95,10.1,10.7,10.9): txt(t,.06)
w=whoosh(.9,2400,500,250,.3,1.0); add(w,13.25,.2)
add(scrape(.7),13.6,.08); w=whoosh(.9,200,1000,300,.5,.9); add(w,13.6,.2)
endcard(14.4)
master('sfx.wav')
