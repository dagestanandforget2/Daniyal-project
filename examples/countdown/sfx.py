import os; os.environ['SFXT']='19'
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
def sub(dur=1.0,f=50):
    n=int(dur*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*(f+25*np.exp(-tt*7))*tt)*np.exp(-tt*3)
def pop(g=1.0):
    n=int(.06*SR); tt=np.arange(n)/SR; return svf(rng.standard_normal(n),1700.0,3.0)*np.exp(-tt*70)*g
add(rumble(18.6),.1,.12)
add(sub(1.2,44),.15,.8); add(thud(90,40,.5,.3,10),.15,.5)
add(whoosh(.5,2600,700,300,.3,1.0),.35,.25,-.4)
for i in range(3): add(whoosh(.5,300,1600,600,.4,1.0),.7+i*.12,.12,(-.3+i*.3)); add(slap(.1),1.2+i*.12,.25)
for s0 in (2.2,5.6,9.0,12.6,14.6):
    w=whoosh(.5,500,2600,900,.35,1.0); add(w,s0-.1,.3,sweep(w,.6,-.6))
for s0 in (2.2,5.6,9.0):
    add(sub(1.0,48),s0+.25,.7); add(thud(100,44,.4,.3,12),s0+.25,.45); add(tick(1),s0+.25,.25)
    add(whoosh(.7,400,1800,600,.4,1.0),s0+.45,.16,.5)
    add(shimmer(.8,7000,.5),s0+1.2,.1)
    for k in range(4): add(pop(.8),s0+1.0+k*.12,.15)
for t in (12.85,13.0): add(whoosh(.45,2400,700,300,.3,1.0),t,.15,-.4)
for t in (13.1,13.25): add(whoosh(.6,300,1500,600,.4,1.0),t,.14); add(slap(.1),t+.6,.25)
add(sub(1.6,40),14.85,.7); add(shimmer(1.4,6200,.5),14.85,.12)
for t in (15.1,15.25): add(pop(1),t,.25)
add(thud(96,42,.35,.22,14),15.6,.45); add(tick(1),15.6,.3)
for k in range(2): add(tick(.6),16.3+k*1.6,.18)
master('sfx.wav')
