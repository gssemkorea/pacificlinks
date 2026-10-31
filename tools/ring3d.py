"""로고 고리를 '튜브'로 셰이딩해 입체 PNG로 굽는다 (원본 측정값: 중심 183/363.5/544, y126.5, 안57·밖125, 분할띠 y121.5~131.5)."""
import numpy as np, sys
from PIL import Image

C = [183.0, 363.5, 544.0]; CY = 126.5; RI, RO = 57.0, 125.0
LT = np.array([104, 171, 228.]); DK = np.array([22, 89, 158.])
COL = {(0, 'T'): LT, (0, 'B'): DK, (1, 'T'): DK, (1, 'B'): LT, (2, 'T'): LT, (2, 'B'): DK}

def render(p, out, W=726, H=262, S=4, OUT_SCALE=2):
    ys, xs = np.mgrid[0:H*S, 0:W*S].astype(np.float32)
    x = (xs + .5) / S; y = (ys + .5) / S
    top = y < CY
    d = [np.hypot(x - c, y - CY) for c in C]
    inside = [(di >= RI) & (di <= RO) for di in d]
    # 사슬 z순서: 위 반원은 왼쪽 고리가 위(우선순위 0>1>2), 아래 반원은 오른쪽 고리가 위(2>1>0)
    owner = np.full(x.shape, -1, np.int8)
    for k in (2, 1, 0):   # 위 반원: 나중에 쓴 쪽(0)이 이김
        owner[top & inside[k]] = k
    for k in (0, 1, 2):   # 아래 반원: 2가 이김
        owner[~top & inside[k]] = k
    gap = (y >= 121.5) & (y <= 131.5)
    owner[gap] = -1
    rgb = np.zeros(x.shape + (3,), np.float32); alpha = (owner >= 0).astype(np.float32)
    L = np.array([-.45, -.75, .9]); L /= np.linalg.norm(L)
    Hh = L + np.array([0, 0, 1.]); Hh /= np.linalg.norm(Hh)
    for k in range(3):
        m = owner == k
        if not m.any(): continue
        dk = d[k][m]; dx = (x[m] - C[k]) / dk; dy = (y[m] - CY) / dk
        u = (dk - RI) / (RO - RI); th = (u - .5) * np.pi * p['curve']
        nr = np.sin(th); nz = np.cos(th)
        nx, ny = nr * dx, nr * dy
        diff = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
        spec = np.clip(nx * Hh[0] + ny * Hh[1] + nz * Hh[2], 0, 1) ** p['shin']
        shade = p['amb'] + p['dif'] * diff
        # 분할 띠 가장자리 살짝 어둡게(절단면)
        eg = np.minimum(np.abs(y[m] - 121.5), np.abs(y[m] - 131.5))
        shade *= 1 - p['cut'] * np.exp(-eg / 2.2)
        # 접촉 그림자: 이 픽셀 위에 오는 고리 가장자리 근처를 어둡게
        occ = np.ones_like(dk)
        tm = top[m]
        for j in range(3):
            if j == k: continue
            above = np.where(tm, j < k, j > k)   # 위 반원은 왼쪽이 위, 아래 반원은 오른쪽이 위
            dj = d[j][m]
            e = np.where(dj > RO, dj - RO, np.where(dj < RI, RI - dj, 0))
            near = above & (e > 0)
            occ = np.where(near, occ * (1 - p['occ'] * np.exp(-e / p['occw'])), occ)
        base = np.empty((m.sum(), 3), np.float32)
        for half, msk in (('T', tm), ('B', ~tm)):
            base[msk] = COL[(k, half)]
        col = base * (shade * occ)[:, None] + 255 * (spec * p['spe'] * occ)[:, None]
        rgb[m] = col
    rgb = np.clip(rgb, 0, 255)
    img = np.dstack([rgb, alpha[..., None] * 255]).astype(np.uint8)
    im = Image.fromarray(img, 'RGBA')
    # 프리멀티플라이 후 축소(가장자리 번짐 방지)
    pm = np.array(im).astype(np.float32); pm[..., :3] *= pm[..., 3:4] / 255
    small = Image.fromarray(pm.astype(np.uint8), 'RGBA').resize((W * OUT_SCALE, H * OUT_SCALE), Image.LANCZOS)
    sm = np.array(small).astype(np.float32); a = np.maximum(sm[..., 3:4], 1)
    sm[..., :3] = np.clip(sm[..., :3] * 255 / a, 0, 255)
    Image.fromarray(sm.astype(np.uint8), 'RGBA').save(out, optimize=True)

PRESETS = {
  'soft':  dict(curve=1.0, amb=.62, dif=.45, spe=.28, shin=28, cut=.18, occ=.32, occw=7),
  'gloss': dict(curve=1.0, amb=.50, dif=.62, spe=.62, shin=55, cut=.22, occ=.42, occw=8),
}
if __name__ == '__main__':
    for k in sys.argv[2:] or PRESETS:
        render(PRESETS[k], f'{sys.argv[1]}/rings3d-{k}.png')
        print('ok', k)
