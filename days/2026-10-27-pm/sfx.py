import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.05)
# drawer slides out toward camera
add(scrape(1.0),.05,.12); add(thud(90,40,.4,.2,12),1.0,.5)
txt(.15,.07,-.3); txt(.3,.06,-.3)
# riffles: one tick per card passed
SUB=[(1.4,0,3,.85),(5.6,3,8,.85),(9.8,8,13,1.0)]
for A,a,b,d in SUB:
    n=b-a
    for k in range(n):
        tt=A+d*(k+.6)/n; add(click(1),tt,.35,-.1+.05*k); add(tick(.6),tt+.01,.18)
    add(clack(.8),A+d,.25)
    add(whoosh(.6,400,1500,600,.5,1.0),A+.95,.12)      # card lifts out
    for j in range(22): add(click(.7),A+1.35+j*.07,.10,.2)  # typewriter
    w=whoosh(.8,250,1200,450,.5,1.0); add(w,A+1.85,.13); add(thud(110,48,.35,.25,12),A+2.6,.38)
    txt(A+.8,.07,-.3)
    add(whoosh(.5,1800,600,300,.3,1.0),A+3.55,.1)
w=whoosh(1.0,300,1300,500,.5,1.0); add(w,13.9,.2)
endcard(14.45)
master('sfx.wav')
