import numpy as np, wave
SR=48000; T=int(__import__("os").environ.get("SFXT","20"))
L=np.zeros(SR*T); R=np.zeros(SR*T)
rng=np.random.default_rng(11)
def add(sig,t,gain=1.0,pan=0.0):
    i=int(t*SR)
    if i<0: sig=sig[-i:]; i=0
    n=min(len(sig),len(L)-i)
    if n<=0: return
    pan=np.asarray(pan,dtype=float)
    l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
    if pan.ndim>0: l=l[:n]; r=r[:n]
    L[i:i+n]+=sig[:n]*gain*l; R[i:i+n]+=sig[:n]*gain*r
def svf(x,fc,q=1.2,mode='bp'):
    out=np.zeros_like(x); lo=0.0; bd=0.0
    fc=np.broadcast_to(np.asarray(fc,dtype=float),x.shape)
    f=2*np.sin(np.pi*np.minimum(fc,SR/6.5)/SR); d=1.0/q
    for i in range(len(x)):
        lo+=f[i]*bd; hi=x[i]-lo-d*bd; bd+=f[i]*hi
        out[i]=bd if mode=='bp' else (lo if mode=='lp' else hi)
    return out
def env(n,a,shape=2.0):
    t=np.arange(n)/n; return np.where(t<a,(t/a)**1.5,((1-t)/(1-a))**shape)
def whoosh(dur,f0,f1,f2,peak=.5,q=1.0):
    n=int(dur*SR); t=np.arange(n)/n
    fc=np.where(t<peak,f0*(f1/f0)**(t/peak),f1*(f2/f1)**((t-peak)/(1-peak)))
    return svf(rng.standard_normal(n),fc,q)*env(n,peak,2.2)
def thud(f0=95,f1=42,dur=.38,click=.25,decay=11):
    n=int(dur*SR); t=np.arange(n)/SR
    f=f1+(f0-f1)*np.exp(-t*22); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*decay)
    c=svf(rng.standard_normal(n),1800.0,.8,'lp')*np.exp(-t*90)*click
    s[:48]*=np.linspace(0,1,48); return s+c
def beat(strength=1.0,gap=.15):     # lub-dub
    a=thud(120,58,.3,.18,16); b=thud(150,70,.24,.12,20)
    n=int(gap*SR)+len(b); s=np.zeros(max(n,len(a))); s[:len(a)]+=a; s[int(gap*SR):int(gap*SR)+len(b)]+=b*.75
    return s*strength
def flip(dur=.6):
    n=int(dur*SR); t=np.arange(n)/n
    fc=1400+4200*np.sin(np.pi*t)**1.5
    e=(np.sin(np.pi*t)**1.3)*(0.75+0.25*np.sin(2*np.pi*t*9+rng.uniform(0,6)))
    return svf(rng.standard_normal(n),fc,.9)*e + svf(rng.standard_normal(n),3200.0,.7)*np.exp(-np.abs(t-.86)*38)*.9
def shimmer(dur,f=6500,amt=.5):
    n=int(dur*SR); t=np.arange(n)/n
    return svf(rng.standard_normal(n),f+1800*t,.6,'hp')*(np.sin(np.pi*t)**2)*(.75+.25*np.sin(2*np.pi*t*dur*6))*amt
def scrape(dur):                    # a book dragged along wood
    n=int(dur*SR); t=np.arange(n)/n
    x=svf(rng.standard_normal(n),420+500*t,1.6)*(.6+.4*np.sin(2*np.pi*t*dur*23)**2)
    return x*env(n,.25,1.2)
def scratch(dur):                   # pen on paper
    n=int(dur*SR); t=np.arange(n)/n
    return svf(rng.standard_normal(n),2600+900*np.sin(2*np.pi*t*3),1.3)*env(n,.15,1.0)*(.55+.45*np.sin(2*np.pi*t*dur*17)**2)
def rumble(dur):
    n=int(dur*SR); x=svf(rng.standard_normal(n),90.0,1.2,'lp')+.25*svf(rng.standard_normal(n),320.0,.7)
    e=np.ones(n); k=int(1.2*SR); e[:k]=np.linspace(0,1,k); e[-k:]=np.linspace(1,0,k); return x*e
def pl(n,a,b): return np.linspace(a,b,n)
def sweep(sig,a,b): return pl(len(sig),a,b)


def txt(t,g=.085,p=0.0): add(whoosh(.45,800,1900,1000,.5,.9),t-.1,g,p)
def tick(g=1.0):
    n=int(.03*SR); tt=np.arange(n)/SR
    return (svf(rng.standard_normal(n),3400.0,1.6)*np.exp(-tt*240)+.5*np.sin(2*np.pi*190*tt)*np.exp(-tt*160))*g
def click(g=1.0):
    n=int(.025*SR); tt=np.arange(n)/SR
    return svf(rng.standard_normal(n),2500.0,2.0)*np.exp(-tt*400)*g
def slap(dur=.16):
    n=int(dur*SR); tt=np.arange(n)/SR
    return svf(rng.standard_normal(n),1300.0,.8,'lp')*np.exp(-tt*35)
def clack(g=1.0):   # hard book-on-book knock
    n=int(.12*SR); tt=np.arange(n)/SR
    return (svf(rng.standard_normal(n),900.0,2.5)*np.exp(-tt*55)+.6*np.sin(2*np.pi*140*tt)*np.exp(-tt*40))*g
def endcard(t0):
    w=whoosh(1.0,200,1100,320,.5,.9); add(w,t0-.3,.3)
    add(thud(82,36,.6,.14),t0+.05,.6); add(shimmer(1.6,6200,.6),t0-.1,.2)
    txt(t0+.4); add(thud(92,40,.4,.22),t0+1.05,.55); add(tick(1),t0+1.05,.4)
    for k in range(4):
        if t0+1.75+k*1.6<T-.3: add(tick(.6),t0+1.75+k*1.6,.22)
def master(out):
    pk=max(np.abs(L).max(),np.abs(R).max()); g=0.62/pk
    st=np.stack([np.tanh(L*g*1.2)/1.2,np.tanh(R*g*1.2)/1.2],1)
    k=int(.4*SR); st[-k:]*=np.linspace(1,0,k)[:,None]
    with wave.open(out,'wb') as w_:
        w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(SR); w_.writeframes((st*32767).astype('<i2').tobytes())
