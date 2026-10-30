import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.05)
txt(.3,.07,-.3); txt(.45,.06,-.2); txt(.6,.06,-.1)
add(whoosh(.6,1500,500,300,.3,1.0),1.85,.08,-.4)
# feature books slide along the shelf
for a,n in [(2.1,1),(5.45,2),(8.75,1)]:
    for j in range(n):
        add(scrape(.75),a+j*.12,.22,.4)
        add(clack(.7),a+j*.12+.62,.25,0)
    txt(a+.45,.07,-.3); txt(a+.85,.06,-.2); txt(a+1.0,.05,-.2)
for e in [5.25,8.55,10.75]: add(whoosh(.6,1400,500,300,.35,1.0),e,.09,-.4)
# hero row
for i,a in enumerate([10.85,11.0,11.15,11.3]):
    add(scrape(.6),a,.15,.3); add(clack(.5),a+.62,.18,-.3+.2*i)
add(whoosh(.5,250,1200,500,.7,1.0),11.85,.14)
add(thud(100,38,.5,.45,8),12.5,.75); add(slap(.18),12.5,.4)
for i in range(4): add(clack(.8),12.5+.03*i,.2,-.45+.3*i)
txt(12.85,.07,-.3); txt(13.0,.06,-.2); txt(13.4,.05,-.2)
add(whoosh(.8,200,1000,350,.6,1.0),14.9,.14,.3)
endcard(15.7)
master('sfx.wav')
