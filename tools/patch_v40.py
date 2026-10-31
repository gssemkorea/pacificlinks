P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

# ---- 1. 인트로 커튼: 첫 방문 시 로고 애니메이션을 전체 화면에서 먼저 보여주고, 커튼이 위로 걷히며 히어로 등장 ----
rep('.hero-slides{position:absolute;inset:0}', '''.hero-slides{position:absolute;inset:0}
/* 인트로 커튼 */
.intro{position:fixed;inset:0;z-index:1000;color:#fff;background:radial-gradient(1100px 620px at 50% 30%,#17406E,#0B1C33 72%);display:grid;place-items:center;padding:24px;transform:translateY(0);transition:transform .85s cubic-bezier(.7,0,.3,1)}
.intro.leave{transform:translateY(-102%)}
.intro-box{display:grid;justify-items:center;gap:6px;width:100%}
.intro .lg{width:min(100%,780px)}
.intro .lg-tag{color:#B5C4D6}
.intro .skip{position:absolute;right:22px;bottom:22px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);color:#fff;border-radius:999px;padding:8px 14px;font-size:13px;font-weight:700;cursor:pointer;opacity:0;transition:opacity .4s}
.intro.ready .skip{opacity:1}
body.intro-on{overflow:hidden}
/* 히어로 높이: 첫 화면에 다음 밴드(로고 윗부분)가 살짝 보이도록 */
.hero .wrap{min-height:clamp(520px,calc(100svh - 76px - 150px),780px);box-sizing:border-box;padding-block:clamp(48px,7vw,96px)}
.hero-cue{position:absolute;left:50%;bottom:16px;transform:translateX(-50%);color:rgba(255,255,255,.75);font-size:12px;letter-spacing:.14em;display:flex;flex-direction:column;align-items:center;gap:4px;pointer-events:none}
.hero-cue i{width:18px;height:18px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg);animation:cue 1.6s ease-in-out infinite}
@keyframes cue{0%,100%{transform:translateY(0) rotate(45deg);opacity:.5}50%{transform:translateY(6px) rotate(45deg);opacity:1}}''')
rep('    <div class="wrap">\n      <div class="hero-text">', '    <div class="wrap">\n      <div class="hero-cue" aria-hidden="true">SCROLL<i></i></div>\n      <div class="hero-text">')

# JS: 인트로 + 밴드 재생 규칙
j0 = h.index('function countUp() {'); j1 = h.index('\n}\n', j0) + 3
js = '''function countUp() {
  const lg = document.getElementById('logoStats'); if (!lg) return;
  if (location.search.includes('logocheck')) document.body.classList.add('logocheck');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const numsOf = el => el.querySelectorAll('.n[data-count]');
  const nums = (el, dur = 900) => numsOf(el).forEach(n => {
    const to = +n.dataset.count, suf = n.dataset.suffix || '', t0 = performance.now();
    const step = now => { const k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3); n.textContent = Math.round(to * e).toLocaleString('ko-KR') + suf; if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  });
  const finish = el => numsOf(el).forEach(n => n.textContent = (+n.dataset.count).toLocaleString('ko-KR') + (n.dataset.suffix || ''));
  const play = el => { el.classList.add('play'); setTimeout(() => nums(el), 2000); setTimeout(() => el.classList.add('done'), 2700); };
  const playOnScroll = () => {
    if (reduce || !('IntersectionObserver' in window)) { finish(lg); lg.classList.add('done'); return; }
    const io = new IntersectionObserver(es => es.forEach(en => { if (!en.isIntersecting) return; io.disconnect(); play(lg); }), { threshold: .5 });
    io.observe(lg);
  };
  // 인트로: 세션당 1회, 동작 축소·해시 진입·data-intro="off"면 생략
  let seen = false; try { seen = sessionStorage.getItem('plk-intro') === '1'; } catch (e) {}
  const introOff = document.body.dataset.intro === 'off' || reduce || seen || location.hash.length > 1 || location.search.includes('nointro');
  if (introOff) { playOnScroll(); return; }
  const intro = document.createElement('div'); intro.className = 'intro'; intro.setAttribute('aria-label', '퍼시픽링스코리아 수도권지사');
  const clone = lg.cloneNode(true); clone.id = 'logoIntro';
  clone.innerHTML = clone.innerHTML.replace(/-lg\\b/g, '-in'); // SVG id 충돌 방지
  const box = document.createElement('div'); box.className = 'intro-box'; box.appendChild(clone); intro.appendChild(box);
  const tag = document.querySelector('.lg-tag'); if (tag) box.appendChild(tag.cloneNode(true));
  const row = document.querySelector('.lg-row'); if (row) box.appendChild(row.cloneNode(true));
  const skip = document.createElement('button'); skip.type = 'button'; skip.className = 'skip'; skip.textContent = '건너뛰기'; intro.appendChild(skip);
  document.body.appendChild(intro); document.body.classList.add('intro-on');
  let left = false;
  const leave = () => { if (left) return; left = true; try { sessionStorage.setItem('plk-intro', '1'); } catch (e) {}
    intro.classList.add('leave'); document.body.classList.remove('intro-on');
    finish(lg); lg.classList.add('done'); // 아래 밴드는 완성 상태로 대기
    setTimeout(() => intro.remove(), 900); track('intro_done'); };
  requestAnimationFrame(() => { play(clone); setTimeout(() => intro.classList.add('ready'), 1200); setTimeout(leave, 3600); });
  skip.addEventListener('click', leave);
  ['wheel', 'touchstart', 'keydown'].forEach(ev => window.addEventListener(ev, leave, { once: true, passive: true }));
}
'''
h = h[:j0] + js + h[j1:]
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
