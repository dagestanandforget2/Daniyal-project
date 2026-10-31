import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
def obp(x):
    x=min(max(x,0),1); c=1.7; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def herop(p):
    p=min(max(p,0),1); e=1-(1-p)**4
    return e+(np.sin((p-.6)/.4*np.pi)*-.012 if p>.6 else 0)
STEPS=[(1.9,-45,.9),(4.85,-90,.7),(7.45,-90,.7),(10.05,-90,.7),(12.6,-810,1.7)]
def rot(t):
    r=45
    for s,d,du in STEPS:
        p=(t-s)/du
        if p>0: r+=d*(herop(p) if du>1 else obp(p))
    return r
add(rumble(18.0),.0,.05)
add(whoosh(.9,150,700,300,.5,1.0),.1,.14); add(thud(90,40,.4,.2),.9,.35)
txt(.25,.07,-.3); txt(.42,.06,-.2)
# detent ticks: one per 5 degrees crossed
prev=rot(0)
for i in range(1,int(17*1000)):
    t=i/1000; r=rot(t)
    if int(np.floor(prev/5))!=int(np.floor(r/5)): add(tick(.8),t,.16 if t>12.5 else .22,.1)
    prev=r
for a in [2.3,5.15,7.75,10.35]:
    add(whoosh(.55,250,1400,500,.6,1.0),a-.1,.12)
    add(thud(100,44,.36,.28,11),a+.45,.45); add(clack(.6),a+.45,.18)
for a in [2.45,5.3,7.9,10.5]:
    txt(a,.07,-.3); txt(a+.1,.06,-.2); txt(a+.2,.05,-.1)
add(whoosh(1.7,300,2400,700,.35,.8),12.6,.18)
for i in range(4): add(slap(.12),12.75+i*.12+.4,.22,-.4+i*.27)
add(thud(80,36,.55,.3,8),14.3,.55)
txt(13.3,.08,-.3); txt(13.55,.07,-.2)
add(whoosh(.9,200,1000,320,.6,1.0),14.85,.16)
endcard(15.45)
master('sfx.wav')
