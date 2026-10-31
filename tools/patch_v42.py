P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

# ---- 순서 복원: 히어로 → 로고 밴드. 로고 밴드가 첫 화면을 차지하고(히어로 높이 0), 애니메이션 후 히어로가 위에서 펼쳐져 밴드를 아래로 밀어냄 ----
bs = h.index('  <section class="band logo-band" id="brand" aria-label="신뢰">'); be = h.index('  </section>', bs) + len('  </section>')
band = h[bs:be]
h = h[:bs] + h[be:].lstrip('\n')
hs = h.index('  <noscript><style>.hero{grid-template-rows:1fr!important}'); he = h.index('  </section>', h.index('<section class="hero" id="hero"', hs)) + len('  </section>')
h = h[:he] + '\n\n' + band + h[he:]

# 히어로 내부: 하단 기준 정렬(아래부터 드러남 = 끌어내려지는 느낌), 배경은 최종 높이로 고정해 함께 내려옴
rep('.hero-in{min-height:0;overflow:hidden;position:relative}', '.hero-in{min-height:0;overflow:hidden;position:relative;display:grid;align-content:end}')
rep('.hero-media{position:absolute;inset:0;overflow:hidden}', '.hero-media{position:absolute;left:0;right:0;bottom:0;height:var(--heroH,100%);overflow:hidden}')
rep('.hero-text{opacity:0;transform:translateY(16px);transition:opacity .6s ease .45s,transform .6s ease .45s}', '.hero-text{opacity:0;transform:translateY(-14px);transition:opacity .6s ease .5s,transform .6s ease .5s}')
rep('/* 히어로 펼침: 로고 애니메이션이 끝나면 0 → 화면 하단까지 (가용 높이 − 헤더 − 로고 밴드, 최소 460px·최대 860px) */',
    '/* 히어로 펼침: 처음엔 높이 0(로고 밴드가 첫 화면). 로고 애니메이션이 끝나면 히어로가 위에서 펼쳐지며 로고 밴드를 아래로 밀어냄. 높이 = 가용 − 헤더 − 밴드(최소 420) → 펼친 뒤 밴드 하단이 화면 하단 */')

# JS: --heroH 계산
rep("  const size = () => { document.documentElement.style.setProperty('--lgH', band.offsetHeight + 'px'); document.documentElement.style.setProperty('--hdrH', (hdr ? hdr.offsetHeight : 76) + 'px'); };",
    "  const size = () => { const r = document.documentElement.style; r.setProperty('--lgH', band.offsetHeight + 'px'); r.setProperty('--hdrH', (hdr ? hdr.offsetHeight : 76) + 'px'); const w = hero.querySelector('.wrap'); if (w) r.setProperty('--heroH', w.offsetHeight + 'px'); };")
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
