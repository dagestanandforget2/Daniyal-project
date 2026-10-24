import os; os.environ['SFXT']='19'
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
def sub(dur=1.0,f=50):
    n=int(dur*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*(f+25*np.exp(-tt*7))*tt)*np.exp(-tt*3)
def pop(g=1.0):
    n=int(.06*SR); tt=np.arange(n)/SR; return svf(rng.standard_normal(n),1800.0,3.0)*np.exp(-tt*70)*g
add(rumble(18.6),.1,.1)
for i,t in enumerate((0.15,0.3,0.45,0.6)): add(pop(1),t+.05,.35,-.2+i*.13); add(thud(110,55,.2,.3,20),t+.05,.25)
add(whoosh(.5,600,2000,900,.4,1.0),.7,.15); add(slap(.12),1.0,.3); add(shimmer(.6,6800,.4),1.05,.08)
for c in (3.6,7.0,10.6,14.0):
    w=whoosh(.7,250,1600,500,.5,.9); add(w,c-.35,.32); add(sub(.7,52),c,.4)
for t in (3.95,4.15,4.7): add(pop(1),t+.05,.3); add(thud(100,48,.25,.3,16),t+.05,.25)
add(scratch(.8),5.0,.08)
add(pop(1),7.4,.3)
for i in range(4): add(whoosh(.45,1200,3000,1500,.3,1.0),7.7+i*.22,.12,(-.4 if i%2==0 else .4)); add(slap(.1),8.2+i*.22,.25)
n=int(3.3*SR); tt=np.arange(n)/SR; bed=svf(rng.standard_normal(n),300+120*np.sin(tt*2),1.0)*(np.sin(np.pi*tt/3.3)**.6); add(bed,10.65,.18)
for k in range(12): add(tick(.6),10.8+k*.27,.12,rng.uniform(-.5,.5))
add(sub(1.4,44),14.4,.6); add(thud(84,38,.6,.15,8),14.45,.4); add(shimmer(1.4,6200,.5),14.4,.12)
for t in (14.75,14.9): add(pop(1),t+.05,.3)
add(thud(96,42,.35,.22,14),15.3,.45); add(tick(1),15.3,.3)
for k in range(2): add(tick(.6),16.0+k*1.6,.18)
master('sfx.wav')
