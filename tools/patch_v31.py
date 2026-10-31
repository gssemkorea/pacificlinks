import json
P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)
faq = json.load(open('data/faq.json', encoding='utf-8'))

# ---------- voice: generic source (product or FAQ) ----------
rep('''function voiceStart(box) {
  const id = box.dataset.id, p = DATA.products.find(x => x.id === id);
  if (!p || !p.voice) return;
  voiceReset();
  const v = vo(p);
  VOICE.box = box;''', '''function voiceOf(box) {
  if (box.dataset.faq) { const q = (FAQ.items || []).find(x => x.id === box.dataset.faq); if (!q || !q.a) return null; const t = faqPlain(q); return { id: 'faq-' + q.id, script: t, say: t }; }
  const p = DATA.products.find(x => x.id === box.dataset.id); const v = p && vo(p);
  return v ? Object.assign({ id: p.id }, v) : null;
}
function voiceStart(box) {
  const v = voiceOf(box); if (!v) return; const id = v.id;
  voiceReset();
  VOICE.box = box;''')
rep("    const fallback = () => { if (VOICE.audio !== a) return; VOICE.audio = null; a.onended = a.onerror = null; voiceTTS(p, 0); };",
    "    const fallback = () => { if (VOICE.audio !== a) return; VOICE.audio = null; a.onended = a.onerror = null; voiceTTS(v, 0); };")
rep("  } else voiceTTS(p, 0);\n  track('voice_play', { product_id: id, mode: VOICE.mode, gender: VOICE_GENDER });",
    "  } else voiceTTS(v, 0);\n  track('voice_play', { product_id: id, mode: VOICE.mode, gender: VOICE_GENDER });")
rep("function voiceTTS(p, from) {", "function voiceTTS(vv, from) {")
rep("  const vv = vo(p), box = VOICE.box, says = splitSents(vv.say || vv.script), n = says.length;",
    "  const box = VOICE.box, says = splitSents(vv.say || vv.script), n = says.length;")
rep("if (VOICE.box === box && VOICE.state === 'playing') { setProgress(1); voiceFinish(p.id); } };",
    "if (VOICE.box === box && VOICE.state === 'playing') { setProgress(1); voiceFinish(vv.id); } };")
rep("    else { const p = DATA.products.find(x => x.id === box.dataset.id); voiceTTS(p, Math.max(0, VOICE.idx)); }",
    "    else { const vv = voiceOf(box); if (vv) voiceTTS(vv, Math.max(0, VOICE.idx)); }")
rep("    track('voice_pause', { product_id: box.dataset.id }); return;", "    track('voice_pause', { product_id: box.dataset.id || ('faq-' + box.dataset.faq) }); return;")

# ---------- FAQ module ----------
rep("let DATA = null, activeGroup = 'all';", "let DATA = null, activeGroup = 'all';\nlet FAQ = { items: [], categories: [], glossary: [] }, faqCat = 'all', faqQuery = '', faqProduct = '';")
rep("async function loadData() {", '''async function loadFaq() {
  try { const r = await fetch('data/faq.json', { cache: 'no-store' }); if (r.ok) return await r.json(); } catch (e) {}
  return window.__FAQ_FALLBACK__;
}
function faqPlain(q) { return String(q.a || '').replace(/\\*\\*(.+?)\\*\\*/g, '$1'); }
function termFor(txt) { const g = FAQ.glossary || []; return g.find(t => t.term === txt) || g.find(t => txt.includes(t.term) || t.term.includes(txt)) || null; }
function faqAnswerHtml(q) {
  if (!q.a) return `<p class="fq-pending">${esc(FAQ.pendingText || '상담 시 안내')}</p>`;
  return '<p>' + esc(q.a).replace(/\\*\\*(.+?)\\*\\*/g, (m, t) => { const g = termFor(t); return g ? `<button type="button" class="term" data-term="${esc(g.id)}" aria-label="${esc(g.term)} 용어 설명">${t}</button>` : `<b>${t}</b>`; }) + '</p>';
}
function hl(text, qry) { const t = esc(text); if (!qry) return t; const re = new RegExp('(' + qry.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi'); return t.replace(re, '<mark>$1</mark>'); }
function renderFaq() {
  const tabs = document.getElementById('faqTabs'); if (!tabs) return;
  const cats = [{ id: 'all', name: '전체' }, { id: 'first', name: '처음이신가요?' }, ...(FAQ.categories || [])];
  tabs.innerHTML = cats.map(c => `<button class="tab" type="button" data-fcat="${esc(c.id)}" aria-selected="${c.id === faqCat}">${esc(c.name)}</button>`).join('');
  const q = faqQuery.trim().toLowerCase();
  let list = (FAQ.items || []).filter(it => {
    if (faqProduct && !(it.products || []).includes(faqProduct)) return false;
    if (faqCat === 'first') return (FAQ.beginner || []).includes(it.id);
    if (faqCat !== 'all' && it.cat !== faqCat) return false;
    return !q || (it.q + ' ' + faqPlain(it)).toLowerCase().includes(q);
  });
  if (faqCat === 'first') list = (FAQ.beginner || []).map(id => list.find(x => x.id === id)).filter(Boolean);
  const pname = faqProduct ? (DATA.products.find(p => p.id === faqProduct) || {}).name : '';
  document.getElementById('faqCount').innerHTML = (pname ? `<b>${esc(pname)}</b> 관련 ` : '') + `${list.length}개` + (pname ? ` <button type="button" class="faq-clear" data-faq-product="">전체 보기 ✕</button>` : '');
  const open = faqCat === 'first' || !!q;
  document.getElementById('faqList').innerHTML = list.map(it => `
    <details class="fq${it.a ? '' : ' pending'}" id="faq-${esc(it.id)}"${open ? ' open' : ''}>
      <summary><span class="qm">Q</span><b>${hl(it.q, q)}</b><span class="chev" aria-hidden="true"></span></summary>
      <div class="fq-body">${faqAnswerHtml(it)}
        <div class="fq-act">
          ${it.a ? `<div class="voice" data-faq="${esc(it.id)}"><button type="button" class="vbtn tts-only" data-state="idle" data-tip="답변 듣기" aria-label="답변 듣기" aria-pressed="false"><svg class="ring" viewBox="0 0 56 56" aria-hidden="true"><circle class="bg" cx="28" cy="28" r="26"/><circle class="fg" cx="28" cy="28" r="26"/></svg><span class="ico" aria-hidden="true">${ICON_HEAD}</span></button></div>` : ''}
          <button type="button" class="btn btn-ghost" data-consult-q="${esc(it.id)}">이 질문으로 상담</button>
          <small>근거: ${esc(it.src || '')}${it.status === 'partial' ? ' · 일부 본사 확인 중' : ''}</small>
        </div>
      </div>
    </details>`).join('') || `<div class="noresult"><b>찾는 답이 없네요</b>그 질문 그대로 카톡으로 보내 주세요. 지사장이 직접 답합니다.<div class="cta" style="justify-content:center;margin-top:14px"><a class="btn btn-primary" href="${esc(DATA.branch.kakao || '#contact')}" target="_blank" rel="noopener">카톡으로 질문 보내기</a></div></div>`;
}
function showTerm(btn) {
  document.querySelectorAll('.term-tip').forEach(t => t.remove());
  const g = (FAQ.glossary || []).find(t => t.id === btn.dataset.term); if (!g) return;
  const tip = document.createElement('div'); tip.className = 'term-tip'; tip.setAttribute('role', 'tooltip');
  tip.innerHTML = `<b>${esc(g.term)}</b><span>${esc(g.desc)}</span>${g.faq && g.faq !== (btn.closest('.fq') || {}).id?.replace('faq-', '') ? `<a href="#faq-${esc(g.faq)}" data-faq-go="${esc(g.faq)}">FAQ에서 더 보기 →</a>` : ''}<button type="button" class="term-x" aria-label="닫기">✕</button>`;
  btn.insertAdjacentElement('afterend', tip);
  track('term_tooltip', { term: g.id });
}
function setupFaq() {
  const sec = document.getElementById('faq'); if (!sec) return;
  const inp = document.getElementById('faqSearch');
  let t0 = null; inp.addEventListener('input', () => { clearTimeout(t0); t0 = setTimeout(() => { faqQuery = inp.value; renderFaq(); if (faqQuery.trim()) track('faq_search', { q: faqQuery.trim(), n: document.querySelectorAll('#faqList .fq').length }); }, 150); });
  sec.addEventListener('click', e => {
    const tb = e.target.closest('[data-fcat]'); if (tb) { faqCat = tb.dataset.fcat; renderFaq(); track('faq_tab', { cat: faqCat }); return; }
    const tm = e.target.closest('.term'); if (tm) { showTerm(tm); return; }
    if (e.target.closest('.term-x')) { document.querySelectorAll('.term-tip').forEach(t => t.remove()); return; }
    const go = e.target.closest('[data-faq-go]'); if (go) { e.preventDefault(); openFaq(go.dataset.faqGo); return; }
    const cq = e.target.closest('[data-consult-q]'); if (cq) { consultWithQuestion(cq.dataset.consultQ, cq); return; }
    const s = e.target.closest('summary'); if (s) { const d = s.parentElement; if (!d.open) track('faq_open', { id: d.id.replace('faq-', '') }); }
  });
  document.addEventListener('click', e => {
    const fp = e.target.closest('[data-faq-product]');
    if (fp) { e.preventDefault(); faqProduct = fp.dataset.faqProduct; faqCat = 'all'; faqQuery = ''; inp.value = ''; renderFaq(); if (faqProduct) { const lb = document.getElementById('lb'); if (lb && !lb.hidden) document.getElementById('lbClose').click(); setTimeout(() => sec.scrollIntoView({ behavior: 'smooth', block: 'start' }), 220); } }
    if (!e.target.closest('.term') && !e.target.closest('.term-tip')) document.querySelectorAll('.term-tip').forEach(t => t.remove());
  });
}
function openFaq(id) {
  faqProduct = ''; faqCat = 'all'; faqQuery = ''; const inp = document.getElementById('faqSearch'); if (inp) inp.value = '';
  renderFaq(); const d = document.getElementById('faq-' + id); if (d) { d.open = true; d.scrollIntoView({ behavior: 'smooth', block: 'center' }); d.querySelector('summary').focus(); }
}
async function consultWithQuestion(id, btn) {
  const it = (FAQ.items || []).find(x => x.id === id); if (!it) return;
  const msg = `[PLK 수도권지사 상담 신청]\\n궁금한 점: ${it.q}` + (faqProduct ? `\\n상품: ${(DATA.products.find(p => p.id === faqProduct) || {}).name || ''}` : '') + `\\n성함: \\n연락처: `;
  try { await navigator.clipboard.writeText(msg); btn.textContent = '복사됨 · 카톡에 붙여넣기'; } catch (e) { btn.textContent = '카톡으로 이동'; }
  track('faq_to_consult', { id }); setTimeout(() => window.open(DATA.branch.kakao || '#contact', '_blank', 'noopener'), 300);
  setTimeout(() => btn.textContent = '이 질문으로 상담', 2500);
}
async function loadData() {''')
rep("  renderTabs(); renderProducts(); renderCourses(); renderEvents();", "  FAQ = await loadFaq();\n  renderTabs(); renderProducts(); renderCourses(); renderEvents(); renderFaq();")
rep("  setupVideo(); countUp(); setupLightbox(); setupVoice(); setupFilter();", "  setupVideo(); countUp(); setupLightbox(); setupVoice(); setupFilter(); setupFaq();")
# lightbox caption → product FAQ link
rep("    img.src = card.dataset.sheet; img.alt = card.dataset.title + ' 상품 안내서'; title.textContent = card.dataset.title;",
    "    img.src = card.dataset.sheet; img.alt = card.dataset.title + ' 상품 안내서'; title.textContent = card.dataset.title;\n    const pid = card.id.replace(/^p-/, ''), nq = (FAQ.items || []).filter(x => (x.products || []).includes(pid)).length;\n    cap.innerHTML = '본사 상품 안내서 · 가격·조건은 안내서 기준일을 따릅니다' + (nq ? ` · <a href=\"#faq\" data-faq-product=\"${esc(pid)}\">이 상품 자주 묻는 질문 ${nq}개 →</a>` : '');")
# fallback data
h = h.replace("window.__SITE_FALLBACK__ = ", "window.__FAQ_FALLBACK__ = " + json.dumps(faq, ensure_ascii=False, separators=(',', ':')) + ";\nwindow.__SITE_FALLBACK__ = ", 1)

# ---------- markup: section + nav ----------
rep('<a href="#events">행사</a><a href="#manager">담당자</a>', '<a href="#events">행사</a><a href="#faq">FAQ</a><a href="#manager">담당자</a>')
rep('  <section class="band dark manager-band" id="manager" aria-label="담당자">', '''  <section class="band" id="faq" aria-label="자주 묻는 질문">
    <div class="wrap">
      <div class="sec-title">
        <div class="eyebrow">FAQ</div>
        <h2>자주 묻는 질문</h2>
        <p class="lead muted">처음이시면 '처음이신가요?'부터. 점선 용어를 누르면 뜻이 뜨고, 답마다 들을 수 있습니다.</p>
      </div>
      <div class="faq-tools">
        <label class="faq-search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg><input type="search" id="faqSearch" placeholder="궁금한 말을 입력하세요 — 양도, 주말, 세금, 페이백" aria-label="FAQ 검색"></label>
        <div class="tabs" id="faqTabs" role="tablist"></div>
        <p class="faq-count muted" id="faqCount" aria-live="polite"></p>
      </div>
      <div class="faq-list" id="faqList"></div>
      <p class="note">FAQ 기준일 <span id="faqUpdated">2026.10.30</span> · 본사 확인 중인 항목은 상담에서 안내합니다.</p>
    </div>
  </section>

  <section class="band dark manager-band" id="manager" aria-label="담당자">''')

# ---------- CSS ----------
rep('.noresult{grid-column:1/-1;', '''/* FAQ */
.faq-tools{display:grid;gap:12px;margin-bottom:18px}
.faq-search{display:flex;align-items:center;gap:10px;max-width:560px;min-height:50px;padding:0 16px;border:1px solid var(--line);border-radius:12px;background:var(--panel)}
.faq-search svg{width:18px;height:18px;color:var(--muted);flex:none}
.faq-search input{flex:1;min-width:0;border:0;background:transparent;font:inherit;font-size:16px;color:var(--fg);outline:none}
.faq-count{margin:0;font-size:13.5px}
.faq-clear{margin-left:8px;border:1px solid var(--line);background:transparent;color:var(--fg);border-radius:999px;padding:3px 10px;font:inherit;font-size:12.5px;font-weight:700;cursor:pointer}
.faq-list{display:grid;gap:10px;max-width:860px}
.fq{border:1px solid var(--line);border-radius:14px;background:var(--panel);overflow:hidden}
.fq summary{display:grid;grid-template-columns:34px 1fr 24px;align-items:center;gap:12px;padding:16px 18px;cursor:pointer;list-style:none;font-size:16.5px;font-weight:700;min-height:56px}
.fq summary::-webkit-details-marker{display:none}
.fq summary:hover{background:var(--blue-soft)}
.fq summary:focus-visible{outline:3px solid var(--blue-light);outline-offset:-3px}
.fq .qm{display:inline-grid;place-items:center;width:34px;height:34px;border-radius:10px;background:var(--blue-soft);color:var(--blue);font-family:var(--latin);font-weight:700;font-size:15px}
.fq[open] .qm{background:var(--blue);color:#fff}
.fq .chev{width:10px;height:10px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg);transition:transform .2s;justify-self:center}
.fq[open] .chev{transform:rotate(-135deg)}
.fq mark{background:#FFE89A;color:inherit;border-radius:3px;padding:0 2px}
.fq-body{padding:2px 18px 18px 64px;font-size:16px;line-height:1.8;position:relative}
.fq-body p{margin:0;text-align:justify}
.fq-pending{color:var(--muted);padding:10px 14px;background:var(--bg);border-radius:10px;font-size:14.5px}
.term{font:inherit;background:none;border:0;padding:0;color:var(--blue);font-weight:700;border-bottom:2px dotted var(--blue-light);cursor:pointer}
.term-tip{position:relative;display:grid;gap:4px;margin:10px 0 4px;padding:12px 40px 12px 14px;background:var(--blue-soft);border:1px solid var(--blue-light);border-radius:10px;font-size:14px;line-height:1.6;animation:lbPop .2s ease}
.term-tip b{color:var(--blue)}
.term-tip a{color:var(--blue);font-weight:700;text-decoration:none}
.term-x{position:absolute;right:8px;top:8px;width:28px;height:28px;border:0;border-radius:50%;background:rgba(14,28,46,.08);color:var(--fg);cursor:pointer;font-size:13px}
.fq-act{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:14px}
.fq-act .voice{--c-acc:var(--blue);--c-fg:var(--fg);--c-line:var(--line);--c-bg:#fff}
.fq-act .vbtn{width:42px;height:42px;box-shadow:none}
.fq-act .vbtn .ico svg{width:19px;height:19px}
.fq-act .vbtn::after{right:auto;left:0}
.fq-act .btn{min-height:40px;padding:0 14px;font-size:13.5px}
.fq-act small{font-size:12.5px;color:var(--muted);margin-left:auto}
@media (max-width:640px){.fq summary{grid-template-columns:30px 1fr 20px;padding:14px;font-size:15.5px}.fq .qm{width:30px;height:30px;font-size:14px}.fq-body{padding:0 14px 16px 14px;font-size:15px}.fq-act small{margin-left:0;flex-basis:100%}}
body.full .fq,body.full .faq-search{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.14)}
body.full .fq summary:hover{background:rgba(255,255,255,.06)}
body.full .fq .qm{background:rgba(255,255,255,.12);color:#fff}
body.full .fq-pending{background:rgba(255,255,255,.06)}
body.full .term-tip{background:rgba(26,90,163,.25);border-color:var(--blue-light);color:var(--on-dark)}
body.full .faq-search input{color:var(--on-dark)}
body.full .fq-act .voice{--c-fg:var(--on-dark);--c-line:rgba(255,255,255,.2)}
.noresult{grid-column:1/-1;''')
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
