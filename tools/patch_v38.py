P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

# ---- 1. 로고 그림자 (사전 렌더 PNG, 완성 시 서서히) ----
rep('  <g class="segs" clip-path="url(#nogap-lg)">', '  <image class="lg-shadow" href="img/logo-shadow.png" x="-60" y="-60" width="846" height="521"/>\n  <g class="segs" clip-path="url(#nogap-lg)">')
rep('.lg .final{display:none}', '.lg .final{display:none}\n.lg .lg-shadow{opacity:0;transition:opacity .9s ease}\n.lg.done .lg-shadow{opacity:1}')

# ---- 2. 히어로: 영상 제거, 고해상 정지 이미지, 제목 2줄·중앙 ----
rep('''      <img id="heroPoster" src="img/hero-cf.jpg" srcset="img/ad-lbh.jpg 1080w, img/hero-cf.jpg 1600w" sizes="(max-width: 860px) 100vw, 1600px" alt="">
      <!-- 2) 자체 호스팅 루프: 이병헌 CF 컷 + 필드 3컷 (media/hero.mp4, 무음) -->
      <video autoplay muted loop playsinline preload="auto" id="heroVideo">
        <source src="media/hero.mp4" type="video/mp4">
      </video>
      <!-- 3) 자체 영상이 없고 유튜브 임베드가 허용된 호스트면 이병헌 CF(5j4Z3RH6RPM)를 무음 배경으로 삽입 (스크립트) -->''',
    '''      <img id="heroPoster" src="img/hero-hd.jpg" srcset="img/hero-mobile-hd.jpg 1080w, img/hero-hd.jpg 1920w" sizes="(max-width: 860px) 100vw, 1920px" alt="">''')
rep('''      <!-- 1) 포스터: 데스크톱은 가로 1920, 모바일은 세로 1080 고해상도 -->''', '''      <!-- 정지 이미지 한 장(Unsplash, 1920 가로 / 1080 세로). 영상·유튜브 배경은 v38에서 제거 -->''')
rep('<h1>주말 라운드, 수도권 276곳에서 그린피 절반으로</h1>', '<h1>주말 라운드, 수도권 276곳에서 <br>그린피 절반으로</h1>')
# hero layout: 중앙 정렬 블록
rep('.hero .wrap{position:relative;padding-block:clamp(80px,12vw,150px) clamp(110px,14vw,160px);display:grid;grid-template-columns:1fr;gap:24px;align-items:center}',
    '.hero .wrap{position:relative;padding-block:clamp(80px,12vw,150px) clamp(110px,14vw,160px);display:grid;grid-template-columns:1fr;gap:24px;align-items:center;justify-items:center;text-align:center}')
rep('.hero-text{display:grid;gap:18px}', '.hero-text{display:grid;gap:18px;justify-items:center;max-width:940px}')
rep('.hero h1{font-size:clamp(34px,5.2vw,58px);max-width:16ch}', '.hero h1{font-size:clamp(30px,4.3vw,54px);max-width:none;line-height:1.18;white-space:nowrap}
@media (max-width:640px){.hero h1{white-space:normal}}\n@media (max-width:640px){.hero h1 br{display:none}}')
rep('.hero .cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:6px}', '.hero .cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:6px;justify-content:center}')
rep('.hero-media::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,14,24,.3) 0%,rgba(6,14,24,.6) 55%,rgba(6,14,24,.9) 100%)}',
    '.hero-media::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,14,24,.45) 0%,rgba(6,14,24,.62) 55%,rgba(6,14,24,.92) 100%)}')
# JS: 히어로 영상/유튜브 로직 제거
j0 = h.index('function setupVideo() {'); j1 = h.index('  // CF 섹션: 자체 호스팅 CF 재생', j0)
h = h[:j0] + 'function setupVideo() {\n' + h[j1:]
# 그림자/배경 참조 정리
rep('.hero-media video,.hero-media img{', '.hero-media img{')
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
