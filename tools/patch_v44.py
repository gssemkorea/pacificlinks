P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

# ---- 1. 풋터 로고 확대 ----
rep('footer>.wrap>img{height:44px;width:auto;margin-bottom:16px;opacity:.9}', 'footer>.wrap>img{height:52px;width:auto;margin-bottom:18px;opacity:.95}')

# ---- 2. 공통 미세 리빌 ----
rep('/* footer */', '''/* 공통 리빌: 화면에 15% 들어올 때 1회, transform·opacity만 (레이아웃 영향 없음) */
[data-reveal]{opacity:0;transform:translateY(12px);transition:opacity .45s ease,transform .45s ease;transition-delay:var(--rd,0ms)}
[data-reveal="img"]{transform:scale(1.03);transition-duration:.8s}
[data-reveal].in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){[data-reveal]{opacity:1;transform:none;transition:none}}
/* footer */''')

rep('function countUp() {', '''// 리빌 대상 지정 + 관찰. 렌더 후마다 scan() 재호출 가능
const REVEAL = { io: null, mobile: matchMedia('(max-width:860px)').matches };
function revealScan() {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const mark = (sel, step, limit = 8) => document.querySelectorAll(sel).forEach(parent => {
    [...parent.children].forEach((el, i) => { if (el.hasAttribute('data-reveal')) return; el.setAttribute('data-reveal', ''); el.style.setProperty('--rd', Math.min(i, limit) * (REVEAL.mobile ? step / 2 : step) + 'ms'); });
  });
  mark('.band .sec-title', 80);                     // 섹션 타이틀: eyebrow → h2 → 설명
  mark('#productGrid', 60); mark('#bnCards', 60); mark('#bnTiles', 50); mark('#courseGrid', 60); mark('.evt', 60);
  mark('.cond', 50); mark('.corp-cols', 70); mark('#faqList', 40, 6); mark('.faq-tabs', 30, 8);
  document.querySelectorAll('.mgr-wrap img.mgr-photo, .corp-ad img, .promo-poster img, .sec-person img, .closing img, .reviews > *').forEach(el => { if (!el.hasAttribute('data-reveal')) el.setAttribute('data-reveal', 'img'); });
  // 자료 받기 폼·담당자 본문
  document.querySelectorAll('#manager .lead, #manager .phone, #manager .namecard, #leadForm').forEach(el => { if (!el.hasAttribute('data-reveal')) el.setAttribute('data-reveal', ''); });
  if (!('IntersectionObserver' in window)) { document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('in')); return; }
  if (!REVEAL.io) REVEAL.io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); REVEAL.io.unobserve(en.target); } }), { threshold: .15, rootMargin: '0px 0px -5% 0px' });
  document.querySelectorAll('[data-reveal]:not(.in)').forEach(el => REVEAL.io.observe(el));
  // 앵커 점프 등으로 화면을 지나쳐 버린 요소는 즉시 표시
  if (!REVEAL.scroll) { REVEAL.scroll = true; let t = 0; addEventListener('scroll', () => { if (t) return; t = setTimeout(() => { t = 0; document.querySelectorAll('[data-reveal]:not(.in)').forEach(el => { if (el.getBoundingClientRect().bottom < 0) el.classList.add('in'); }); }, 120); }, { passive: true }); }
}
function countUp() {''')
# 초기 렌더 후 + 재렌더(탭·필터·FAQ 검색) 후
rep("  renderTabs(); renderProducts(); renderCourses(); renderEvents(); renderFaq(); renderBenefits(); renderSectionVoices();\n",
    "  renderTabs(); renderProducts(); renderCourses(); renderEvents(); renderFaq(); renderBenefits(); renderSectionVoices(); revealScan();\n  new MutationObserver(() => revealScan()).observe(document.getElementById('productGrid'), { childList: true });\n  new MutationObserver(() => revealScan()).observe(document.getElementById('faqList'), { childList: true });\n")
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
