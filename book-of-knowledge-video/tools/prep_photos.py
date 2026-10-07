"""Perspective-correct, crop and even out the lighting of the book photos.

Corner coordinates are in the 900x1200 preview space of the 1932x2576 originals
(TL, TR, BR, BL). Output goes to src/assets/photos/.
Run: python3 -I tools/prep_photos.py   (from the project root)
"""
import cv2, numpy as np, os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src/assets/orig")
DST = os.path.join(ROOT, "src/assets/photos")
os.makedirs(DST, exist_ok=True)
K = 1932 / 900.0

# name: (quad, out_w, out_h, flatten strength 0..1, kind)
JOBS = {
    "en-front": ([(197, 212), (745, 217), (812, 1113), (143, 1100)], 1200, 1800, 0.5, "cover"),
    "en-back": ([(103, 64), (772, 98), (808, 1128), (78, 1118)], 1200, 1800, 0.6, "cover"),
    "en-spine": ([(405, 70), (505, 70), (500, 1158), (373, 1158)], 190, 1800, 0.3, "cover"),
    "ar-front": ([(98, 62), (822, 68), (868, 1160), (45, 1158)], 1200, 1760, 0.4, "cover"),
    "ar-back": ([(207, 250), (662, 248), (686, 960), (150, 950)], 1200, 1760, 0.9, "cover"),
    "ar-spine": ([(380, 40), (474, 40), (447, 1190), (316, 1190)], 165, 1760, 0.3, "cover"),
    "en-page-definition": ([(97, 38), (862, 38), (877, 1200), (40, 1200)], 1500, 2230, 1.0, "page"),
    "ar-page-definition": ([(113, 95), (810, 92), (838, 1200), (42, 1200)], 1500, 2180, 1.0, "page"),
}

# glare blobs to inpaint (preview coords: cx, cy, rx, ry)
GLARE = {
    "en-front": [(262, 668, 85, 70), (437, 735, 50, 50)],
}


def flatten(img, strength, kind):
    if strength <= 0:
        return img
    f = img.astype(np.float32)
    if kind == "cover":
        # low-frequency correction: remove broad glare/shadow, keep texture and detail
        low = cv2.GaussianBlur(f, (0, 0), 160)
        out = f - strength * (low - low.reshape(-1, 3).mean(0))
        return np.clip(out, 0, 255).astype(np.uint8)
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    k = 61 if kind == "page" else 151
    bg = cv2.morphologyEx(g, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    bg = cv2.GaussianBlur(bg, (0, 0), k / 3).astype(np.float32)
    bg = np.maximum(bg, 20)
    target = np.percentile(bg, 85 if kind == "page" else 50)
    gain = target / bg
    gain = 1 + (gain - 1) * strength
    out = f * gain[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


# highlight rectangles on the page photos, preview coords (x0, y0, x1, y1)
HILITE = {
    "en-page-definition": [(172, 738, 726, 768), (172, 770, 620, 803)],
    "ar-page-definition": [(412, 648, 698, 678)],
}


def main():
    hl = {}
    for name, (quad, w, h, strength, kind) in JOBS.items():
        img = cv2.imread(os.path.join(SRC, name + ".jpg"))
        for (cx, cy, rx, ry) in GLARE.get(name, []):
            m = np.zeros(img.shape[:2], np.uint8)
            cv2.ellipse(m, (int(cx * K), int(cy * K)), (int(rx * K), int(ry * K)), 0, 0, 360, 255, -1)
            m = cv2.GaussianBlur(m, (0, 0), 28).astype(np.float32)[..., None] / 255.0
            f = img.astype(np.float32)
            wt = 1 - np.clip(m * 3, 0, 1)
            low = cv2.GaussianBlur(f * wt, (0, 0), 60) / np.maximum(cv2.GaussianBlur(wt[..., 0], (0, 0), 60)[..., None], 1e-3)
            detail = f - cv2.GaussianBlur(f, (0, 0), 6)
            fixed = low + detail * 0.8
            img = np.clip(f * (1 - m) + fixed * m, 0, 255).astype(np.uint8)
        src = np.float32([(x * K, y * K) for x, y in quad])
        dst = np.float32([(0, 0), (w, 0), (w, h), (0, h)])
        M = cv2.getPerspectiveTransform(src, dst)
        out = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        out = flatten(out, strength, kind)
        if kind == "page":
            out = cv2.resize(out, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LANCZOS4)
            blur = cv2.GaussianBlur(out, (0, 0), 2.2)
            out = cv2.addWeighted(out, 1.6, blur, -0.6, 0)
            for (x0, y0, x1, y1) in HILITE.get(name, []):
                pts = np.float32([[[x0 * K, y0 * K], [x1 * K, y0 * K], [x1 * K, y1 * K], [x0 * K, y1 * K]]])
                q = cv2.perspectiveTransform(pts, M)[0]
                hl.setdefault(name, []).append([float(q[:, 0].min() / w), float(q[:, 1].min() / h), float(q[:, 0].max() / w), float(q[:, 1].max() / h)])
        cv2.imwrite(os.path.join(DST, name + ".jpg"), out, [cv2.IMWRITE_JPEG_QUALITY, 92])
        print(name, out.shape)
    json.dump(hl, open(os.path.join(ROOT, "src/assets/highlights.json"), "w"))


if __name__ == "__main__":
    main()
