"""v48: 히어로 = 이병헌 CF (C안: 시네마 → 도킹).
- 영상은 16:9 그대로(자르지 않음), 영상 위에 페이지 글자 없음
- 데스크톱: 처음엔 화면 최대 크기 + 양옆 흐린 앰비언트, 스크롤하면 영상이 오른쪽 카드로 줄며 왼쪽에 문구 등장 (sticky + JS 진행률, 모든 브라우저 동일)
- 모바일(≤860px)·동작 줄이기: 스크롤 연출 없이 영상(16:9 전폭) + 아래 문구
"""
P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

# ---------- CSS ----------
c0 = h.index('/* hero */\n.hero{position:relative;')
c1 = h.index('/* ===== 로고 지표 밴드:')
css = '''/* hero: 이병헌 CF (시네마 → 도킹) */
.hero{position:relative;color:var(--on-dark);background:#08121F;overflow:clip;display:grid;grid-template-rows:0fr;transition:grid-template-rows .9s cubic-bezier(.7,0,.3,1)}
.hero.open{grid-template-rows:1fr}
.hero-in{min-height:0;overflow:clip;position:relative}
@media (prefers-reduced-motion:reduce){.hero{transition:none}}
.hero-scroll{position:relative;height:calc((100svh - var(--hdrH,76px)) * 1.8)}
.hero-sticky{position:sticky;top:var(--hdrH,76px);height:calc(100svh - var(--hdrH,76px));overflow:hidden}
.hero-amb{position:absolute;left:-8%;top:-8%;width:116%;height:116%;filter:blur(46px) brightness(.4) saturate(1.3);opacity:calc(1 - var(--hp,0) * .5);pointer-events:none}
.hero-sticky::after{content:"";position:absolute;inset:0;background:radial-gradient(120% 90% at 50% 45%,transparent 55%,rgba(4,10,20,.55));pointer-events:none}
.cf-box{position:absolute;left:0;top:0;z-index:2;transform-origin:0 0;background:#000;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.55);will-change:transform}
.cf-box video,.cf-box img{display:block;width:100%;height:100%;object-fit:contain;background:#000}
.cf-box img{position:absolute;inset:0;transition:opacity .4s}
.cf-box.playing img{opacity:0}
.cfh-play{position:absolute;inset:0;margin:auto;width:84px;height:84px;border-radius:50%;border:0;background:rgba(0,0,0,.55);color:#fff;display:none;place-items:center;cursor:pointer;backdrop-filter:blur(6px);z-index:2}
.cfh-play svg{width:34px;height:34px;margin-left:5px}
.cf-box.idle .cfh-play{display:grid}
.cf-ctrl{position:absolute;z-index:3;display:flex;gap:8px;left:0;top:0;will-change:transform}
.cf-ctrl button{display:inline-flex;align-items:center;gap:6px;min-height:34px;padding:0 13px;border-radius:999px;border:1px solid rgba(255,255,255,.35);background:rgba(8,18,31,.55);color:#fff;font:700 13px/1 var(--body);cursor:pointer;backdrop-filter:blur(6px);white-space:nowrap}
.cf-ctrl button:hover{background:rgba(255,255,255,.14)}
.cf-ctrl button svg{width:16px;height:16px}
.cf-ctrl .cf-sound[aria-pressed="true"]{background:#fff;color:#0E1C2E;border-color:#fff}
.hero-cue{position:absolute;left:0;right:0;bottom:0;z-index:2;height:64px;display:flex;align-items:center;gap:18px;padding:0 var(--cueX,24px);opacity:calc(1 - var(--hp,0) * 3);pointer-events:none}
.hero-cue b{font-size:clamp(15px,1.25vw,19px);font-weight:800;letter-spacing:-.01em;white-space:nowrap}
.hero-cue span{font-size:11px;letter-spacing:.24em;color:#A9B7C6;font-weight:700;display:flex;align-items:center;gap:6px}
.hero-cue span i{width:9px;height:9px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:rotate(45deg);animation:cueB 1.6s ease-in-out infinite}
@keyframes cueB{0%,100%{transform:translateY(-2px) rotate(45deg);opacity:.5}50%{transform:translateY(2px) rotate(45deg);opacity:1}}
.hero-text{position:absolute;z-index:3;top:50%;left:var(--txX,24px);width:var(--txW,440px);transform:translate(calc((1 - var(--ht,0)) * -24px),-50%);opacity:var(--ht,0);pointer-events:none;display:grid;gap:16px;text-align:left}
.hero.docked .hero-text{pointer-events:auto}
.hero h1{font-size:clamp(28px,2.6vw,44px);line-height:1.2;letter-spacing:-.02em;margin:0}
.hero h1 span{display:block}
.hero .sub{font-size:clamp(15px,1.05vw,17px);color:var(--on-dark-muted);line-height:1.65;margin:0}
.hero .cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:4px}
.hero .owner{font-size:13.5px;color:var(--on-dark-muted);margin:0}
.hero .cf-note{font-size:11.5px;color:#7F90A3;margin:0}
/* 모바일·좁은 화면: 스크롤 연출 없음 */
@media (max-width:860px){
  .hero-scroll{height:auto}
  .hero-sticky{position:static;height:auto;overflow:visible}
  .hero-amb,.hero-sticky::after,.hero-cue{display:none}
  .cf-box{position:relative;width:100%!important;height:auto!important;aspect-ratio:16/9;transform:none!important;box-shadow:none}
  .cf-ctrl{position:static;transform:none!important;padding:10px 16px 0;justify-content:flex-end}
  .hero-text{position:static;width:auto;transform:none;opacity:1;pointer-events:auto;padding:18px 16px 30px}
  .hero h1{font-size:26px}.hero h1 span{display:inline}
}
/* 동작 줄이기: 처음부터 도킹 상태, 스크롤 공간 없음 */
@media (min-width:861px) and (prefers-reduced-motion:reduce){.hero-scroll{height:calc(100svh - var(--hdrH,76px))}}
/* 짧은 화면(노트북 1366×768 등): 로고 밴드 압축 */
@media (min-width:861px) and (max-height:820px){.logo-band{padding:14px 0 10px}.logo-band .lg{width:min(100%,560px)}}
/* 로고 애니메이션 동안 헤더 로고 숨김 */
.brand{transition:opacity .35s}
header.no-brand .brand{opacity:0;pointer-events:none}
.dock{transition:opacity .3s,transform .3s}
body.hero-focus .dock{opacity:0;transform:translateY(12px);pointer-events:none}

'''
h = h[:c0] + css + h[c1:]
# 전체배경(B) 버전의 옛 hero-media 규칙 정리
h = h.replace('body.full .hero-media{display:none}\n', '')

# ---------- 마크업 ----------
m0 = h.index('  <noscript><style>.hero{grid-template-rows:1fr!important}')
m1 = h.index('  </section>', h.index('<section class="hero" id="hero"')) + len('  </section>')
ICON_SND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4z"/><path class="w1" d="M15.5 8.5a5 5 0 0 1 0 7"/><path class="w2" d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>'
ICON_PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>'
hero = f'''  <noscript><style>.hero{{grid-template-rows:1fr!important}}.hero-text{{opacity:1!important}}</style></noscript>
  <section class="hero" id="hero" aria-label="소개">
    <div class="hero-in">
      <div class="hero-scroll" id="heroScroll">
        <div class="hero-sticky" id="heroSticky">
          <canvas class="hero-amb" id="heroAmb" width="64" height="36" aria-hidden="true"></canvas>
          <div class="cf-box idle" id="cfHeroBox">
            <img src="img/cf-hero-poster.jpg" srcset="img/cf-hero-poster-960.jpg 960w, img/cf-hero-poster.jpg 1920w" sizes="(max-width:860px) 100vw, 80vw" alt="">
            <video id="cfHero" muted playsinline loop preload="metadata" aria-label="퍼시픽링스코리아 전속모델 이병헌 TV CF 15초" data-src-hd="media/cf-hero-1080.mp4" data-src-sd="media/cf-hero-720.mp4"></video>
            <button class="cfh-play" type="button" id="cfHeroPlay" aria-label="CF 재생"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></button>
          </div>
          <div class="cf-ctrl" id="cfHeroCtrl">
            <button type="button" class="cf-sound" id="cfHeroSound" aria-pressed="false">{ICON_SND}<span>소리 켜기</span></button>
            <button type="button" class="cf-pause" id="cfHeroPause" aria-pressed="false">{ICON_PAUSE}<span>일시정지</span></button>
          </div>
          <div class="hero-cue" aria-hidden="true"><b>주말 라운드, 수도권 276곳에서 그린피 절반으로</b><span>SCROLL<i></i></span></div>
          <div class="hero-text">
            <div class="eyebrow">Pacific Links Korea · 수도권지사</div>
            <h1><span>주말 라운드,</span> <span>수도권 276곳에서</span> <span>그린피 절반으로</span></h1>
            <p class="sub">멤버십 한 장으로 국내 276곳, 전 세계 1,000여 코스. 개인·법인 멤버십을 담당 지사장이 직접 안내합니다.</p>
            <div class="cta">
              <a class="btn btn-primary" href="#products" data-track="hero_cta_click">내게 맞는 상품 확인</a>
              <a class="btn btn-ghost" href="#contact" data-track="hero_form_click">자료 받기</a>
            </div>
            <p class="owner">담당: 강현식 지사장 · 접수 후 24시간 내 회신</p>
          </div>
        </div>
      </div>
    </div>
  </section>'''
h = h[:m0] + hero + h[m1:]

# ---------- JS: 롤링 슬라이드 제거 → CF 히어로 ----------
s0 = h.index('const HERO_SLIDES = [')
s1 = h.index('function setupVideo() {')
cfjs = '''function setupHeroCF() {
  const hero = document.getElementById('hero'), sc = document.getElementById('heroScroll'), st = document.getElementById('heroSticky');
  const box = document.getElementById('cfHeroBox'), v = document.getElementById('cfHero'), ctrl = document.getElementById('cfHeroCtrl');
  const amb = document.getElementById('heroAmb'), snd = document.getElementById('cfHeroSound'), pau = document.getElementById('cfHeroPause'), playBtn = document.getElementById('cfHeroPlay');
  if (!hero || !v) return;
  const root = document.documentElement.style;
  const mqMob = matchMedia('(max-width: 860px)'), reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  // 해상도별 소스: 화면 폭 × 배율이 1600 이상이면 1080p, 아니면 720p
  const pickSrc = () => (!mqMob.matches && innerWidth * (devicePixelRatio || 1) >= 1600) ? v.dataset.srcHd : v.dataset.srcSd;
  let userPaused = false, started = false, inView = true;
  const setPlaying = on => { box.classList.toggle('playing', on); box.classList.toggle('idle', !on && !started); pau.setAttribute('aria-pressed', String(!on)); pau.querySelector('span').textContent = on ? '일시정지' : '재생'; pau.querySelector('svg').innerHTML = on ? '<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/>' : '<path d="M8 5v14l11-7z"/>'; };
  const play = () => { if (!v.src) v.src = pickSrc(); v.play().then(() => { started = true; setPlaying(true); }).catch(() => setPlaying(false)); };
  v.addEventListener('playing', () => { started = true; setPlaying(true); });
  v.addEventListener('pause', () => setPlaying(false));
  v.muted = true; v.defaultMuted = true; v.setAttribute('muted', '');
  setPlaying(false);
  // 자동재생: 히어로가 펼쳐질 때 0초부터 (데이터 절약·동작 줄이기는 재생 버튼만)
  const auto = !saveData && !reduce;
  const kick = () => { if (auto && !userPaused) { v.currentTime = 0; play(); } };
  if (hero.classList.contains('open')) kick(); else hero.addEventListener('hero:open', kick, { once: true });
  playBtn.addEventListener('click', () => { userPaused = false; play(); track('hero_cf_play'); });
  pau.addEventListener('click', () => { if (v.paused) { userPaused = false; play(); } else { userPaused = true; v.pause(); } track('hero_cf_pause'); });
  snd.addEventListener('click', () => {
    const on = v.muted; v.muted = !on;
    if (on) { v.currentTime = 0; userPaused = false; play(); }
    snd.setAttribute('aria-pressed', String(on)); snd.querySelector('span').textContent = on ? '소리 끄기' : '소리 켜기';
    track(on ? 'hero_cf_sound_on' : 'hero_cf_sound_off');
  });
  // 화면 밖이면 일시정지, 돌아오면 이어서 (사용자가 직접 멈춘 경우 제외)
  if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(en => {
    inView = en.isIntersecting;
    if (!started && !auto) return;
    if (!inView && !v.paused) v.pause(); else if (inView && v.paused && started && !userPaused) play();
  }), { threshold: .15 }).observe(box);
  document.addEventListener('visibilitychange', () => { if (document.hidden && !v.paused) v.pause(); else if (!document.hidden && inView && started && !userPaused) play(); });
  // 앰비언트: 영상(재생 전엔 포스터)을 64×36 캔버스에 그려 CSS로 흐리게
  const ctx = amb.getContext('2d'); const poster = box.querySelector('img');
  const paint = src => { try { ctx.drawImage(src, 0, 0, 64, 36); } catch (e) {} };
  if (poster.complete) paint(poster); else poster.addEventListener('load', () => paint(poster), { once: true });
  setInterval(() => { if (!v.paused && inView && !mqMob.matches) paint(v); }, 220);

  // 시네마 → 도킹: 히어로 안의 스크롤 진행률로 영상 위치·크기를 보간
  const ease = t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
  let G = null;
  const measure = () => {
    if (mqMob.matches) { G = null; ['--hp', '--ht'].forEach(k => root.removeProperty(k)); box.style.cssText = ''; ctrl.style.cssText = ''; return; }
    const W = st.clientWidth, H = st.clientHeight, cue = 64;
    // 시네마: 큐 띠(64px)를 뺀 높이 안에서 16:9 최대
    let ch = Math.min(H - cue - 20, (W - 48) * 9 / 16), cw = ch * 16 / 9;
    const cx = (W - cw) / 2, cy = Math.max(12, (H - cue - ch) / 2);
    // 도킹: 콘텐츠 폭(최대 1320) 중 왼쪽 38% 문구, 오른쪽 영상 카드
    const gut = Math.max(24, Math.min(64, W * .04)), wrapW = Math.min(W - gut * 2, 1320), x0 = (W - wrapW) / 2;
    const txW = Math.max(340, Math.min(500, wrapW * .36)), gap = Math.max(32, wrapW * .035);
    let dw = wrapW - txW - gap, dh = dw * 9 / 16;
    if (dh > H - 120) { dh = H - 120; dw = dh * 16 / 9; }
    const dx = x0 + wrapW - dw, dy = (H - dh) / 2 - 14;
    G = { cw, ch, cx, cy, dx, dy, s: dw / cw };
    box.style.width = cw + 'px'; box.style.height = ch + 'px';
    root.setProperty('--txX', x0 + 'px'); root.setProperty('--txW', txW + 'px'); root.setProperty('--cueX', cx + 'px');
    frame();
  };
  const frame = () => {
    if (!G) return;
    let p = 1;
    if (!reduce) { const r = sc.getBoundingClientRect(), room = sc.offsetHeight - st.clientHeight; p = room > 0 ? Math.min(1, Math.max(0, -r.top / room)) : 1; }
    const e = ease(Math.min(1, Math.max(0, (p - .12) / .72)));   // 처음 12%는 시네마 유지
    const x = G.cx + (G.dx - G.cx) * e, y = G.cy + (G.dy - G.cy) * e, s = 1 + (G.s - 1) * e;
    box.style.transform = `translate(${x}px,${y}px) scale(${s})`;
    box.style.borderRadius = (16 * e / s) + 'px';
    const bw = G.cw * s, bh = G.ch * s;
    ctrl.style.transform = `translate(${x + (bw - ctrl.offsetWidth) * (1 - e)}px,${y + bh + 12}px)`;   // 시네마: 오른쪽 정렬 → 도킹: 왼쪽 정렬(플로팅 버튼과 겹침 방지)
    root.setProperty('--hp', e.toFixed(3));
    root.setProperty('--ht', Math.min(1, Math.max(0, (e - .45) / .45)).toFixed(3));
    hero.classList.toggle('docked', e > .6);
    const hr = sc.getBoundingClientRect(); document.body.classList.toggle('hero-focus', hr.bottom > innerHeight * .55 && hr.top < innerHeight * .4);
  };
  let raf = 0; const onScroll = () => { if (raf) return; raf = requestAnimationFrame(() => { raf = 0; frame(); }); };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', measure);
  (mqMob.addEventListener ? mqMob.addEventListener('change', measure) : mqMob.addListener(measure));
  hero.addEventListener('hero:open', measure);
  measure(); setTimeout(measure, 950);
}
'''
h = h[:s0] + cfjs + h[s1:]
rep('function setupVideo() {\n  setupHeroSlides();', 'function setupVideo() {\n  setupHeroCF();')
# 펼침 직후 레이아웃 재계산 (높이 0 → 펼침)
rep("  const open = () => { size(); if (hero.classList.contains('open')) return; hero.classList.add('open'); if (hdr) hdr.classList.remove('no-brand'); setTimeout(() => hero.dispatchEvent(new Event('hero:open')), 300); };",
    "  const open = () => { size(); if (hero.classList.contains('open')) return; hero.classList.add('open'); if (hdr) hdr.classList.remove('no-brand'); setTimeout(() => hero.dispatchEvent(new Event('hero:open')), 120); };")
assert 'heroSlides' not in h and 'setupHeroSlides' not in h
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok', len(h))
