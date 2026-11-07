import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.4),.1,.04)
# pad drops in
add(whoosh(.6,150,700,300,.5,1.0),.05,.15); add(thud(95,42,.4,.3,10),.65,.4); add(slap(.14),.65,.12)
txt(.35,.08); txt(.5,.07); txt(.9,.05)
# books drop and stand
for a in (2.45,5.85,9.25):
    add(whoosh(.45,300,1100,500,.5,1.0),a,.1)
    add(thud(110,50,.35,.4,12),a+.42,.4); add(clack(.6),a+.42,.08)
    txt(a+.45,.08); txt(a+.6,.06)
for a,o in ((5.15,4.75),(8.55,8.15),(11.35,11.05)):
    add(whoosh(.55,400,1500,500,.5,1.0),a,.1,-.4); add(scrape(.4),a,.05)
# single tears
for a in (5.25,8.65): add(flip(.6),a,.22); add(scratch(.35),a,.1)
# flurry
for i in range(27):
    q=i/26; s=11.55+1.4*(1-(1-q)**1.6)
    add(flip(.45),s,.12,(-1)**i*.35); add(tick(.5),s,.05)
add(whoosh(1.6,200,2400,700,.5,.9),11.5,.16)
# hero landing
txt(13.3,.08); txt(13.75,.08)
for k,a in enumerate((13.35,13.6,13.85)):
    add(whoosh(.4,300,1200,500,.5,1.0),a-.42,.08); add(thud(90-k*8,40,.45,.35,9),a,.5); add(clack(.7),a,.1,(k-1)*.4)
# last page tears, pad fills screen
add(flip(.7),14.85,.25); add(whoosh(.8,180,900,300,.5,1.0),15.1,.16)
endcard(15.75)
master('sfx.wav')
