import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.035)
for a in [.25,.4,.55]: txt(a,.06,-.3)
txt(.95,.04,-.2)
def opening(t0,g=1.0):          # blinds tilt open: a quick ripple of slat ticks top to bottom
    add(whoosh(.7,500,1600,700,.5,1.0),t0,.08*g)
    for i in range(8): add(click(.8),t0+.35+i*.045,.22*g,-.4+i*.1)
def closing(t0,g=1.0):          # blinds slap shut, bottom to top
    add(whoosh(.5,1400,600,300,.4,1.0),t0,.08*g)
    for i in range(8): add(clack(.55),t0+.4+i*.045,.16*g,.4-i*.1)
    add(thud(95,42,.38,.25,11),t0+.55,.42*g); add(slap(.14),t0+.55,.16*g)
opening(2.45,1.1); add(thud(80,38,.5,.15,9),3.2,.3)
for a in [3.0,6.55,10.15]:
    txt(a,.06,-.3); txt(a+.1,.05,-.2); txt(a+.2,.04,-.1)
closing(5.45); opening(6.15)
closing(9.05); opening(9.75)
closing(12.45)
# hero spin
add(whoosh(1.0,250,1800,500,.55,.9),13.1,.16)
for k in range(22): add(tick(.8),13.25+k*.035,.16,-.3+(k%8)*.08)
add(thud(88,38,.55,.2,8),14.1,.55); add(shimmer(1.2,6000,.4),14.0,.08)
for i,a in enumerate([14.05,14.15,14.25]): add(clack(.7),a,.22,-.4+i*.4)
txt(14.2,.07,-.2); txt(14.32,.06,-.1)
closing(15.3,1.2)
endcard(15.8)
master('sfx.wav')
