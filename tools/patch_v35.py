import json, re
P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:80]; h = h.replace(a, b, 1)

# ---------- data ----------
d = json.load(open('data/site.json', encoding='utf-8'))
d['benefits'] = [
 {"id": "booking", "kind": "card", "title": "예약은 사람이 합니다", "img": "img/manager-half.png", "imgPos": "center 20%",
  "body": "본사 예약실·고객서비스팀이 상시 운영되고, 수도권은 전담팀이 따로 있습니다. 수도권지사 회원은 강현식 지사장에게 직접 연락해 예약·페이백·행사를 한 번에 처리합니다. 회원 앱으로 횟수 확인과 페이백 신청(라운드 3일 전).",
  "link": {"label": "담당자 보기", "href": "#manager"},
  "voice": {"say": "예약은 사람이 합니다. 본사 예약실과 수도권 전담팀이 있고, 수도권지사 회원은 강현식 지사장에게 바로 연락하면 예약과 페이백, 행사까지 한 번에 처리됩니다. 횟수 확인과 페이백 신청은 회원 앱으로 하시면 됩니다."}},
 {"id": "travel", "kind": "card", "title": "항공·호텔·라운드를 한 번에", "img": "img/bn-resort.jpg",
  "body": "본사 여행사 투어링스가 동남아·일본·미국·유럽 골프 여행과 1:1 맞춤 여행을 설계합니다. 마스터스 등 4대 메이저 직관 투어는 매년. 수도권지사는 11월 태국 로터스밸리 행사를 직접 만듭니다.",
  "link": {"label": "여행 보기", "href": "https://www.tourlinks.co.kr/overseas/index/4250", "ext": True}, "link2": {"label": "행사 보기", "href": "#events"},
  "voice": {"say": "항공과 호텔, 라운드를 한 번에. 본사 여행사 투어링스가 동남아, 일본, 미국, 유럽 골프 여행과 맞춤 여행을 설계하고, 마스터스 같은 메이저 대회 직관 투어도 매년 있습니다. 수도권지사는 십일월 태국 로터스밸리 행사를 직접 만듭니다."}},
 {"id": "lounge", "kind": "card", "title": "레슨·피팅·스크린, 트랙맨으로", "img": "img/bn-sim.jpg",
  "body": "강남 논현동과 광주 흑석동의 프리미엄 골프 스튜디오 PLK 라운지. 프라이빗 레슨, 트랙맨 스윙 분석, 피팅센터, 프로샵·카페. 수도권 회원은 강남점이 가깝습니다.",
  "link": {"label": "라운지 안내", "href": "https://www.plklounge.com", "ext": True},
  "voice": {"say": "레슨과 피팅, 스크린을 트랙맨으로. 강남 논현동과 광주 흑석동에 프리미엄 골프 스튜디오 피엘케이 라운지가 있습니다. 프라이빗 레슨, 트랙맨 스윙 분석, 피팅센터, 프로샵과 카페까지. 수도권 회원은 강남점이 가깝습니다."}},
 {"id": "overseas", "kind": "tile", "title": "해외 1,000여 코스", "body": "50여 개국 · 그린피 $60 수준 · 연 횟수 안에서 이용", "link": {"label": "FAQ", "faq": "B5"}},
 {"id": "mall", "kind": "tile", "title": "PLK 몰", "body": "굿즈·골프 기어·의류, 멤버 혜택 (본사 운영)", "link": {"label": "몰 열기", "href": "https://plkmall.co.kr/shop/list.php?ca_id=001", "ext": True}},
 {"id": "events", "kind": "tile", "title": "회원 행사", "body": "월 정기 라운드 · 지사배 대회 · 부부모임 — 수도권지사 직접 운영", "link": {"label": "행사 보기", "href": "#events"}},
 {"id": "life", "kind": "tile", "title": "평생 · 양도", "body": "라이프는 평생 이용, 입회 5년 후 2회 양도 — 자산으로 남는 멤버십", "link": {"label": "FAQ", "faq": "C3"}}
]
for b in d['benefits']:
    if b.get('voice'): b['voice'] = {'m': {'script': b['body'], 'say': b['voice']['say']}, 'f': {'script': b['body'], 'say': b['voice']['say']}}
json.dump(d, open('data/site.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
s = h.index('window.__SITE_FALLBACK__ = '); e = h.index('\n', s)
h = h[:s] + 'window.__SITE_FALLBACK__ = ' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ';' + h[e:]

# ---------- markup ----------
rep('''        <h2>멤버십 한 장에 담긴 여섯 가지</h2>
        <p class="lead muted">그린피만이 아닙니다. 여행·라운지·레슨까지 한 장으로 이어집니다.</p>''',
    '''        <h2>라운드 밖에서 더 얻는 것</h2>
        <p class="lead muted">그린피는 시작입니다. 예약부터 여행·레슨·대회까지, 한 장으로 이어집니다.</p>''')
rep('<section class="band" aria-label="혜택">', '<section class="band" id="benefits" aria-label="혜택">')
i0 = h.index('      <div class="benefits">'); i1 = h.index('</div>\n    </div>\n  </section>', i0)
h = h[:i0] + '      <div class="bn-cards" id="bnCards"></div>\n      <div class="bn-tiles" id="bnTiles"></div>\n    ' + h[i1 + len('</div>\n'):]

# ---------- CSS ----------
rep('.photo-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:28px}', '.photo-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:0}')
rep('.photo-row img{width:100%;aspect-ratio:4/3;', '.photo-row img{width:100%;aspect-ratio:16/9;height:120px;')
rep('.benefits{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:18px}', '''.bn-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:22px}
.bn-card{display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--line);border-radius:16px;overflow:hidden;cursor:pointer;transition:box-shadow .2s,transform .2s}
.bn-card:hover{box-shadow:0 18px 40px rgba(16,42,74,.14);transform:translateY(-2px)}
.bn-card img{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:center 35%;display:block}
.bn-card .bn-body{padding:16px 18px 0;display:grid;gap:8px}
.bn-card b{font-size:18px;line-height:1.3}
.bn-card p{margin:0;font-size:14.5px;line-height:1.7;color:var(--muted)}
.bn-card .bn-act{display:flex;align-items:center;gap:10px;padding:14px 18px 18px;margin-top:auto}
.bn-card .bn-act .btn{flex:1;min-height:42px;font-size:14px;padding:0 12px}
.bn-card .voice{--c-acc:var(--blue);--c-fg:var(--fg);--c-line:var(--line)}
.bn-card .vbtn{width:42px;height:42px;box-shadow:none}
.bn-card .vbtn .ico svg{width:19px;height:19px}
.ext::after{content:" ↗";font-size:.85em}
.bn-tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:14px}
.bn-tile{display:grid;grid-template-columns:1fr auto;align-items:center;gap:10px;padding:14px 16px;border:1px solid var(--line);border-radius:12px;background:var(--panel);text-decoration:none;color:inherit;cursor:pointer}
.bn-tile:hover{border-color:var(--blue)}
.bn-tile b{display:block;font-size:15px;margin-bottom:2px}
.bn-tile span{display:block;font-size:13px;color:var(--muted);line-height:1.5}
.bn-tile i{font-style:normal;font-size:12.5px;font-weight:700;color:var(--blue);white-space:nowrap}
@media (max-width:900px){.bn-tiles{grid-template-columns:1fr 1fr}}
@media (max-width:760px){.bn-cards{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:6px;margin-inline:-16px;padding-inline:16px;-webkit-overflow-scrolling:touch}.bn-card{flex:0 0 84%;scroll-snap-align:start}.photo-row img{height:84px}}
@media (max-width:480px){.bn-tiles{grid-template-columns:1fr}}
body.full .bn-card,body.full .bn-tile{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)}
body.full .bn-card p,body.full .bn-tile span{color:var(--on-dark-muted)}
body.full .bn-card .voice{--c-fg:var(--on-dark);--c-line:rgba(255,255,255,.2)}
.benefits{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:18px}''')

# ---------- JS ----------
rep("function renderCourses() {", '''function renderBenefits() {
  const cards = document.getElementById('bnCards'), tiles = document.getElementById('bnTiles'); if (!cards || !DATA.benefits) return;
  const linkA = (l, cls) => !l ? '' : l.faq ? `<a class="${cls}" href="#faq-${esc(l.faq)}" data-faq-go="${esc(l.faq)}">${esc(l.label)}</a>` : `<a class="${cls}${l.ext ? ' ext' : ''}" href="${esc(l.href)}"${l.ext ? ' target="_blank" rel="noopener"' : ''} data-track="benefit_click" data-benefit="${esc(l.label)}">${esc(l.label)}</a>`;
  cards.innerHTML = DATA.benefits.filter(b => b.kind === 'card').map(b => `
    <article class="bn-card" id="bn-${esc(b.id)}">
      <img src="${esc(b.img)}" alt=""${b.imgPos ? ` style="object-position:${esc(b.imgPos)}"` : ''}>
      <div class="bn-body"><b>${esc(b.title)}</b><p>${esc(b.body)}</p></div>
      <div class="bn-act">${linkA(b.link, 'btn btn-primary')}${b.link2 ? linkA(b.link2, 'btn btn-ghost') : ''}${b.voice ? `<div class="voice" data-benefit-id="${esc(b.id)}"><button type="button" class="vbtn tts-only" data-state="idle" data-tip="설명 듣기" aria-label="${esc(b.title)} 설명 듣기" aria-pressed="false"><svg class="ring" viewBox="0 0 56 56" aria-hidden="true"><circle class="bg" cx="28" cy="28" r="26"/><circle class="fg" cx="28" cy="28" r="26"/></svg><span class="ico" aria-hidden="true">${ICON_HEAD}</span></button></div>` : ''}</div>
    </article>`).join('');
  tiles.innerHTML = DATA.benefits.filter(b => b.kind === 'tile').map(b => {
    const l = b.link || {}; const href = l.faq ? `#faq-${esc(l.faq)}` : esc(l.href || '#');
    return `<a class="bn-tile${l.ext ? '' : ''}" href="${href}"${l.ext ? ' target="_blank" rel="noopener"' : ''}${l.faq ? ` data-faq-go="${esc(l.faq)}"` : ''} data-track="benefit_click" data-benefit="${esc(b.id)}"><div><b>${esc(b.title)}</b><span>${esc(b.body)}</span></div><i class="${l.ext ? 'ext' : ''}">${esc(l.label || '')}</i></a>`;
  }).join('');
}
function renderCourses() {''')
rep("  renderTabs(); renderProducts(); renderCourses(); renderEvents(); renderFaq();", "  renderTabs(); renderProducts(); renderCourses(); renderEvents(); renderFaq(); renderBenefits();")
# voiceOf: benefit cards
rep("  if (box.dataset.faq) {", "  if (box.dataset.benefitId) { const b = (DATA.benefits || []).find(x => x.id === box.dataset.benefitId); const v = b && b.voice && (b.voice[VOICE_GENDER] || b.voice.f || b.voice.m); return v ? Object.assign({ id: 'benefit-' + b.id }, v) : null; }\n  if (box.dataset.faq) {")
# data-faq-go clicks outside the FAQ section (tiles) → openFaq
rep("  document.addEventListener('click', e => {\n    const fp = e.target.closest('[data-faq-product]');",
    "  document.addEventListener('click', e => {\n    const fg = e.target.closest('#benefits [data-faq-go]'); if (fg) { e.preventDefault(); openFaq(fg.dataset.faqGo); return; }\n    const fp = e.target.closest('[data-faq-product]');")
# card click (not on a/button) → first link
rep("    const evb = e.target.closest('[data-ev-open]');", "    const bc = e.target.closest('.bn-card'); if (bc && !e.target.closest('a, button')) { const a = bc.querySelector('.bn-act a'); if (a) a.click(); return; }\n    const evb = e.target.closest('[data-ev-open]');")
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
