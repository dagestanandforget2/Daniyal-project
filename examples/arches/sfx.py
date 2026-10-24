import os; os.environ['SFXT']='18'
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
def sub(dur=1.0,f=50):
    n=int(dur*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*(f+25*np.exp(-tt*7))*tt)*np.exp(-tt*3)
def pop(g=1.0):
    n=int(.06*SR); tt=np.arange(n)/SR; return svf(rng.standard_normal(n),1600.0,3.0)*np.exp(-tt*70)*g
add(rumble(17.6),.1,.1)
add(pop(1),.4,.3); add(pop(1),.6,.3); add(thud(100,45,.3,.25,14),.6,.3)
add(whoosh(1.1,200,1100,400,.5,.9),.55,.25); add(sub(1.2,46),1.5,.4)
for i in range(3): add(shimmer(.5,7000,.4),1.2+i*.18,.07,(-.4+i*.4)); add(tick(.7),1.2+i*.18,.15)
for c in (3.4,6.6,9.8,12.8):
    w=whoosh(.8,180,1400,400,.55,.9); add(w,c-.4,.3); add(sub(.8,50),c+.35,.4)
for t in (3.6,3.78,6.85,7.05,13.6): add(pop(1),t+.05,.3); add(thud(100,48,.25,.3,16),t+.05,.22)
for i,t in enumerate((4.0,4.15,4.3)): add(whoosh(.7,300,1500,600,.5,1.0),t,.14,(-.4+i*.4)); add(slap(.1),t+.75,.2,(-.4+i*.4))
for t in (7.3,7.5): add(whoosh(.7,300,1500,600,.5,1.0),t,.14)
for t in (10.2,10.4,10.6): add(whoosh(.5,2600,700,300,.3,1.0),t,.18,sweep(np.zeros(int(.5*SR)),-.7,0)); add(thud(90,40,.3,.25,14),t+.45,.3)
add(whoosh(.7,300,1500,600,.5,1.0),11.0,.12)
add(sub(1.8,40),13.0,.6); add(shimmer(1.6,6200,.5),13.0,.12)
add(thud(96,42,.35,.22,14),14.2,.45); add(tick(1),14.2,.3)
for k in range(2): add(tick(.6),15.0+k*1.6,.18)
master('sfx.wav')
