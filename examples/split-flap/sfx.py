import os, json; os.environ['SFXT']='18'
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
def flap(g=1.0):  # small plastic flap clack
    n=int(.03*SR); tt=np.arange(n)/SR
    return (svf(rng.standard_normal(n),rng.uniform(2600,3800),2.2)*np.exp(-tt*260)+.35*svf(rng.standard_normal(n),900.0,1.5)*np.exp(-tt*200))*g
def bigflap():
    n=int(.12*SR); tt=np.arange(n)/SR
    return svf(rng.standard_normal(n),700.0,1.2)*np.exp(-tt*45)+.6*svf(rng.standard_normal(n),2400.0,1.6)*np.exp(-tt*120)
add(rumble(17.6),.1,.1)
F=json.load(open('/home/claude/f/flips.json'))
for t in F: add(flap(rng.uniform(.6,1)),t,.05,rng.uniform(-.6,.6))
for s in (0.15,3.0,5.8,8.6,11.4,14.0):
    add(bigflap(),s+.25,.45); add(bigflap(),s+.25+.17,.35); add(thud(110,55,.25,.25,16),s+.25+.34,.3)
add(thud(92,40,.4,.22),14.6,.5); add(tick(1),14.6,.3); add(shimmer(1.4,6200,.5),14.5,.1)
for k in range(2): add(tick(.6),15.4+k*1.6,.18)
master('sfx.wav')
