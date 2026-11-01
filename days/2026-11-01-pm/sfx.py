import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.04)
txt(.3,.06,-.3); txt(.6,.06,-.2)
add(whoosh(.35,600,1500,900,.5,1.0),1.95,.06,.4)      # reach for chain
add(click(1.0),2.2,.5,.4); add(tick(1.0),2.24,.3,.4)  # chain pull
for a,g in [(2.36,.25),(2.49,.18),(2.6,.3)]: add(click(.6),a,g,.3)   # flicker
add(shimmer(1.4,5200,.35),2.6,.05,.2); add(rumble(1.2),2.6,.12)
add(scrape(.5),2.95,.14,-.1); add(thud(100,44,.4,.3,10),3.75,.55); add(slap(.14),3.75,.2)
for a in [6.0,9.4,12.6]: add(whoosh(.6,400,1400,700,.5,1.0),a,.1,-.3)
add(whoosh(.7,1500,500,300,.4,1.0),6.3,.09,.4); add(thud(90,42,.35,.3,11),7.15,.45)
add(whoosh(.6,300,1200,600,.6,1.0),9.7,.1); add(thud(85,40,.4,.35,10),10.35,.6); add(clack(.7),10.35,.2)
for a in [3.9,7.3,10.6]:
    txt(a,.06,-.3); txt(a+.12,.05,-.2); txt(a+.24,.05,-.1)
for a in [13.25,13.4,13.55]: add(clack(.6),a,.2)
txt(13.3,.07,-.2)
add(click(1.0),14.95,.5,.4); add(whoosh(.9,200,1100,400,.6,1.0),15.05,.13)
endcard(15.5)
master('sfx.wav')
