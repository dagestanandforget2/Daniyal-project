import os; os.environ['SFXT']='18'
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
def sub(dur=1.2,f=46):
    n=int(dur*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*(f+20*np.exp(-tt*6))*tt)*np.exp(-tt*2.6)
add(rumble(17.6),.1,.13)
add(tick(1),.0,.4); add(shimmer(.6,7200,.4),.02,.08)
add(scratch(.7),.2,.1,-.2); add(scratch(.6),.7,.08,.2)          # compass arcs
add(scratch(.7),1.0,.12,-.3); add(scratch(.7),1.35,.12,.3)        # the two squares
add(scratch(.6),1.8,.08)
add(sub(1.6,44),2.3,.6); add(whoosh(1.4,200,900,300,.4,.9),2.3,.25)
for d in range(1,6): add(shimmer(.5,6000+d*300,.4),2.35+d*.32,.07,(-.3 if d%2 else .3)); add(tick(.7),2.35+d*.32,.12)
add(thud(80,36,.6,.18,8),3.2,.45); add(shimmer(1.0,6600,.5),3.2,.1)
for t in (3.6,3.9,6.3,6.6,9.3,9.6,13.6): add(whoosh(.45,800,2000,900,.4,1.0),t,.08)
add(whoosh(.9,1600,500,200,.5,.9),5.9,.25)
for k,t in enumerate((6.6,6.85,7.1,7.35)): add(thud(100,48,.3,.25,14),t,.35,(-.4 if k%2==0 else .4)); add(tick(.7),t,.15)
add(shimmer(2.2,6200,.6),9.0,.1)
add(whoosh(1.2,300,1200,400,.5,.9),11.7,.25)
add(sub(2.0,40),12.9,.75); add(thud(80,36,.8,.14,6),12.95,.45); add(shimmer(1.6,6000,.6),12.9,.15)
add(thud(92,40,.4,.22),14.4,.45); add(tick(1),14.4,.3)
for k in range(2): add(tick(.6),15.2+k*1.7,.18)
master('sfx.wav')
