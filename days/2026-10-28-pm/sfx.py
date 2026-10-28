import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.05)
# tiles pop in radially
for j in range(14): add(click(.6),.1+j*.045,.10,-.3+.045*j)
txt(.4,.07,-.3); txt(.95,.06,-.3)
# four tile waves: rippling clacks along the diagonal
for F in [2.55,6.85,10.75,14.55]:
    add(whoosh(1.2,300,1400,500,.5,1.0),F,.12)
    for d in range(16): add(tick(.5),F+.3+d*.055,.13,-.4+.05*d)
# books lift out of the mosaic and settle back
for a,e in [(3.95,6.55),(8.15,10.45),(12.05,14.35)]:
    add(whoosh(.9,250,1100,450,.5,1.0),a,.14); add(thud(100,45,.38,.25,11),a+.95,.42)
    txt(a+.55,.07,-.2); txt(a+.85,.05,-.2)
    add(whoosh(.6,1500,500,300,.3,1.0),e-.7,.09); add(clack(.6),e,.18)
endcard(15.35)
master('sfx.wav')
