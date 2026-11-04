"""v52: 60초 브랜드 필름(풀버전) 뷰어 + 제한적 스냅(히어로 끝·로고 밴드·멤버십) + 히어로 화질 원본 유지"""
P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

FILM_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m10 9 5 3-5 3z" fill="currentColor"/></svg>'
# 1) 히어로 컨트롤에 '풀버전 보기(60초)'
rep('          </div>\n          <div class="hero-cue" aria-hidden="true">',
    f'            <button type="button" class="cf-film" id="cfFilmOpen" aria-haspopup="dialog">{FILM_ICON}<span>풀버전 보기 · 60초</span></button>\n          </div>\n          <div class="hero-cue" aria-hidden="true">')
# 2) 풀버전 대화상자 (</main> 뒤)
rep('</main>', '''</main>

<dialog class="film-dlg" id="filmDlg" aria-label="이병헌 브랜드 필름 60초">
  <div class="film-in">
    <video id="filmVideo" controls playsinline preload="none" poster="img/cf-film-poster.jpg" data-src-hd="media/cf-film-1080.mp4" data-src-sd="media/cf-film-720.mp4"></video>
    <div class="film-bar"><b>퍼시픽링스코리아 × 이병헌 · Brand Film</b><span>더 넓은 세계로 라운드 하라 · 60초</span><button type="button" class="film-x" id="filmClose" aria-label="닫기">닫기 ✕</button></div>
  </div>
</dialog>''')
# 3) 히어로 스냅 마커 (도킹 완료 위치)
rep('      <div class="hero-scroll" id="heroScroll">\n', '      <div class="hero-scroll" id="heroScroll">\n        <i class="snap-mark" aria-hidden="true"></i>\n')
# 4) CSS
rep('/* 짧은 화면(노트북 1366×768 등): 로고 밴드 압축 */', '''.cf-ctrl .cf-film{background:rgba(22,89,158,.85);border-color:rgba(255,255,255,.45)}
.cf-ctrl .cf-film:hover{background:#1B66B5}
/* 풀버전 뷰어 */
.film-dlg{padding:0;border:0;background:transparent;width:min(92vw,calc((100svh - 140px) * 16 / 9),1600px);max-width:none;max-height:none;overflow:visible}
.film-dlg::backdrop{background:rgba(3,8,16,.88);backdrop-filter:blur(6px)}
.film-in{display:grid;gap:12px}
.film-in video{width:100%;aspect-ratio:16/9;background:#000;border-radius:12px;display:block}
.film-bar{display:flex;align-items:center;gap:14px;color:#fff;font-size:14px}
.film-bar span{color:#A9B7C6;font-size:13px}
.film-x{margin-left:auto;min-height:38px;padding:0 16px;border-radius:999px;border:1px solid rgba(255,255,255,.4);background:transparent;color:#fff;font:700 14px/1 var(--body);cursor:pointer}
.film-x:hover{background:rgba(255,255,255,.12)}
@media (max-width:860px){.cf-ctrl{flex-wrap:wrap;gap:6px}.cf-ctrl button{min-height:32px;padding:0 10px;font-size:12px}.film-dlg{width:100vw}.film-in video{border-radius:0}.film-bar{padding:0 14px;flex-wrap:wrap}.film-bar span{display:none}}
/* 섹션 경계 스냅: 근처에 왔을 때만 살짝(proximity), 3지점만 — 히어로 도킹 완료 · 로고 밴드 · 멤버십 시작. 모바일·동작 줄이기 제외 */
.snap-mark{position:absolute;left:0;width:1px;height:1px;top:calc(100% - (100svh - var(--hdrH,76px)));pointer-events:none}
@media (min-width:861px) and (prefers-reduced-motion:no-preference){
  html{scroll-snap-type:y proximity;scroll-padding-top:var(--hdrH,76px)}
  .snap-mark,#brand,#products{scroll-snap-align:start}
}
/* 짧은 화면(노트북 1366×768 등): 로고 밴드 압축 */''')
# 5) JS: 뷰어
rep('function setupVideo() {\n  setupHeroCF();', '''function setupFilm() {
  const dlg = document.getElementById('filmDlg'), fv = document.getElementById('filmVideo'), open = document.getElementById('cfFilmOpen'), hv = document.getElementById('cfHero');
  if (!dlg || !fv || !open) return;
  let heroWasPlaying = false;
  const close = () => { fv.pause(); if (dlg.open) dlg.close(); };
  open.addEventListener('click', () => {
    heroWasPlaying = hv && !hv.paused; if (hv) hv.pause();
    if (!fv.src) fv.src = (innerWidth * (devicePixelRatio || 1) >= 1400 && !(navigator.connection && navigator.connection.saveData)) ? fv.dataset.srcHd : fv.dataset.srcSd;
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
    fv.muted = false; fv.currentTime = 0; fv.play().catch(() => {});
    track('film_open');
  });
  document.getElementById('filmClose').addEventListener('click', close);
  dlg.addEventListener('click', e => { if (e.target === dlg) close(); });   // 바깥(배경) 클릭 닫기
  dlg.addEventListener('close', () => { fv.pause(); if (heroWasPlaying && hv) hv.play().catch(() => {}); track('film_close', { t: Math.round(fv.currentTime) }); });
  fv.addEventListener('ended', () => track('film_complete'));
}
function setupVideo() {
  setupHeroCF(); setupFilm();''')
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
