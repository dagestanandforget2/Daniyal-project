import os; os.environ['SFXT']='18'
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
def pop(g=1.0):
    n=int(.06*SR); tt=np.arange(n)/SR; return svf(rng.standard_normal(n),1700.0,3.0)*np.exp(-tt*70)*g
add(rumble(18.4),.1,.07)
for i,t in enumerate((.15,.3,.75)): add(whoosh(.45,500,1900,800,.4,1.0),t-.05,.14,-.3+i*.3)
w=whoosh(.6,2200,600,300,.3,1.0); add(w,2.5,.22,sweep(w,.3,-.3))
for i in range(9):
    t0=2.75+i*.17+.55; add(thud(105-i*3,46,.32,.3,13),t0,.42,(-.6+i*.15)); add(clack(.8),t0,.18,(-.6+i*.15))
for t in (3.95,4.1): add(whoosh(.4,600,2000,900,.4,1.0),t-.05,.12)
w=whoosh(1.0,300,1500,600,.5,1.0); add(w,5.0,.22,sweep(w,-.5,.5))
for t in (5.75,7.95,8.65,9.45): add(slap(.12),t,.22); add(whoosh(.4,700,2200,900,.4,1.0),t-.1,.1)
w=whoosh(.8,300,1400,500,.5,1.0); add(w,7.45,.12,sweep(w,-.3,.3)); add(w,8.1,.1); add(w,8.85,.1); add(w,9.6,.1)
add(scrape(.9),10.15,.3); add(whoosh(.9,400,1600,600,.5,1.0),10.5,.18); add(shimmer(1.2,6500,.5),11.0,.08)
for t in (10.85,11.15): add(whoosh(.4,600,2000,900,.4,1.0),t-.05,.12)
add(scrape(.6),13.3,.22); add(whoosh(.7,2400,600,300,.3,1.0),13.7,.2)
add(thud(96,42,.4,.25,12),14.25,.5); add(shimmer(1.2,6200,.5),14.3,.08)
for t in (14.55,14.8): add(whoosh(.4,600,2000,900,.4,1.0),t-.05,.1)
add(pop(1),15.2,.3); add(tick(1),15.25,.18)
for k in range(2): add(tick(.6),16.1+k*1.5,.13)
master('sfx.wav')
