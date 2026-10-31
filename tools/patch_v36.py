import json, re, os, glob
P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, cnt)

# ================= ① 음성 규칙 통일: 여성(윤서) 단일, 토글 제거, FAQ 음성 전면 제거 =================
# --- data: site.json ---
d = json.load(open('data/site.json', encoding='utf-8'))
def only_f(v):
    if not v: return v
    if 'f' in v or 'm' in v:
        v = v.get('f') or v.get('m')
    if v.get('src'): v['src'] = v['src'].replace('-f.mp3', '.mp3')
    return v
for p in d['products']:
    if p.get('voice'): p['voice'] = only_f(p['voice'])
for b in d['benefits']:
    if b.get('voice'): b['voice'] = only_f(b['voice'])

# 섹션 음성 (여성 윤서) — src/sec은 생성 후 채움
d['sections'] = {
  "promo": {
    "title": "100구좌 한정 프로모션",
    "script": "100구좌 한정 프로모션입니다. 프리미엄 소멸형과 5년 반환형 상품에 적용됩니다. 국내 정산 그린피 최대 100% 면제, 5년 반환형은 5년 후 보증금 100% 반환입니다. 적용 골프장과 조건은 본사 기준표를 따르며 자료에 함께 안내해 드립니다. 선착순 마감이라 남은 구좌는 상담 시 확인해 드립니다.",
    "say": "백 구좌 한정 프로모션입니다. 프리미엄 소멸형과 오년 반환형 상품에 적용됩니다. 국내 정산 그린피 최대 백 퍼센트 면제, 오년 반환형은 오년 후 보증금 백 퍼센트 반환입니다. 적용 골프장과 조건은 본사 기준표를 따르며, 자료에 함께 안내해 드립니다. 선착순 마감이라, 남은 구좌는 상담 시 확인해 드립니다."
  },
  "corp": {
    "title": "법인 임원을 위한 조건",
    "script": "법인 임원을 위한 조건, 세 가지만 기억하세요. 첫째, 기명 1 + 무기명 3. 대표나 임원 한 분은 기명으로, 나머지 세 자리는 회사가 지정하는 누구나 쓸 수 있어 접대와 복지를 한 장으로 해결합니다. 둘째, 위임. 연 30회·50회 상품은 회원 없이 거래처 손님만 라운드하게 할 수 있고, 동반 3인까지 회원가가 적용됩니다. 셋째, 명의개서와 양도. 담당 임원이 바뀌면 입회 1년 후 연 1회 기명인을 바꿀 수 있고, 입회 5년 후에는 2회 양도가 가능합니다. 견적서 양식과 약관은 자료로 먼저 드립니다.",
    "say": "법인 임원을 위한 조건, 세 가지만 기억하세요. 첫째, 기명 한 분에 무기명 세 자리. 대표나 임원 한 분은 기명으로, 나머지 세 자리는 회사가 지정하는 누구나 쓸 수 있어, 접대와 복지를 한 장으로 해결합니다. 둘째, 위임. 연 삼십회, 오십회 상품은 회원 없이 거래처 손님만 라운드하게 할 수 있고, 동반 세 분까지 회원가가 적용됩니다. 셋째, 명의개서와 양도. 담당 임원이 바뀌면 입회 일년 후 연 한 번 기명인을 바꿀 수 있고, 입회 오년 후에는 두 번 양도가 가능합니다. 견적서 양식과 약관은 자료로 먼저 드립니다."
  },
  "manager": {
    "title": "강현식 지사장 인사",
    "own": True,
    "script": "안녕하세요, 퍼시픽링스코리아 수도권지사장 강현식입니다. 이 페이지의 상담은 상담사가 아니라 제가 직접 받습니다. 회원 가입부터 예약·페이백·행사까지 같은 사람이 끝까지 담당합니다. 궁금한 점은 아래 번호나 카카오톡으로 편하게 연락 주세요. 24시간 안에 답드리겠습니다.",
    "say": "",
    "src": "", "sec": 0
  }
}
json.dump(d, open('data/site.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# --- data: faq.json (voice 제거) ---
f = json.load(open('data/faq.json', encoding='utf-8'))
for it in f['items']: it.pop('voice', None)
json.dump(f, open('data/faq.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
for fn in glob.glob('media/voice/faq-*.mp3') + glob.glob('media/voice/*-m.mp3'):
    os.remove(fn)
for fn in glob.glob('media/voice/*-f.mp3'):
    os.rename(fn, fn.replace('-f.mp3', '.mp3'))

# --- markup: voicePick 제거 ---
s = h.index('          <div class="voice-pick" id="voicePick"'); e = h.index('\n', s)
h = h[:s] + h[e+1:]
# --- css: voice-pick 제거 ---
h = re.sub(r'\n\.voice-pick[^\n]*', '', h)
h = re.sub(r'\nbody\.full \.voice-pick[^\n]*', '', h)

# --- js: 성별 상태 제거, 단일 voice 객체 ---
rep("let VOICE_GENDER = 'm'; try { VOICE_GENDER = localStorage.getItem('plk-voice') === 'f' ? 'f' : 'm'; } catch (e) {}\nfunction vo(p) { return (p.voice && (p.voice[VOICE_GENDER] || p.voice.m)) || null; }",
    "function vo(p) { return p && p.voice && p.voice.script ? p.voice : null; }")
rep("function voiceSec(p) { const v = vo(p); return (v.sec || p.voice.sec) || Math.round((v.say || v.script).length / 5.5); }",
    "function voiceSec(p) { const v = vo(p); return v.sec || Math.round((v.say || v.script).length / 5.5); }")
# 공통 버튼 마크업 헬퍼
rep("function voiceMarkup(p, withText) {",
    "function vbtnHtml(label, sec, src) { return `<button type=\"button\" class=\"vbtn${src ? '' : ' tts-only'}\" data-state=\"idle\" data-tip=\"설명 듣기${sec ? ' · ' + sec + '초' : ''}\" aria-label=\"${esc(label)} 설명 듣기${sec ? ', ' + sec + '초' : ''}\" aria-pressed=\"false\"><svg class=\"ring\" viewBox=\"0 0 56 56\" aria-hidden=\"true\"><circle class=\"bg\" cx=\"28\" cy=\"28\" r=\"26\"/><circle class=\"fg\" cx=\"28\" cy=\"28\" r=\"26\"/></svg><span class=\"ico\" aria-hidden=\"true\">${ICON_HEAD}</span></button>`; }\nfunction renderSectionVoices() { document.querySelectorAll('[data-section-voice]').forEach(el => { el.innerHTML = sectionVoice(el.dataset.sectionVoice); }); }\nfunction sectionVoice(id) { const v = DATA.sections && DATA.sections[id]; if (!v || !v.script || (v.own && !v.src)) return ''; return `<div class=\"voice\" data-section-id=\"${esc(id)}\">${vbtnHtml(v.title, v.sec || Math.round((v.say || v.script).length / 5.5), v.src)}</div>`; }\nfunction voiceMarkup(p, withText) {")
rep('''    <button type="button" class="vbtn${v.src ? '' : ' tts-only'}" data-state="idle" data-tip="설명 듣기 · ${sec}초" aria-label="${esc(p.name)} 설명 듣기, ${sec}초" aria-pressed="false"><svg class="ring" viewBox="0 0 56 56" aria-hidden="true"><circle class="bg" cx="28" cy="28" r="26"/><circle class="fg" cx="28" cy="28" r="26"/></svg><span class="ico" aria-hidden="true">${ICON_HEAD}</span></button>''',
    '''    ${vbtnHtml(p.name, sec, v.src)}''')
# benefits 버튼 → 헬퍼
rep('''${b.voice ? `<div class="voice" data-benefit-id="${esc(b.id)}"><button type="button" class="vbtn tts-only" data-state="idle" data-tip="설명 듣기" aria-label="${esc(b.title)} 설명 듣기" aria-pressed="false"><svg class="ring" viewBox="0 0 56 56" aria-hidden="true"><circle class="bg" cx="28" cy="28" r="26"/><circle class="fg" cx="28" cy="28" r="26"/></svg><span class="ico" aria-hidden="true">${ICON_HEAD}</span></button></div>` : ''}''',
    '''${b.voice ? `<div class="voice" data-benefit-id="${esc(b.id)}">${vbtnHtml(b.title, b.voice.sec || '', b.voice.src)}</div>` : ''}''')
# voiceOf: 단일 규칙
rep('''  if (box.dataset.benefitId) { const b = (DATA.benefits || []).find(x => x.id === box.dataset.benefitId); const v = b && b.voice && (b.voice[VOICE_GENDER] || b.voice.f || b.voice.m); return v ? Object.assign({ id: 'benefit-' + b.id }, v) : null; }
  if (box.dataset.faq) { const q = (FAQ.items || []).find(x => x.id === box.dataset.faq); if (!q || !q.a) return null; const t = q.q + ' ' + faqPlain(q); const v = (q.voice || {})[VOICE_GENDER] || (q.voice || {}).f || (q.voice || {}).m || {}; return { id: 'faq-' + q.id, script: t, say: t, src: v.src, sec: v.sec }; }
  const p = DATA.products.find(x => x.id === box.dataset.id); const v = p && vo(p);
  return v ? Object.assign({ id: p.id }, v) : null;''',
    '''  if (box.dataset.sectionId) { const v = (DATA.sections || {})[box.dataset.sectionId]; return v ? Object.assign({ id: 'sec-' + box.dataset.sectionId }, v) : null; }
  if (box.dataset.benefitId) { const b = (DATA.benefits || []).find(x => x.id === box.dataset.benefitId); return b && b.voice ? Object.assign({ id: 'benefit-' + b.id }, b.voice) : null; }
  const p = DATA.products.find(x => x.id === box.dataset.id); const v = vo(p);
  return v ? Object.assign({ id: p.id }, v) : null;''')
rep("  track('voice_play', { product_id: id, mode: VOICE.mode, gender: VOICE_GENDER });", "  track('voice_play', { product_id: id, mode: VOICE.mode });")
rep("u.pitch = VOICE_GENDER === 'f' ? 1.05 : 0.95;", "u.pitch = 1.05;")
rep('''  const pick = document.getElementById('voicePick');
  const syncPick = () => pick.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.g === VOICE_GENDER)));
  syncPick();
  pick.addEventListener('click', e => {
    const b = e.target.closest('button[data-g]'); if (!b || b.dataset.g === VOICE_GENDER) return;
    VOICE_GENDER = b.dataset.g; try { localStorage.setItem('plk-voice', VOICE_GENDER); } catch (err) {}
    syncPick(); renderProducts(); track('voice_gender', { gender: VOICE_GENDER });
  });
''', '')
rep("renderTabs(); renderProducts(); renderCourses(); renderEvents(); renderFaq(); renderBenefits();\n", "renderTabs(); renderProducts(); renderCourses(); renderEvents(); renderFaq(); renderBenefits(); renderSectionVoices();\n")
# FAQ 음성 버튼 제거
rep('''          ${it.a ? `<div class="voice" data-faq="${esc(it.id)}"><button type="button" class="vbtn${(it.voice && (it.voice.f || it.voice.m)) ? '' : ' tts-only'}" data-state="idle" data-tip="답변 듣기${(it.voice && (it.voice.f || it.voice.m)) ? ' · ' + ((it.voice.f || it.voice.m).sec || '') + '초' : ''}" aria-label="답변 듣기" aria-pressed="false"><svg class="ring" viewBox="0 0 56 56" aria-hidden="true"><circle class="bg" cx="28" cy="28" r="26"/><circle class="fg" cx="28" cy="28" r="26"/></svg><span class="ico" aria-hidden="true">${ICON_HEAD}</span></button></div>` : ''}
''', '')

# ================= ② 섹션 음성 버튼 슬롯 (프로모션 · 법인 · 담당자) =================
rep('''<div class="cta"><a class="btn btn-primary" href="#contact" data-track="promo_cta_click" data-product="premium-refund-5y">프리미엄 자료 받기</a><a class="btn btn-ghost" href="#products" data-track="promo_cards_click">상품 카드 보기</a></div>''',
    '''<div class="cta sec-cta"><a class="btn btn-primary" href="#contact" data-track="promo_cta_click" data-product="premium-refund-5y">프리미엄 자료 받기</a><a class="btn btn-ghost" href="#products" data-track="promo_cards_click">상품 카드 보기</a><span data-section-voice="promo"></span></div>''')
rep('''<div class="cta" style="margin-top:22px"><a class="btn btn-primary" href="#contact" data-track="corp_cta_click" data-product="corp-life-30">법인 자료 받기</a><a class="btn btn-ghost" href="#products" data-show-product="corp-life-30">법인 상품 카드 보기</a></div>''',
    '''<div class="cta sec-cta" style="margin-top:22px"><a class="btn btn-primary" href="#contact" data-track="corp_cta_click" data-product="corp-life-30">법인 자료 받기</a><a class="btn btn-ghost" href="#products" data-show-product="corp-life-30">법인 상품 카드 보기</a><span data-section-voice="corp"></span></div>''')
rep('''        <div class="phone"><span id="phoneText">010-4734-2000</span><button class="copy" type="button" id="copyPhone">번호 복사</button></div>''',
    '''        <div class="phone"><span id="phoneText">010-4734-2000</span><button class="copy" type="button" id="copyPhone">번호 복사</button><span class="mgr-voice" data-section-voice="manager"></span></div>''')
# css
rep('.cta{display:flex;gap:12px;flex-wrap:wrap}', '.cta{display:flex;gap:12px;flex-wrap:wrap}\n.sec-cta{align-items:center}\n.sec-cta .voice{margin-left:2px}\n.mgr-voice{display:inline-flex;margin-left:8px;vertical-align:middle}')
rep('.fq-act .voice{--c-acc:var(--blue);--c-fg:var(--fg);--c-line:var(--line);--c-bg:#fff}', '.sec-cta .voice,.mgr-voice .voice{--c-acc:var(--blue);--c-fg:var(--fg);--c-line:var(--line);--c-bg:#fff}\n.band.dark .sec-cta .voice,.mgr-voice .voice{--c-acc:#FFD766;--c-fg:#fff;--c-bg:#0E1C2E;--c-line:rgba(255,255,255,.25)}\n.band.dark .sec-cta .vbtn,.mgr-voice .vbtn{color:#0E1C2E}\n.band.dark .sec-cta .vbtn[data-state="paused"],.mgr-voice .vbtn[data-state="paused"]{background:#fff;color:#0E1C2E}')
rep('body.no-tts .vbtn.tts-only{display:none}', 'body.no-tts .vbtn.tts-only{display:none}\n.band.dark .vbtn .ring .bg{stroke:rgba(255,255,255,.25)}')

# ---------- fallback 재생성 ----------
s = h.index('window.__SITE_FALLBACK__ = '); e = h.index('\n', s)
h = h[:s] + 'window.__SITE_FALLBACK__ = ' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ';' + h[e:]
s = h.index('window.__FAQ_FALLBACK__ = '); e = h.index('\n', s)
h = h[:s] + 'window.__FAQ_FALLBACK__ = ' + json.dumps(f, ensure_ascii=False, separators=(',', ':')) + ';' + h[e:]

assert 'VOICE_GENDER' not in h and 'voicePick' not in h and 'voice-pick' not in h and 'data-faq=' not in h, 'leftover'
open(P, 'w', encoding='utf-8').write(h)
print('ok', len(h))
