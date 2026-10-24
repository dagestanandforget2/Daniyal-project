import os; os.environ['SFXT']='18'
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
def pop(g=1.0):
    n=int(.06*SR); tt=np.arange(n)/SR; return svf(rng.standard_normal(n),1700.0,3.0)*np.exp(-tt*70)*g
def rustle(dur):
    n=int(dur*SR); x=svf(rng.standard_normal(n),3200.0,.8); am=np.clip(np.abs(svf(rng.standard_normal(n),18.0,.7,'lp'))*6,0,1); return x*am
add(rumble(18.4),.1,.08)
w=whoosh(1.3,300,2400,700,.5,.9); add(w,0,.3,sweep(w,-.5,.5)); add(rustle(1.4),.1,.12)
add(thud(90,40,.45,.35,11),1.5,.55); add(slap(.14),1.5,.35)
for t in (3.4,7.1): add(whoosh(.9,400,1400,600,.5,1.0),t,.12); add(rustle(.6),t,.06)
add(scratch(1.1),8.4,.35)
w=whoosh(.5,500,2600,900,.35,1.0); add(w,9.45,.3,sweep(w,.5,-.5))
w=whoosh(1.2,300,2400,700,.5,.9); add(w,9.6,.28,sweep(w,.5,-.5)); add(rustle(1.2),9.7,.12)
add(thud(80,36,.6,.4,9),10.9,.8); add(slap(.18),10.9,.45)
add(whoosh(.6,2400,600,300,.3,1.0),13.3,.25); add(rustle(.6),13.3,.08)
add(thud(100,44,.4,.35,13),14.0,.6); add(clack(1),14.0,.3)
add(pop(1),14.9,.3); add(tick(1),15.0,.2)
for k in range(2): add(tick(.6),15.9+k*1.0,.15)
master('sfx.wav')
