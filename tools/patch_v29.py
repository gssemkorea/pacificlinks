import json
P = 'pacificlinks-branch-mvp.html'
d = json.load(open('data/site.json', encoding='utf-8'))
by = {p['id']: p for p in d['products']}

# ---------- facets ----------
FAC = {
 'personal-life-20':  dict(freq=['low'], fee=['half'], term=['life'], money=['life'], deleg=False, budget=['u50']),
 'personal-life-30':  dict(freq=['mid'], fee=['half'], term=['life'], money=['life'], deleg=False, budget=['u50']),
 'personal-life-50':  dict(freq=['high'], fee=['half'], term=['life'], money=['life'], deleg=True, budget=['u50']),
 'personal-1plus1-50':dict(freq=['high'], fee=['half'], term=['life'], money=['life'], deleg=False, budget=['u100']),
 'corp-life-30':      dict(freq=['mid'], fee=['half'], term=['life'], money=['life'], deleg=True, budget=['u200']),
 'corp-life-50':      dict(freq=['high'], fee=['half'], term=['life'], money=['life'], deleg=True, budget=['u200']),
 'corp-delegate':     dict(freq=['low'], fee=['half'], term=[], money=[], deleg=True, budget=[]),
 'premium-expire':    dict(freq=['mid','high'], fee=['free'], term=['short'], money=['expire'], deleg=True, budget=['u100']),
 'premium-refund-5y': dict(freq=['mid'], fee=['free','half'], term=['5y'], money=['refund'], deleg=True, budget=['u200']),
 'premium-weekend':   dict(freq=['mid'], fee=['free'], term=['short'], money=['expire'], deleg=True, budget=['u100']),
 'premium-expire-long':dict(freq=['mid','high'], fee=['free'], term=['short','5y'], money=['expire'], deleg=True, budget=['u100','u200']),
 'premium-refund-5y-50':dict(freq=['high'], fee=['half','free'], term=['5y'], money=['refund'], deleg=None, budget=['o200']),
 'premium-gold':      dict(freq=['high'], fee=['fixed'], term=['8y'], money=['expire'], deleg=True, budget=['u200']),
 'resort-lotus':      dict(freq=['high'], fee=['free'], term=['5y'], money=['expire'], deleg=True, budget=['u50']),
}
for k, v in FAC.items(): by[k]['f'] = v
d['groups'] = [{'id': 'personal', 'name': '개인·부부', 'desc': '혼자 또는 부부가 쓰는 기명 멤버십 — 평생 이용, 그린피 50%'},
               {'id': 'corp', 'name': '법인·접대', 'desc': '임원 접대와 임직원 복지용 — 기명 1 + 무기명 3, 손님 위임 가능'},
               {'id': 'premium', 'name': '프리미엄', 'desc': '그린피 100% 면제(소멸형)와 입회금 반환형 — 2년·3년·5년'},
               {'id': 'resort', 'name': '해외 체류', 'desc': '해외 골프장 체류형 — 그린피·숙박·조식 포함'}]
d['filters'] = [
 {'id': 'freq', 'name': '라운드 빈도', 'opts': [['low', '월 1~2회'], ['mid', '월 3회'], ['high', '주 1회 이상']]},
 {'id': 'fee', 'name': '그린피', 'opts': [['half', '50% 할인'], ['free', '100% 면제'], ['fixed', '고정 요금']]},
 {'id': 'money', 'name': '입회금', 'opts': [['life', '평생형 (양도 가능)'], ['refund', '만기 반환'], ['expire', '소멸형']]},
 {'id': 'term', 'name': '이용 기간', 'opts': [['life', '평생'], ['short', '2~3년'], ['5y', '5년']]},
 {'id': 'deleg', 'name': '손님만 보내기 (위임)', 'opts': [['yes', '위임 가능']]},
 {'id': 'budget', 'name': '입회금 예산', 'opts': [['u50', '5천만원 이하'], ['u100', '1억 이하'], ['u200', '2억 이하'], ['o200', '2억 초과']]},
]
# ---------- event details ----------
DET = {
 'PLK 정기 라운드': dict(when='매월 둘째 목요일 · 오전 티오프', where='베르힐CC (수도권)', who='수도권지사 회원 · 동반 1인까지', includes='라운드(회원 그린피 적용) · 조별 편성 · 라운드 후 식사', fee='그린피·카트·캐디피 각자 부담 · 식사는 지사 제공', how='전월 25일까지 카톡 또는 전화로 신청 · 선착순 마감', note='처음 오시는 분은 지사장이 같은 조로 편성해 드립니다.'),
 'PLK 부부모임 골프': dict(when='10월 셋째 일요일', where='사우스스프링스CC (경기 이천)', who='부부 동반 회원 · 6팀', includes='라운드 · 부부 팀 대항 시상 · 점심', fee='그린피·카트·캐디피 각자 부담', how='카톡으로 부부 성함과 연락처 접수', note='1+1 라이프 50 회원이 가장 많이 참여하는 모임입니다.'),
 'PLK 수도권지사배 골프대회': dict(when='10월 넷째 수요일 · 07:30 집결', where='클럽72 (인천 영종)', who='수도권지사 회원 · 12팀', includes='신페리오 시상 · 롱기스트·니어리스트 · 시상식 만찬', fee='참가비 상담 시 안내 (그린피 회원가 별도)', how='지사장 전화 또는 카톡 · 팀 단위 접수 가능', note='법인 회원은 손님 동반(위임) 참가가 가능합니다.'),
 'PLK 셀럽 골프대회': dict(when='10월 마지막 수요일', where='청라 베어즈베스트CC (인천 서구)', who='초청 회원 · 6팀', includes='초청 라운드 · 기념 촬영 · 만찬', fee='초청 행사 (그린피 회원가 별도)', how='지사장 초청 안내를 받으신 분만 접수', note='가입 상담 중인 분도 지사장 동반으로 참관 가능합니다.'),
 '해외 골프여행 (태국 로터스밸리)': dict(when='11월 · 3박 5일 (출발일 모집 중)', where='태국 로터스밸리CC · Grand Sappaya Hotel', who='회원 및 가족 · 소수 정원', includes='항공 · 호텔 · 라운드 · 조식 (카트·캐디피 별도)', fee='여행 경비 상담 시 안내', how='카톡 또는 전화로 인원·출발 희망일 접수', note='로터스밸리CC 5년 멤버십(그린피·숙박·조식 0원)을 현장에서 함께 안내합니다.'),
}
for e in d['events']:
    if e['name'] in DET: e['detail'] = DET[e['name']]
json.dump(d, open('data/site.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:80]; h = h.replace(a, b, 1)
s = h.index('window.__SITE_FALLBACK__ = '); e = h.index('\n', s)
h = h[:s] + 'window.__SITE_FALLBACK__ = ' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ';' + h[e:]

# ---------- CSS: events layout fix + filter + event popup ----------
rep('.evt div{display:grid;grid-template-columns:108px 1fr auto;gap:18px;align-items:center;padding:16px 0;border-top:1px solid var(--line)}',
    '.evt>.ev{display:grid;grid-template-columns:108px minmax(0,1fr) auto;gap:18px;align-items:center;padding:16px 0;border-top:1px solid var(--line);cursor:pointer}\n.evt>.ev:hover b{color:var(--blue)}\n.ev-body{min-width:0;display:grid;gap:4px}\n.ev-act{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}\n.ev-act .btn{min-height:40px;padding:0 14px;font-size:13px}')
rep('.evt b{display:block}.evt span{font-size:13px;color:var(--muted)}', '.evt b{display:block;font-size:16px;word-break:keep-all}.evt span{font-size:13px;color:var(--muted)}')
rep('@media (max-width:520px){.evt div{grid-template-columns:96px 1fr;gap:12px}.evt img{width:96px;height:96px}.evt div .btn{grid-column:2}}',
    '@media (max-width:640px){.evt>.ev{grid-template-columns:88px minmax(0,1fr);gap:12px 14px}.evt img{width:88px;height:88px}.ev-act{grid-column:1/-1;justify-content:flex-start}}')
rep('body.full .strip div,body.full .evt div{border-color:rgba(255,255,255,.14)}', 'body.full .strip div,body.full .evt>.ev{border-color:rgba(255,255,255,.14)}')
rep('.tabs{display:flex;gap:6px;flex-wrap:wrap}',
    '''.tabs{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.filter-btn{display:inline-flex;align-items:center;gap:6px;min-height:36px;padding:0 12px;border-radius:8px;border:1px dashed var(--line);background:transparent;color:var(--fg);font:inherit;font-size:14px;font-weight:700;cursor:pointer;position:relative}
.filter-btn svg{width:15px;height:15px}
.filter-btn[data-n]:not([data-n="0"])::after{content:attr(data-n);display:inline-grid;place-items:center;min-width:20px;height:20px;padding:0 6px;border-radius:999px;background:var(--blue);color:#fff;font-size:12px}
.applied{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.applied:empty{display:none}
.applied button{display:inline-flex;align-items:center;gap:6px;min-height:28px;padding:0 10px;border-radius:999px;border:1px solid var(--blue);background:var(--blue-soft);color:var(--blue);font:inherit;font-size:12.5px;font-weight:700;cursor:pointer}
.applied button i{font-style:normal;opacity:.7}
.fpop{position:fixed;inset:0;z-index:40;display:grid;place-items:center;padding:16px}
.fpop-back{position:absolute;inset:0;background:rgba(6,12,20,.45);animation:lbFade .2s ease}
.fpop-box{position:relative;width:min(560px,100%);max-height:calc(100vh - 32px);overflow:auto;background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:16px;box-shadow:0 30px 60px rgba(0,0,0,.35);animation:lbPop .25s cubic-bezier(.2,.8,.2,1)}
.fpop-head{display:flex;align-items:center;justify-content:space-between;padding:14px 18px;border-bottom:1px solid var(--line);font-weight:800;font-size:16px}
.fpop-head .lb-close{background:rgba(14,28,46,.08);color:var(--fg)}
.fgroup{padding:12px 18px;border-bottom:1px solid var(--line)}
.fgroup:last-of-type{border-bottom:0}
.fgroup h4{margin:0 0 8px;font-size:13px;color:var(--muted);font-weight:700}
.fchips{display:flex;gap:6px;flex-wrap:wrap}
.fchips button{min-height:34px;padding:0 12px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--fg);font:inherit;font-size:13.5px;font-weight:600;cursor:pointer}
.fchips button[aria-pressed="true"]{background:var(--blue);border-color:var(--blue);color:#fff}
.fpop-foot{position:sticky;bottom:0;display:flex;gap:10px;padding:12px 18px;background:var(--panel);border-top:1px solid var(--line)}
.fpop-foot .btn{flex:1;min-height:44px}
.fpop-foot .btn-ghost{flex:0 0 auto}
.noresult{grid-column:1/-1;padding:28px 20px;border:1px dashed var(--line);border-radius:14px;text-align:center;color:var(--muted)}
.noresult b{display:block;color:var(--fg);margin-bottom:6px}
@media (max-width:640px){.fpop{place-items:end center;padding:0}.fpop-box{width:100%;max-height:85vh;border-radius:18px 18px 0 0;animation:fsheet .25s ease}}
@keyframes fsheet{from{transform:translateY(40px);opacity:0}to{transform:none;opacity:1}}
body.full .fpop-box{background:#0E1C2E;color:var(--on-dark);border-color:rgba(255,255,255,.14)}
body.full .fpop-head,body.full .fgroup,body.full .fpop-foot{border-color:rgba(255,255,255,.12)}
body.full .fpop-foot{background:#0E1C2E}
body.full .fchips button,body.full .filter-btn{border-color:rgba(255,255,255,.25);color:var(--on-dark)}
body.full .fpop-head .lb-close{background:rgba(255,255,255,.1);color:#fff}
.lb-html{padding:18px 20px;color:#E6EDF5;font-size:15px;line-height:1.7}
.lb-html img{border-radius:12px;margin-bottom:14px;aspect-ratio:16/9;object-fit:cover}
.lb-html dl{display:grid;grid-template-columns:92px 1fr;gap:8px 14px;margin:0}
.lb-html dt{color:#A9B7C6;font-size:13px;font-weight:700;padding-top:2px}
.lb-html dd{margin:0}
.lb-html .ev-note{margin-top:14px;padding:12px 14px;background:rgba(255,232,154,.12);border-left:3px solid #FFD766;border-radius:0 8px 8px 0;font-size:14px}
.lb-html .cta{margin-top:16px}
@media (max-width:480px){.lb-html dl{grid-template-columns:1fr;gap:2px 0}.lb-html dt{margin-top:8px}}''')

# ---------- markup ----------
rep('<div class="tabs" role="tablist" id="tabs"></div>\n          <p class="group-desc" id="groupDesc"></p>',
    '<div class="tabs" role="tablist" id="tabs"></div>\n          <div class="applied" id="applied"></div>\n          <p class="group-desc" id="groupDesc"></p>')
rep('''    <div class="lb-scroll"><img id="lbImg" src="" alt=""></div>
    <figcaption>본사 상품 안내서 · 가격·조건은 안내서 기준일을 따릅니다</figcaption>''',
    '''    <div class="lb-scroll"><img id="lbImg" src="" alt=""><div class="lb-html" id="lbHtml" hidden></div></div>
    <figcaption id="lbCap">본사 상품 안내서 · 가격·조건은 안내서 기준일을 따릅니다</figcaption>''')
rep('<div class="lb" id="lb" hidden role="dialog"',
    '''<div class="fpop" id="fpop" hidden role="dialog" aria-modal="true" aria-labelledby="fpopTitle">
  <div class="fpop-back" id="fpopBack"></div>
  <div class="fpop-box">
    <div class="fpop-head"><span id="fpopTitle">조건으로 찾기</span><button type="button" class="lb-close" id="fpopClose" aria-label="닫기">✕</button></div>
    <div id="fpopBody"></div>
    <div class="fpop-foot"><button type="button" class="btn btn-ghost" id="fpopReset">초기화</button><button type="button" class="btn btn-primary" id="fpopApply">상품 보기</button></div>
  </div>
</div>
<div class="lb" id="lb" hidden role="dialog"''')

# ---------- JS ----------
rep("let DATA = null, activeGroup = 'all';", "let DATA = null, activeGroup = 'all';\nlet FILTERS = {}; // {facetId: Set(values)}")
rep("""  tabs.innerHTML = all.map(g => `<button class="tab" role="tab" type="button" data-group="${esc(g.id)}" aria-selected="${g.id === activeGroup}">${esc(g.name)}</button>`).join('');""",
    """  const n = Object.values(FILTERS).reduce((s, v) => s + v.size, 0);
  tabs.innerHTML = all.map(g => `<button class="tab" role="tab" type="button" data-group="${esc(g.id)}" aria-selected="${g.id === activeGroup}">${esc(g.name)}</button>`).join('') +
    `<button type="button" class="filter-btn" id="filterBtn" data-n="${n}" aria-haspopup="dialog"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 6h16M7 12h10M10 18h4"/></svg>조건으로 찾기</button>`;
  document.getElementById('filterBtn').addEventListener('click', openFilter);
  renderApplied();""")
rep("  const list = DATA.products.filter(p => !p.hidden && (activeGroup === 'all' ? true : p.group === activeGroup));",
    "  const list = DATA.products.filter(p => !p.hidden && (activeGroup === 'all' ? true : p.group === activeGroup) && matchFilters(p));")
rep("""    </article>`).join('');
  const sel = document.getElementById('fProduct');""",
    """    </article>`).join('') || `<div class="noresult"><b>조건에 맞는 상품이 없습니다</b>조건을 하나 줄이거나, 원하시는 조건을 그대로 카톡으로 보내 주시면 맞는 상품을 찾아 드립니다.<div class="cta" style="justify-content:center;margin-top:14px"><button type="button" class="btn btn-ghost" data-reset-filters>조건 초기화</button><a class="btn btn-primary" href="${esc(DATA.branch.kakao || '#contact')}" target="_blank" rel="noopener">카톡으로 조건 보내기</a></div></div>`;
  const sel = document.getElementById('fProduct');""")
rep("function renderCourses() {", """/* ===== 조건 필터 ===== */
function matchFilters(p) {
  const f = p.f || {};
  return Object.entries(FILTERS).every(([k, set]) => {
    if (!set.size) return true;
    if (k === 'deleg') return f.deleg === true;
    const vals = f[k] || [];
    return vals.some(v => set.has(v));
  });
}
function filterLabel(k, v) { const g = (DATA.filters || []).find(x => x.id === k); const o = g && g.opts.find(x => x[0] === v); return g ? `${g.name}: ${o ? o[1] : v}` : v; }
function renderApplied() {
  const box = document.getElementById('applied'); if (!box) return;
  const items = []; Object.entries(FILTERS).forEach(([k, set]) => set.forEach(v => items.push([k, v])));
  box.innerHTML = items.map(([k, v]) => `<button type="button" data-rm="${esc(k)}:${esc(v)}" aria-label="${esc(filterLabel(k, v))} 조건 제거">${esc(filterLabel(k, v))}<i>✕</i></button>`).join('') + (items.length > 1 ? `<button type="button" data-reset-filters style="background:transparent;border-color:var(--line);color:var(--muted)">모두 지우기</button>` : '');
}
function countMatches(tmp) { return DATA.products.filter(p => !p.hidden && (activeGroup === 'all' ? true : p.group === activeGroup) && Object.entries(tmp).every(([k, set]) => !set.size || (k === 'deleg' ? (p.f || {}).deleg === true : ((p.f || {})[k] || []).some(v => set.has(v))))).length; }
let TMP = null;
function openFilter() {
  TMP = {}; Object.entries(FILTERS).forEach(([k, s]) => TMP[k] = new Set(s));
  const body = document.getElementById('fpopBody');
  body.innerHTML = (DATA.filters || []).map(g => `<div class="fgroup"><h4>${esc(g.name)}</h4><div class="fchips">${g.opts.map(([v, l]) => `<button type="button" data-f="${esc(g.id)}" data-v="${esc(v)}" aria-pressed="${TMP[g.id] && TMP[g.id].has(v)}">${esc(l)}</button>`).join('')}</div></div>`).join('');
  updateApplyCount();
  const fp = document.getElementById('fpop'); fp.hidden = false; document.body.classList.add('lb-open');
  body.querySelector('button').focus();
  track('filter_open');
}
function updateApplyCount() { const n = countMatches(TMP); const b = document.getElementById('fpopApply'); b.textContent = n ? `${n}개 상품 보기` : '맞는 상품 없음'; b.disabled = !n; }
function closeFilter() { document.getElementById('fpop').hidden = true; document.body.classList.remove('lb-open'); const fb = document.getElementById('filterBtn'); if (fb) fb.focus(); }
function setupFilter() {
  const fp = document.getElementById('fpop');
  fp.addEventListener('click', e => {
    if (e.target.closest('#fpopBack') || e.target.closest('#fpopClose')) return closeFilter();
    const c = e.target.closest('.fchips button');
    if (c) { const k = c.dataset.f, v = c.dataset.v; TMP[k] = TMP[k] || new Set(); TMP[k].has(v) ? TMP[k].delete(v) : TMP[k].add(v); c.setAttribute('aria-pressed', String(TMP[k].has(v))); updateApplyCount(); return; }
    if (e.target.closest('#fpopReset')) { TMP = {}; fp.querySelectorAll('.fchips button').forEach(b => b.setAttribute('aria-pressed', 'false')); updateApplyCount(); return; }
    if (e.target.closest('#fpopApply')) { FILTERS = {}; Object.entries(TMP).forEach(([k, s]) => { if (s.size) FILTERS[k] = new Set(s); }); closeFilter(); renderTabs(); renderProducts(); track('filter_apply', { filters: Object.entries(FILTERS).map(([k, s]) => k + '=' + [...s].join('|')).join(',') }); document.getElementById('productGrid').scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
  document.addEventListener('click', e => {
    const rm = e.target.closest('[data-rm]');
    if (rm) { const [k, v] = rm.dataset.rm.split(':'); if (FILTERS[k]) { FILTERS[k].delete(v); if (!FILTERS[k].size) delete FILTERS[k]; } renderTabs(); renderProducts(); return; }
    if (e.target.closest('[data-reset-filters]')) { FILTERS = {}; renderTabs(); renderProducts(); }
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !fp.hidden) closeFilter(); });
}

function renderCourses() {""")
# events markup
rep("""  document.getElementById('eventList').innerHTML = DATA.events.map(e => `
    <div><img src="${esc(e.img || 'img/px-couple.jpg')}" alt=""><div><time>${esc(e.date)}</time><b>${esc(e.name)}</b><span>${esc(e.place)} · ${esc(e.note)}</span></div>${e.product ? `<a class="btn btn-ghost" href="#p-${esc(e.product)}" data-show-product="${esc(e.product)}" style="min-height:40px;padding:0 14px;font-size:13px">멤버십 보기</a>` : `<a class="btn btn-ghost" href="#contact" style="min-height:40px;padding:0 14px;font-size:13px">참가 문의</a>`}</div>`).join('');""",
    """  document.getElementById('eventList').innerHTML = DATA.events.map((e, i) => `
    <article class="ev" data-ev="${i}" tabindex="0" role="button" aria-label="${esc(e.name)} 자세히 보기"><img src="${esc(e.img || 'img/px-couple.jpg')}" alt=""><div class="ev-body"><time>${esc(e.date)}</time><b>${esc(e.name)}</b><span>${esc(e.place)} · ${esc(e.note)}</span></div><div class="ev-act"><button type="button" class="btn btn-ghost" data-ev-open="${i}">자세히</button>${e.product ? `<a class="btn btn-ghost" href="#p-${esc(e.product)}" data-show-product="${esc(e.product)}">멤버십 보기</a>` : `<a class="btn btn-primary" href="#contact" data-track="event_cta_click">참가 문의</a>`}</div></article>`).join('');""")
# lightbox: event detail support
rep("""  const open = card => {
    lastFocus = card; img.src = card.dataset.sheet; img.alt = card.dataset.title + ' 상품 안내서'; title.textContent = card.dataset.title;""",
    """  const html = document.getElementById('lbHtml'), cap = document.getElementById('lbCap');
  const show = () => { lb.classList.remove('closing'); lb.hidden = false; document.body.classList.add('lb-open'); document.getElementById('lbClose').focus(); };
  const openEvent = (i, from) => {
    const e = DATA.events[i]; if (!e) return; const dt = e.detail || {};
    lastFocus = from; img.hidden = true; img.src = ''; html.hidden = false; cap.hidden = true; document.getElementById('lbVoice').innerHTML = '';
    title.textContent = e.name;
    const row = (k, v) => v ? `<dt>${k}</dt><dd>${esc(v)}</dd>` : '';
    html.innerHTML = `<img src="${esc(e.img || 'img/px-couple.jpg')}" alt="">` +
      `<dl>${row('일시', dt.when || e.date)}${row('장소', dt.where || e.place)}${row('대상', dt.who)}${row('구성', dt.includes)}${row('비용', dt.fee)}${row('신청', dt.how)}</dl>` +
      (dt.note ? `<p class="ev-note">${esc(dt.note)}</p>` : '') +
      `<div class="cta">${e.product ? `<a class="btn btn-primary" href="#p-${esc(e.product)}" data-show-product="${esc(e.product)}" data-close-lb>멤버십 보기</a>` : `<a class="btn btn-primary" href="${esc(DATA.branch.kakao || '#contact')}" target="_blank" rel="noopener" data-track="event_kakao_click">카톡으로 신청</a>`}<a class="btn btn-ghost" href="tel:${esc((DATA.branch.phone || '').replace(/-/g, ''))}" data-track="event_call_click">전화 ${esc(DATA.branch.phone || '')}</a></div>`;
    show(); track('event_open', { event: e.name });
  };
  const open = card => {
    lastFocus = card; img.hidden = false; html.hidden = true; html.innerHTML = ''; cap.hidden = false;
    img.src = card.dataset.sheet; img.alt = card.dataset.title + ' 상품 안내서'; title.textContent = card.dataset.title;""")
rep("""    lb.classList.remove('closing'); lb.hidden = false; document.body.classList.add('lb-open');
    document.getElementById('lbClose').focus(); track('sheet_open', { product_id: card.id.replace(/^p-/, '') });""",
    """    show(); track('sheet_open', { product_id: card.id.replace(/^p-/, '') });""")
rep("""    if (e.target.closest('#lbClose') || e.target.closest('#lbBack')) return close();
    const card = e.target.closest('.card.has-sheet');""",
    """    if (e.target.closest('#lbClose') || e.target.closest('#lbBack') || e.target.closest('[data-close-lb]')) return close();
    const evb = e.target.closest('[data-ev-open]'); if (evb) return openEvent(+evb.dataset.evOpen, evb);
    const ev = e.target.closest('.evt .ev'); if (ev && !e.target.closest('a, button')) return openEvent(+ev.dataset.ev, ev);
    const card = e.target.closest('.card.has-sheet');""")
rep("""    if ((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('has-sheet')) { e.preventDefault(); open(e.target); }""",
    """    if ((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('has-sheet')) { e.preventDefault(); open(e.target); }
    if ((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('ev')) { e.preventDefault(); openEvent(+e.target.dataset.ev, e.target); }""")
rep("  setupVideo(); countUp(); setupLightbox(); setupVoice();", "  setupVideo(); countUp(); setupLightbox(); setupVoice(); setupFilter();")
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
