import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.05)
for a,e in [(0,4.55),(4.75,8.55),(8.75,12.2)]:
    if a>0: add(whoosh(.5,1800,600,300,.25,1.0),a-.1,.12,.4)
    txt(a+.3,.07,-.3)
    add(shimmer(.6,5200,.4),a+.2,.05)          # rack focus
    add(whoosh(1.3,220,900,400,.55,1.0),a+1.35,.14)  # pull back
    add(flip(.5),a+1.9,.12,.2)
    add(tick(.8),a+2.45,.2,.3)                  # brackets snap
    for j in range(4): txt(a+2.3+j*.09,.05,-.2)
    add(whoosh(.5,1500,500,300,.3,1.0),e,.11,-.4)
add(whoosh(.5,1800,600,300,.25,1.0),12.5,.12,.4)
add(whoosh(1.1,180,700,300,.6,1.0),13.15,.16)
for j in range(5): add(flip(.4),13.95+j*.1,.1,-.4+.2*j); add(clack(.5),14.45+j*.1,.12,-.4+.2*j)
add(tick(.9),14.8,.22); txt(13.95,.07,-.3); txt(14.6,.06,-.2)
add(whoosh(.8,200,1000,350,.6,1.0),15.3,.14,.3)
endcard(15.85)
master('sfx.wav')
