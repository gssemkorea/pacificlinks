import json, re
P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

svg = open('tools/logo-svg.txt', encoding='utf-8').read()

# ---------- CSS: stats panel → logo band ----------
c0 = h.index('/* stats panel: floats over the hero\'s bottom edge */')
c1 = h.index('\n', h.index('body.full .stats-panel b i{'))
css = '''/* ===== 로고 지표 밴드: 고리는 벡터(원본 측정값), 리본은 사진 패턴 스트로크, 완성 시 원본 PNG로 교체 ===== */
.logo-band{background:radial-gradient(1100px 520px at 50% 0,#17406E,#0B1C33 72%);color:#fff;padding:34px 0 30px;position:relative;z-index:2}
.lg{position:relative;width:min(100%,860px);margin:0 auto;container-type:inline-size}
.lg-svg{display:block;width:100%;height:auto;overflow:visible}
.lg .arc{fill:none;stroke-width:68;stroke-linecap:butt;stroke-dasharray:288;stroke-dashoffset:288}
.lg .ink.lt,.lg .fin.lt{stroke:#68ABE4}.lg .ink.dk,.lg .fin.dk{stroke:#16599E}
.lg .fin{fill:none;stroke-width:68}
.lg .final{display:none}
.lg .word{opacity:0;transform:translateY(12px)}
.lg.play .word{animation:lgRise .6s ease-out 2.3s forwards}
.lg.done .word{opacity:1;transform:none;clip-path:none;animation:none}
.lg.done .segs{display:none}
@keyframes lgRise{to{opacity:1;transform:none}}
@keyframes lgFade{to{opacity:1}}
@keyframes lgDraw{to{stroke-dashoffset:0}}
.lg .dk.s1{--dd:0s}.lg .dk.s2{--dd:.55s}.lg .dk.s3{--dd:1.1s}
.lg .lt.s1{--dd:.28s}.lg .lt.s2{--dd:.83s}.lg .lt.s3{--dd:1.38s}
.lg.play .arc{animation:lgDraw .55s linear var(--dd) forwards}
.lg .ph.sharp{opacity:0}
.lg.play .ph.sharp{animation:lgDraw .55s linear var(--dd) forwards,lgFade 1.1s cubic-bezier(.3,0,.2,1) var(--dd) forwards}
.lg .ink{opacity:.3}
.lg.play .ink{animation:lgDraw .55s linear var(--dd) forwards,lgFade .6s ease-in 2s forwards}
.lg .hole{position:absolute;top:31.55%;width:15.7%;aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;line-height:1;padding:0 4%;opacity:0;color:#fff}
.lg .hole.h1{left:25.2%}.lg .hole.h2{left:50.07%}.lg .hole.h3{left:74.93%}
.lg .hole b{overflow-wrap:normal;white-space:nowrap;font-family:var(--latin);font-weight:800;font-size:3.9cqw;letter-spacing:-.03em;font-variant-numeric:tabular-nums;display:flex;align-items:baseline;gap:.15em;background:none;-webkit-text-fill-color:#fff;color:#fff}
.lg .hole b i{font-style:normal;font-size:1.35cqw;font-weight:700;font-family:var(--body);letter-spacing:0;color:#fff;-webkit-text-fill-color:#fff}
.lg .hole>span{font-size:1.5cqw;font-weight:700;margin-top:.6cqw;white-space:nowrap}
.lg .hole small{font-size:1.15cqw;opacity:.72;margin-top:.45cqw;white-space:nowrap}
.lg.play .hole{animation:lgFade .5s ease-out forwards}
.lg.play .h1{animation-delay:2s}.lg.play .h2{animation-delay:2.15s}.lg.play .h3{animation-delay:2.3s}
.lg.done .hole{opacity:1;animation:none}
.lg-tag{text-align:center;margin:14px 0 0;font-size:14px;color:#B5C4D6}
.lg-tag b{font-family:var(--latin);letter-spacing:.3em;font-size:12px;color:#9CC7EE;margin-right:10px}
.lg-row{display:none;justify-content:center;gap:22px;margin:14px 0 0;padding:0;list-style:none;text-align:center}
.lg-row li b{display:block;font-family:var(--latin);font-size:22px;font-weight:800}
.lg-row li b i{font-style:normal;font-size:12px;font-family:var(--body);margin-left:3px}
.lg-row li span{font-size:12.5px;color:#B5C4D6}
@media (max-width:720px){.lg .hole small{display:none}.lg .hole>span{font-size:1.7cqw}.lg .hole b{font-size:4.6cqw}}
@media (max-width:520px){.lg .hole{display:none}.lg-row{display:flex}.lg-tag{font-size:12.5px}}
@media (prefers-reduced-motion:reduce){.lg .segs{display:none}.lg .word{opacity:1;transform:none;clip-path:none;animation:none}.lg .hole{opacity:1;animation:none}}
/* 검증용: ?logocheck → 원본 PNG를 50%로 겹쳐 보기 */
.lg .lg-check{display:none;position:absolute;inset:0;width:100%;height:auto;opacity:.5;pointer-events:none;mix-blend-mode:difference}
body.logocheck .lg .lg-check{display:block}'''
h = h[:c0] + css + h[c1:]

# ---------- markup ----------
s0 = h.index('  <section class="stats" aria-label="신뢰">')
s1 = h.index('  </section>', s0) + len('  </section>')
holes = '''      <div class="hole h1"><b><span class="n" data-count="276">0</span><i>곳</i></b><span>국내 제휴 골프장</span><small>서울·경기·인천·강원·충청</small></div>
      <div class="hole h2"><b><span class="n" data-count="1000" data-suffix="+">0</span></b><span>해외 제휴 코스</span><small>50여 개국 · 그린피 $60</small></div>
      <div class="hole h3"><b><span class="n" data-count="2">0</span><i>년 연속</i></b><span>스타브랜드 대상</span><small>골프멤버십 부문</small></div>'''
sec = f'''  <section class="band logo-band" id="brand" aria-label="신뢰">
    <div class="wrap">
      <div class="lg" id="logoStats">
{svg}
{holes}
      <img class="lg-check" src="img/logo-color.png" alt="">
      </div>
      <p class="lg-tag"><b>SINCE 2009</b>캐나다 창립 · 글로벌 골프 멤버십 · 수도권지사</p>
      <ul class="lg-row" aria-hidden="true"><li><b>276<i>곳</i></b><span>국내 제휴 골프장</span></li><li><b>1,000+</b><span>해외 제휴 코스</span></li><li><b>2<i>년 연속</i></b><span>스타브랜드 대상</span></li></ul>
    </div>
  </section>'''
h = h[:s0] + sec + h[s1:]

# ---------- JS: countUp → logo play ----------
j0 = h.index('function countUp() {'); j1 = h.index('\n}\n', j0) + 3
js = '''function countUp() {
  const lg = document.getElementById('logoStats'); if (!lg) return;
  if (location.search.includes('logocheck')) document.body.classList.add('logocheck');
  const nums = () => lg.querySelectorAll('.n[data-count]').forEach(el => {
    const to = +el.dataset.count, suf = el.dataset.suffix || '', t0 = performance.now(), dur = 900;
    const step = now => { const k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3); el.textContent = Math.round(to * e).toLocaleString('ko-KR') + suf; if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  });
  const finish = () => lg.querySelectorAll('.n[data-count]').forEach(el => el.textContent = (+el.dataset.count).toLocaleString('ko-KR') + (el.dataset.suffix || ''));
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) { finish(); lg.classList.add('done'); return; }
  const io = new IntersectionObserver(es => es.forEach(en => {
    if (!en.isIntersecting) return; io.disconnect();
    lg.classList.add('play'); setTimeout(nums, 2000); setTimeout(() => lg.classList.add('done'), 2700);
  }), { threshold: .35 });
  io.observe(lg);
}
'''
h = h[:j0] + js + h[j1:]

# nav anchor (신뢰 섹션 id)
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok', len(h))
