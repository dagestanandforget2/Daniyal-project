import os; os.environ.setdefault('SFXT','18')
import sys; sys.path.insert(0,'../../tools'); from sfxlib import *
add(rumble(18.0),.0,.05)
# grid sweep + title
add(whoosh(1.3,300,1500,600,.4,1.0),.0,.1); txt(.3,.08,-.3); txt(.95,.06,-.3)
# pattern paper slides in, panel slides in
add(scrape(.9),2.4,.12,-.2); txt(3.15,.07,-.3)
add(scrape(1.0),4.0,.14,.4); add(slap(),4.95,.25,.2)
txt(6.45,.07,-.3)
# sewing: rapid needle clicks while the stitch runs
for k in range(int(2.0*22)): add(tick(.55),6.72+k/22,.12,.1)
add(thud(95,42,.4,.2,11),8.72,.5); add(clack(.7),8.72,.2)
txt(8.95,.06,-.3)
# tape measure unrolls
add(whoosh(1.1,600,2400,900,.5,1.2),10.45,.12,-.4)
for k in range(5): add(click(.7),10.85+k*.17,.18,-.4+.2*k)
txt(10.75,.07,-.3)
# split panels
add(slap(),13.35,.35,-.3); add(slap(),13.5,.35,.3); txt(13.75,.06,-.3); txt(14.0,.06,.3)
add(whoosh(.7,400,1600,500,.5,1.0),15.15,.14)
endcard(15.45)
master('sfx.wav')
