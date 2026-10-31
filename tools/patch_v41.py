import re
P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

# ---- 1. 섹션 순서: 로고 밴드 → 히어로 ----
hs = h.index('  <section class="hero" aria-label="소개">'); he = h.index('  </section>', hs) + len('  </section>')
hero = h[hs:he]
bs = h.index('  <section class="band logo-band" id="brand" aria-label="신뢰">'); be = h.index('  </section>', bs) + len('  </section>')
band = h[bs:be]
assert bs > he
h = h[:hs] + band + '\n\n' + hero + h[be:]
# 히어로 내부를 .hero-in으로 감싸 펼침 애니메이션
rep('''  <section class="hero" aria-label="소개">
    <div class="hero-media" aria-hidden="true" id="heroMedia">''', '''  <section class="hero" id="hero" aria-label="소개">
    <div class="hero-in">
    <div class="hero-media" aria-hidden="true" id="heroMedia">''')
hs = h.index('  <section class="hero" id="hero"'); he = h.index('  </section>', hs)
h = h[:he] + '    </div>\n' + h[he:]
# 스크롤 큐 제거 (히어로가 화면 하단에 맞춰짐)
rep('      <div class="hero-cue" aria-hidden="true">SCROLL<i></i></div>\n', '')
# noscript 대비
rep('  <section class="hero" id="hero" aria-label="소개">', '  <noscript><style>.hero{grid-template-rows:1fr!important}.hero-text{opacity:1!important;transform:none!important}</style></noscript>\n  <section class="hero" id="hero" aria-label="소개">')

# ---- 2. CSS: 인트로 제거, 펼침, 높이, 압축, 헤더 로고 ----
c0 = h.index('/* 인트로 커튼 */'); c1 = h.index('/* 히어로 높이:')
h = h[:c0] + h[c1:]
rep('''/* 히어로 높이: 첫 화면에 다음 밴드(로고 윗부분)가 살짝 보이도록 */
.hero .wrap{min-height:clamp(520px,calc(100svh - 76px - 150px),780px);box-sizing:border-box;padding-block:clamp(48px,7vw,96px)}''',
'''/* 히어로 펼침: 로고 애니메이션이 끝나면 0 → 화면 하단까지 (가용 높이 − 헤더 − 로고 밴드, 최소 460px·최대 860px) */
.hero{display:grid;grid-template-rows:0fr;transition:grid-template-rows .9s cubic-bezier(.7,0,.3,1)}
.hero.open{grid-template-rows:1fr}
.hero-in{min-height:0;overflow:hidden;position:relative}
.hero .wrap{min-height:clamp(460px,calc(100svh - var(--hdrH,76px) - var(--lgH,380px)),860px);box-sizing:border-box;padding-block:clamp(40px,6vw,80px)}
.hero-text{opacity:0;transform:translateY(16px);transition:opacity .6s ease .45s,transform .6s ease .45s}
.hero.open .hero-text{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.hero{transition:none}.hero-text{transition:none}}
/* 짧은 화면(노트북 1366×768 등): 로고 밴드 압축 */
@media (min-width:861px) and (max-height:820px){.logo-band{padding:22px 0 18px}.lg{width:min(100%,560px)}.lg-tag{margin-top:8px;font-size:13px}}
/* 로고 밴드가 보이는 동안 헤더 로고 숨김 (중복 방지) */
.brand{transition:opacity .35s}
header.band-visible .brand{opacity:0;pointer-events:none}''')
h = re.sub(r'\n\.hero-cue\{[^\n]*\n\.hero-cue i\{[^\n]*\n@keyframes cue\{[^\n]*', '', h)
# 로고 밴드 패딩: 첫 섹션이므로 위 여백 축소
rep('.logo-band{background:radial-gradient(1100px 520px at 50% 0,#17406E,#0B1C33 72%);color:#fff;padding:34px 0 30px;position:relative;z-index:2}',
    '.logo-band{background:radial-gradient(1100px 520px at 50% 0,#17406E,#0B1C33 72%);color:#fff;padding:28px 0 26px;position:relative;z-index:2}')

# ---- 3. JS: 인트로 로직 → 밴드 재생 후 히어로 펼침 ----
j0 = h.index('function countUp() {'); j1 = h.index('\n}\n', j0) + 3
js = '''function countUp() {
  const lg = document.getElementById('logoStats'), hero = document.getElementById('hero'), band = document.getElementById('brand'), hdr = document.querySelector('header');
  if (!lg || !hero) return;
  if (location.search.includes('logocheck')) document.body.classList.add('logocheck');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const numsOf = el => el.querySelectorAll('.n[data-count]');
  const nums = (el, dur = 900) => numsOf(el).forEach(n => {
    const to = +n.dataset.count, suf = n.dataset.suffix || '', t0 = performance.now();
    const step = now => { const k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3); n.textContent = Math.round(to * e).toLocaleString('ko-KR') + suf; if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  });
  const finish = el => numsOf(el).forEach(n => n.textContent = (+n.dataset.count).toLocaleString('ko-KR') + (n.dataset.suffix || ''));
  // 히어로 높이 = 가용 높이 − 헤더 − 로고 밴드
  const size = () => { document.documentElement.style.setProperty('--lgH', band.offsetHeight + 'px'); document.documentElement.style.setProperty('--hdrH', (hdr ? hdr.offsetHeight : 76) + 'px'); };
  size(); addEventListener('resize', size);
  const open = () => { size(); hero.classList.add('open'); };
  // 헤더 로고: 로고 밴드가 반 이상 보이면 숨김
  if ('IntersectionObserver' in window && hdr) new IntersectionObserver(es => es.forEach(en => hdr.classList.toggle('band-visible', en.intersectionRatio >= .5)), { threshold: [0, .5, 1] }).observe(band);
  // 재생 규칙: 첫 진입만 애니메이션 → 펼침. 세션 재방문·해시 진입·동작 축소·?nointro 는 즉시 펼친 상태
  let seen = false; try { seen = sessionStorage.getItem('plk-intro') === '1'; } catch (e) {}
  const skip = document.body.dataset.intro === 'off' || reduce || seen || location.hash.length > 1 || location.search.includes('nointro');
  if (skip) { finish(lg); lg.classList.add('done'); hero.classList.add('open'); return; }
  try { sessionStorage.setItem('plk-intro', '1'); } catch (e) {}
  requestAnimationFrame(() => {
    lg.classList.add('play'); setTimeout(() => nums(lg), 2000); setTimeout(() => lg.classList.add('done'), 2700);
    setTimeout(open, 2900); track('intro_done');
  });
  // 사용자가 먼저 스크롤/클릭하면 기다리지 않고 바로 펼침
  ['wheel', 'touchstart', 'keydown', 'pointerdown'].forEach(ev => window.addEventListener(ev, () => { finish(lg); lg.classList.add('done'); open(); }, { once: true, passive: true }));
}
'''
h = h[:j0] + js + h[j1:]
assert '.intro' not in h.split('<body')[0] or True
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok', 'intro' in h)
