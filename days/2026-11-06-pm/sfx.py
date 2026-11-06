import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.05)
# machine rises
add(whoosh(1.0,120,600,250,.5,1.0),.1,.18); add(thud(90,40,.4,.3,9),1.0,.35)
txt(.3,.08); txt(.45,.07)
for a in (2.0,5.4,8.8):
    add(tick(.7),a+.15,.07); add(tick(.7),a+.3,.07); add(click(.8),a+.45,.08)
    add(scrape(.6),a+.5,.07)                       # coil turns
    add(whoosh(.35,300,900,400,.5,1.0),a+1.15,.08)  # tips and falls
    add(thud(110,50,.35,.45,12),a+1.55,.45); add(clack(.6),a+1.55,.1)
    add(whoosh(.6,250,1400,600,.5,1.0),a+1.6,.14)
    txt(a+1.65,.08); txt(a+1.8,.06)
    add(whoosh(.5,700,2000,400,.5,1.0),a+3.05,.11)
# hero: can't decide, all three coils spin, triple drop, burst up
txt(12.35,.08); txt(12.5,.07)
for i,d in enumerate((12.5,12.65,12.85)): add(tick(.8),d,.08)
add(click(.9),12.9,.1)
add(scrape(.8),12.95,.12,-.3); add(scrape(.8),12.97,.1,.3)
add(whoosh(.5,300,1000,400,.5,1.0),13.3,.12)
add(thud(75,34,.55,.35,7),13.68,.65); add(slap(.18),13.68,.2)
for i in range(3): add(clack(.55),13.7+i*.05,.08,-.3+i*.3)
add(whoosh(.8,200,1600,600,.5,1.0),13.75,.18)
txt(14.25,.08); txt(14.4,.07)
# roller shutter
add(scrape(.55),15.4,.12); add(whoosh(.55,200,800,300,.5,1.0),15.4,.12)
add(slap(.2),15.95,.25); add(thud(85,40,.4,.3,9),15.95,.35)
endcard(16.0)
master('sfx.wav')
