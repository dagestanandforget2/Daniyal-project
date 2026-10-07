"""Synthesised, noise-only sound design (whooshes, page flips, soft hits). No melody or instruments.
Event times mirror the timeline in src/film.js. Writes out/sfx.wav (44.1 kHz stereo)."""
import numpy as np, os
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
DUR = 57.0
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(7)
mix = np.zeros((int(SR * DUR), 2))


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f):
    return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f):
    return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), x)


def add(t0, x, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    n = min(len(x), len(mix) - i)
    if n <= 0:
        return
    l, r = gain * (1 - max(0, pan)), gain * (1 + min(0, pan))
    mix[i:i + n, 0] += x[:n] * l
    mix[i:i + n, 1] += x[:n] * r


def env(n, a, d_pow=2.0, peak=0.5):
    x = np.linspace(0, 1, n)
    e = np.where(x < peak, (x / peak) ** a, ((1 - x) / (1 - peak)) ** d_pow)
    return e


def whoosh(t0, dur, f0, f1, gain=0.5, pan=0.0, peak=0.5):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    # sweep the band centre from f0 to f1 by crossfading overlapping bands
    out = np.zeros(n)
    steps = 14
    for k in range(steps):
        a, b = int(n * k / steps), int(n * (k + 1) / steps)
        fc = f0 * (f1 / f0) ** ((k + .5) / steps)
        seg = bp(noise, fc * 0.7, min(fc * 1.4, SR / 2 - 100))
        w = np.zeros(n); w[a:b] = 1
        w = np.convolve(w, np.hanning(int(n / steps) + 1), "same") / (np.hanning(int(n / steps) + 1).sum() / (n / steps))
        out += seg * np.clip(w, 0, 1)
    out *= env(n, 2.2, 1.8, peak)
    out /= np.abs(out).max() + 1e-9
    add(t0, out, gain, pan)


def thud(t0, gain=0.6, f=170, dur=.35):
    n = int(dur * SR)
    x = lp(rng.standard_normal(n), f) * np.exp(-np.linspace(0, 1, n) * 9)
    x /= np.abs(x).max() + 1e-9
    add(t0, x, gain)
    add(t0, hp(rng.standard_normal(int(.03 * SR)), 2500) * np.exp(-np.linspace(0, 1, int(.03 * SR)) * 6), gain * .12)


def flip(t0, gain=0.5, pan=0.0):
    n = int(.42 * SR)
    x = rng.standard_normal(n)
    x = bp(x, 1800, 9000) * (env(n, .6, 2.6, .18))
    x2 = bp(rng.standard_normal(n), 300, 1200) * env(n, .6, 3.5, .1) * .35
    y = x + x2
    y /= np.abs(y).max() + 1e-9
    add(t0, y, gain, pan)


def swish(t0, dur, gain=0.28):
    """soft thread-draw shimmer: airy high noise with a slow swell"""
    n = int(dur * SR)
    x = hp(bp(rng.standard_normal(n), 3000, 11000), 3000) * env(n, 1.6, 1.6, .55)
    x /= np.abs(x).max() + 1e-9
    add(t0, x, gain)


def creak(t0, dur, gain=0.18):
    n = int(dur * SR)
    x = bp(rng.standard_normal(n), 280, 700)
    mod = .55 + .45 * np.sin(2 * np.pi * np.cumsum(np.linspace(5, 11, n)) / SR)
    x = x * mod * env(n, 1.2, 1.8, .5)
    x /= np.abs(x).max() + 1e-9
    add(t0, x, gain)


def swell(t0, dur, gain=0.35):
    n = int(dur * SR)
    x = bp(rng.standard_normal(n), 120, 900) + .4 * bp(rng.standard_normal(n), 900, 3500)
    x *= env(n, 1.8, 1.4, .35)
    x /= np.abs(x).max() + 1e-9
    add(t0, x, gain)


def tick(t0, gain=.22):
    n = int(.12 * SR)
    x = bp(rng.standard_normal(n), 1500, 5000) * np.exp(-np.linspace(0, 1, n) * 12)
    add(t0, x / (np.abs(x).max() + 1e-9), gain)


# ---- timeline ----
thud(0.12, .5); whoosh(0.1, 1.0, 400, 3000, .22)
swish(1.3, 1.1)
for t in (3.6, 4.9, 5.9): whoosh(t, .7, 500, 2500, .18); tick(t + .35, .1)
swish(6.2, .8)
# book entrance
whoosh(7.0, 2.7, 250, 3500, .55, pan=-.4, peak=.45)
whoosh(7.15, 2.6, 300, 3800, .5, pan=.4, peak=.45)
thud(9.5, .7, 150); thud(9.68, .65, 170)
for t in (10.3, 10.6): whoosh(t, .8, 700, 2200, .14)
for t in (11.2, 11.35): tick(t, .12)
swish(12.0, 1.1); whoosh(12.6, .7, 600, 2000, .12)
# pillars
whoosh(15.6, .9, 500, 1600, .3); thud(16.45, .35, 140)
for t in (16.6, 17.4, 18.2): whoosh(t, .6, 500, 2200, .16); thud(t + .3, .22, 200, .2)
swish(17.0, .6, .2); swish(17.8, .6, .2)
# English book
whoosh(19.4, 1.0, 400, 2800, .4, pan=-.5); whoosh(19.5, 1.2, 300, 1800, .4)
creak(20.8, 1.9, .2); whoosh(20.9, 1.8, 300, 1400, .26)
for i in range(4): flip(22.35 + .3 * i, .5, pan=-.2)
thud(23.1, .25, 120)
whoosh(24.0, 2.3, 250, 4200, .5, peak=.7)
swish(26.6, 1.1, .4); tick(26.6, .15); swish(27.6, .8, .4)
whoosh(30.0, .9, 1800, 400, .45, pan=.5, peak=.3)
# Arabic book
whoosh(30.5, 1.2, 300, 2400, .45, pan=-.5, peak=.6); thud(31.65, .5, 150)
creak(31.8, 1.8, .2); whoosh(31.9, 1.7, 300, 1400, .26)
for i in range(4): flip(33.3 + .3 * i, .5, pan=.2)
thud(34.3, .25, 120)
whoosh(34.7, 1.7, 250, 4200, .5, peak=.7)
swish(36.5, 1.1, .4); tick(36.5, .15)
whoosh(38.1, .8, 1800, 400, .4, pan=-.5, peak=.3)
# quotes
thud(38.9, .4, 130); whoosh(38.9, .9, 400, 1800, .2); swish(40.9, .7, .22); whoosh(40.2, .8, 400, 1800, .15)
thud(44.1, .4, 130); whoosh(44.2, 1.0, 400, 1800, .2); swish(46.2, .7, .22); whoosh(45.8, .8, 400, 1800, .15)
# closing
whoosh(49.6, 1.9, 300, 3200, .5, pan=-.5, peak=.5); whoosh(49.7, 1.9, 300, 3400, .45, pan=.5, peak=.5)
thud(51.4, .6, 150); thud(51.55, .55, 170)
swish(51.2, .9, .25); whoosh(50.0, .7, 500, 2000, .14)
whoosh(52.6, 1.0, 1500, 300, .4, peak=.3)
# end card
swell(53.0, 3.5, .38); swish(53.2, 1.5, .3); thud(54.1, .6, 110); tick(54.1, .15); whoosh(54.5, 1.0, 600, 2400, .12)
swell(55.0, 2.0, .15)

# ---- master: gentle limiter, moderate level, fades ----
peak = np.abs(mix).max()
mix = mix / peak * 0.55
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
fade = np.ones(len(mix)); n = int(1.2 * SR); fade[-n:] = np.linspace(1, 0, n); fade[:int(.02 * SR)] = np.linspace(0, 1, int(.02 * SR))
mix *= fade[:, None]
os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
wavfile.write(os.path.join(ROOT, "out/sfx.wav"), SR, (mix * 32767).astype(np.int16))
print("wrote out/sfx.wav", len(mix) / SR, "s; rms", float(np.sqrt((mix ** 2).mean())))
