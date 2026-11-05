import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.06)
txt(.3,.08); txt(.45,.07); txt(1.0,.05)
# two knocks on the door
add(thud(140,70,.25,.5,16),1.85,.45); add(clack(.7),1.85,.12)
add(thud(140,70,.25,.5,16),2.12,.45); add(clack(.7),2.12,.12)
# heavy doors swing open, light floods in
add(whoosh(1.1,150,700,300,.5,1.0),2.6,.22)
add(scrape(.9),2.65,.08)
add(thud(80,38,.5,.3,8),3.25,.5); add(shimmer(1.4,6500,.5),2.8,.08)
add(whoosh(1.2,200,1100,500,.5,1.0),3.0,.14)
# books come out of the light and go back in
for a,b in ((4.1,6.95),(7.1,9.95),(10.1,12.8)):
    add(whoosh(.7,250,1400,600,.5,1.0),a-.3,.15); add(clack(.45),a+.35,.07)
    txt(a,.08); txt(a+.2,.06); add(tick(.6),a+.45,.05)
    add(whoosh(.6,700,2000,400,.5,1.0),b-.15,.12)
# pull back, three books step into the doorway
add(whoosh(1.0,200,900,400,.5,1.0),12.85,.16)
for i in range(3): add(clack(.55),13.85+i*.14,.08,-.3+i*.3)
txt(13.8,.08); txt(13.95,.07)
# doors swing shut
add(whoosh(.6,200,900,300,.5,1.0),15.1,.18)
add(thud(75,34,.55,.35,7),15.65,.6); add(slap(.18),15.65,.22)
endcard(15.85)
master('sfx.wav')
