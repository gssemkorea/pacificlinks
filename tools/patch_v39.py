P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

# ---- 히어로 롤링 슬라이드 (Unsplash 핫링크 5장, 로컬 포스터는 로딩/오프라인 대체) ----
rep('''      <img id="heroPoster" src="img/hero-hd.jpg" srcset="img/hero-mobile-hd.jpg 1080w, img/hero-hd.jpg 1920w" sizes="(max-width: 860px) 100vw, 1920px" alt="">''',
    '''      <img id="heroPoster" src="img/hero-hd.jpg" srcset="img/hero-mobile-hd.jpg 1080w, img/hero-hd.jpg 1920w" sizes="(max-width: 860px) 100vw, 1920px" alt="">
      <div class="hero-slides" id="heroSlides" data-interval="6500"></div>''')
rep('.hero-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 45%}',
    '''.hero-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 45%}
.hero-slides{position:absolute;inset:0}
.hero-slides img{opacity:0;transition:opacity 1.6s ease;will-change:opacity,transform}
.hero-slides img.on{opacity:1;animation:heroKb 8s linear forwards}
@keyframes heroKb{from{transform:scale(1)}to{transform:scale(1.07)}}
@media (prefers-reduced-motion:reduce){.hero-slides img.on{animation:none}}''')

# JS: 슬라이드 로더 + 롤링
rep('function setupVideo() {', '''const HERO_SLIDES = [ // Unsplash License (무료·상업 이용 가능). 핫링크는 Unsplash 공식 권장 방식. 오프라인/차단 시 로컬 포스터 유지
  { id: 'photo-1716464968470-c2162dd998e4', pos: 'center 55%', by: 'Tom Schaeffer', what: '코스·야자수' },
  { id: 'photo-1631294949134-ecd4ecd5f4b2', pos: 'center 30%', by: 'Brandon Williams', what: '스윙' },
  { id: 'photo-1766206096924-c78074981e84', pos: 'center 40%', by: 'Syah', what: '대회 갤러리' },
  { id: 'photo-1709525617656-5498eefc7d03', pos: 'center 60%', by: 'Bryce Wendler', what: '그린 햇살' },
  { id: 'photo-1535131749006-b7f58c99034b', pos: 'center 35%', by: 'Courtney Cook', what: '드라이버 스윙' }
];
function setupHeroSlides() {
  const box = document.getElementById('heroSlides'); if (!box) return;
  const mobile = matchMedia('(max-width: 860px)').matches;
  const url = id => `https://images.unsplash.com/${id}?auto=format&fit=crop&q=80&` + (mobile ? 'w=1080&h=1728' : 'w=1920&h=1100');
  const ready = []; let i = -1, timer = null;
  const show = () => { if (!ready.length) return; const prev = ready[i]; i = (i + 1) % ready.length; const cur = ready[i]; if (prev && prev !== cur) prev.classList.remove('on'); cur.classList.add('on'); };
  const start = () => { if (timer) return; show(); timer = setInterval(show, +box.dataset.interval || 6500); };
  HERO_SLIDES.forEach(s => {
    const im = new Image(); im.alt = ''; im.decoding = 'async'; im.style.objectPosition = s.pos; im.title = 'Photo: ' + s.by + ' / Unsplash';
    im.addEventListener('load', () => { box.appendChild(im); ready.push(im); if (ready.length === 1) start(); });
    im.addEventListener('error', () => {}); im.src = url(s.id);
  });
  document.addEventListener('visibilitychange', () => { if (document.hidden) { clearInterval(timer); timer = null; } else start(); });
}
function setupVideo() {
  setupHeroSlides();''')
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
