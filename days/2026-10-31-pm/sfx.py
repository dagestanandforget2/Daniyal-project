import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.05)
txt(.3,.07,-.3); txt(.48,.06,-.2); txt(.66,.06,-.1)
add(whoosh(1.2,200,900,400,.5,1.0),1.3,.12)          # rahl rises
add(whoosh(.5,1500,500,300,.3,1.0),2.45,.07,-.3)
add(scrape(.5),3.0,.18,.2); add(thud(110,40,.45,.4,9),3.45,.6); add(clack(.8),3.45,.25)   # unfold
for a in [3.65,7.35,11.15]:
    add(whoosh(.5,300,1300,600,.6,1.0),a-.1,.1)
    add(thud(95,42,.38,.3,11),a+.55,.5); add(slap(.14),a+.55,.25)
for a in [4.3,8.1,11.9]:
    txt(a,.07,-.3); txt(a+.12,.06,-.2); txt(a+.24,.05,-.1)
for a in [7.0,10.8,14.05]: add(whoosh(.7,500,1600,800,.4,1.0),a,.11,.4)
add(clack(.7),14.6,.25); add(whoosh(.8,200,1000,350,.6,1.0),14.85,.14,.3)
endcard(15.35)
master('sfx.wav')
