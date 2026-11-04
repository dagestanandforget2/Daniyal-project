import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.06)
# hourglass rises, sand hiss (filtered noise via shimmer, low)
add(whoosh(.9,200,900,400,.5,1.0),.05,.16)
txt(.3,.08); txt(.45,.07); txt(1.0,.05)
for a,b in ((.3,3.2),(3.95,6.6),(7.3,9.9),(10.6,12.6)):
    add(shimmer(b-a,5200,.35),a,.03,.3)
# flips: whoosh then wooden landing
for f in (3.3,6.65,9.95):
    add(whoosh(.55,400,1800,700,.45,1.0),f,.16,sweep(whoosh(.55,400,1800,700,.45,1.0),-.3,.3))
    add(thud(110,50,.3,.3,12),f+.38,.38); add(clack(.6),f+.38,.14)
# books arrive / leave
for a,b in ((3.9,6.55),(7.25,9.85),(10.55,12.3)):
    add(whoosh(.6,300,1500,600,.5,1.0),a-.35,.14,-.3); add(clack(.5),a+.3,.08,-.3)
    txt(a,.08); txt(a+.2,.06); add(tick(.6),a+.4,.05)
    add(whoosh(.5,500,2000,800,.5,1.0),b,.12,sweep(whoosh(.5,500,2000,800,.5,1.0),-.2,-.7))
# hero: whip spin and spray
add(whoosh(1.1,250,2400,900,.35,1.0),12.85,.22)
add(slap(.2),13.05,.3); add(thud(85,38,.45,.3,9),13.05,.5); add(shimmer(1.2,7000,.6),13.05,.1)
for i in range(3): add(clack(.7),13.4+i*.09,.12,-.4+i*.4)
txt(13.75,.08); txt(13.9,.07)
# sand fills the screen
add(scrape(1.0),15.0,.18); add(whoosh(1.0,200,1200,400,.5,1.0),15.0,.2)
endcard(15.7)
master('sfx.wav')
