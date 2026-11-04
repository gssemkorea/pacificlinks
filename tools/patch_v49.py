"""v49: 시작 인트로 제거 — 히어로(CF)가 처음부터 펼쳐진 상태, 로고 애니메이션은 스크롤해서 로고 밴드가 화면에 들어올 때 재생"""
P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)
rep('<section class="hero" id="hero" aria-label="소개">', '<section class="hero open" id="hero" aria-label="소개">')
a = h.index("  const open = () => { size(); if (hero.classList.contains('open')) return;")
b = h.index("\n}\n", a)
h = h[:a] + '''  // 시작 인트로 없음: 히어로(CF)는 처음부터 펼쳐짐. 로고 애니메이션은 로고 밴드가 화면에 절반 이상 들어올 때 1회 재생
  if (reduce || !('IntersectionObserver' in window)) { finish(lg); lg.classList.add('done'); return; }
  const io = new IntersectionObserver(es => es.forEach(en => {
    if (!en.isIntersecting) return; io.disconnect();
    lg.classList.add('play'); setTimeout(() => nums(lg), 2000); setTimeout(() => lg.classList.add('done'), 2700); track('logo_anim_view');
  }), { threshold: .5 });
  io.observe(lg);''' + h[b:]
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
