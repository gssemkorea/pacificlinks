import json, re
P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
lines = h.split('\n')

def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    raise SystemExit('not found: ' + prefix)

# ---------- CSS: voice block ----------
a = find('/* 음성 설명 */'); b = find('@media (prefers-reduced-motion:reduce){.voice-bar i')
voice_css = r'''/* 음성 설명: 원버튼 (헤드폰 → 일시정지 → 이어듣기 / 다시듣기) */
.card .act{display:flex;align-items:center;gap:12px}
.voice{position:relative;flex:none}
.vbtn{position:relative;width:48px;height:48px;border-radius:50%;border:0;padding:0;background:var(--c-acc);color:#fff;cursor:pointer;display:grid;place-items:center;box-shadow:0 8px 18px rgba(0,0,0,.18);transition:transform .15s,box-shadow .2s;font:inherit}
.vbtn:hover{transform:translateY(-1px)}
.card[data-tier="corp"] .vbtn,.card[data-tier="premium"] .vbtn{color:#0E1C2E}
.vbtn .ico{position:relative;z-index:1;display:grid;place-items:center;width:22px;height:22px}
.vbtn .ico svg{width:22px;height:22px}
.vbtn .ring{position:absolute;inset:-5px;width:calc(100% + 10px);height:calc(100% + 10px);transform:rotate(-90deg);pointer-events:none;opacity:0;transition:opacity .2s}
.vbtn .ring circle{fill:none;stroke-width:3}
.vbtn .ring .bg{stroke:var(--c-line)}
.vbtn .ring .fg{stroke:var(--c-acc);stroke-linecap:round;stroke-dasharray:164;stroke-dashoffset:164;transition:stroke-dashoffset .25s linear}
.vbtn[data-state="playing"] .ring,.vbtn[data-state="paused"] .ring,.vbtn[data-state="done"] .ring{opacity:1}
.vbtn[data-state="playing"]{animation:vpulse 1.6s ease-out infinite}
.vbtn[data-state="paused"]{background:var(--c-fg);color:var(--c-bg,#fff)}
.card[data-tier="corp"] .vbtn[data-state="paused"],.card[data-tier="premium"] .vbtn[data-state="paused"]{background:#fff;color:#0E1C2E}
@keyframes vpulse{0%{box-shadow:0 8px 18px rgba(0,0,0,.18),0 0 0 0 color-mix(in srgb,var(--c-acc) 50%,transparent)}100%{box-shadow:0 8px 18px rgba(0,0,0,.18),0 0 0 14px transparent}}
.vbtn::after{content:attr(data-tip);position:absolute;bottom:calc(100% + 12px);right:0;background:#0E1C2E;color:#fff;font-size:12.5px;font-weight:700;line-height:1;padding:8px 11px;border-radius:7px;white-space:nowrap;opacity:0;transform:translateY(4px);transition:opacity .15s,transform .15s;pointer-events:none;z-index:2}
.vbtn:hover::after,.vbtn:focus-visible::after{opacity:1;transform:none}
.vbtn:focus-visible{outline:3px solid var(--c-acc);outline-offset:3px}
body.no-tts .vbtn.tts-only{display:none}
.voice-script{text-align:justify;font-size:14.5px;line-height:1.8;color:var(--c-mut)}
.voice-script span{border-radius:4px;padding:1px 3px;transition:background .2s,color .2s}
.voice-script span.on{background:#FFE89A;color:#0E1C2E;font-weight:700}
.card .who,.card .details li,.sec-copy .lead{text-align:justify}
@media (prefers-reduced-motion:reduce){.vbtn{animation:none!important}.vbtn .ring .fg,.voice-script span{transition:none}}'''.split('\n')
lines[a:b+1] = voice_css
i = find('.card .act .btn{width:100%}'); lines[i] = '.card .act .btn{flex:1;width:auto}'

# ---------- CSS: popup voice strip ----------
a = find('.lb-voice{--c-acc'); b = find('.lb-voice .voice-script{')
lines[a:b+1] = r'''.lb-voice{--c-acc:#C9A86A;--c-fg:#fff;--c-mut:#B7C2CE;--c-line:rgba(255,255,255,.14)}
.lb-voice:empty{display:none}
.lbv{display:grid;grid-template-columns:auto 1fr;align-items:center;gap:8px 12px;padding:10px 16px 12px;border-bottom:1px solid rgba(255,255,255,.1)}
.lbv .vbtn{width:40px;height:40px;color:#0B1220;box-shadow:none}
.lbv .vbtn .ico svg{width:19px;height:19px}
.lbv .vbtn[data-state="paused"]{background:#fff;color:#0B1220}
.lbv .vbtn::after{right:auto;left:0}
.lbv .vlbl{font-size:13.5px;font-weight:700;color:#fff}
.lbv .vlbl small{display:block;font-weight:500;color:#B7C2CE;font-size:12px;margin-top:2px}
.lbv .voice-script{grid-column:1/-1;display:none;font-size:14px;line-height:1.7;max-height:110px;overflow:auto;padding-right:4px}
.lbv.on .voice-script{display:block}'''.split('\n')

# ---------- CSS: header light + logo, tabs ----------
i = find('header{position:sticky')
lines[i] = 'header{position:sticky;top:env(safe-area-inset-top,0px);z-index:9;background:rgba(255,255,255,.94);color:var(--fg);backdrop-filter:blur(10px);border-bottom:1px solid rgba(14,28,46,.08)}'
i = find('.brand img{'); lines[i] = '.brand img{height:46px;width:auto}'
i = find('.brand small{'); lines[i] = '.brand small{font-size:12.5px;font-weight:700;color:var(--muted);white-space:nowrap;border-left:1px solid rgba(14,28,46,.18);padding-left:12px}'
i = find('.anchors a{'); lines[i] = '.anchors a{text-decoration:none;color:#3B4A59;font-weight:600}'
i = find('.anchors a:hover{'); lines[i] = '.anchors a:hover{color:var(--blue)}'
i = find('.ver{'); lines[i] = '.ver{border:1px solid rgba(14,28,46,.22);color:var(--fg);background:transparent;border-radius:999px;padding:6px 12px;font-size:12px;cursor:pointer;font-family:var(--body)}'
i = find('body.full body.full body.full .tab{')
lines[i] = '.tab{border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:8px;min-height:36px;padding:0 14px;font:inherit;font-size:14px;font-weight:700;line-height:1;cursor:pointer;transition:background .15s,color .15s}\n.tab:hover{border-color:var(--blue);color:var(--blue)}'
i = find('.tabs{display:flex;gap:8px'); lines[i] = '.tabs{display:flex;gap:6px;flex-wrap:wrap}'
i = find('.tab[aria-selected="true"]{'); lines[i] = '.tab[aria-selected="true"],.tab[aria-selected="true"]:hover{background:var(--blue);border-color:var(--blue);color:#fff}'
# namecard css
i = find('.phone{'); lines.insert(i+1, '.namecard{display:block;width:min(440px,100%);margin-top:22px;border-radius:10px;box-shadow:0 18px 40px rgba(0,0,0,.45)}')

h = '\n'.join(lines)

# ---------- markup ----------
def rep(a, b, cnt=1):
    global h
    assert a in h, a[:70]
    h = h.replace(a, b, cnt)
rep('<img src="img/lockup-white.png" alt="퍼시픽링스코리아">\n      <small>수도권지사</small>', '<img src="img/logo-color.png" alt="퍼시픽링스코리아">\n      <small>수도권지사</small>')
rep('''<div class="phone"><span id="phoneText">010-4734-2000</span><button class="copy" type="button" id="copyPhone">번호 복사</button></div>
      </div>''', '''<div class="phone"><span id="phoneText">010-4734-2000</span><button class="copy" type="button" id="copyPhone">번호 복사</button></div>
        <img class="namecard" src="img/namecard.jpg" alt="강현식 지사장 명함 — 서울 강남구 역삼로 235 위너스빌딩 3F, T 1522-1642, earnie@pacificlinks.co.kr">
      </div>''')
rep('''      <p class="who">${esc(p.who)}</p>
      ${p.voice && p.voice.script ? voiceMarkup(p) : ''}
''', '''      <p class="who">${esc(p.who)}</p>
''')
rep('''<div class="act"><a class="btn btn-primary" href="#contact" data-track="product_cta_click" data-product="${esc(p.id)}">이 상품 자료 받기</a></div>''',
    '''<div class="act"><a class="btn btn-primary" href="#contact" data-track="product_cta_click" data-product="${esc(p.id)}">이 상품 자료 받기</a>${p.voice && p.voice.script ? voiceMarkup(p) : ''}</div>''')
rep("document.getElementById('lbVoice').innerHTML = vp && vp.voice ? voiceMarkup(vp) : '';",
    "document.getElementById('lbVoice').innerHTML = vp && vp.voice ? voiceMarkup(vp, true) : '';")
rep("if (lb.hidden) return; lb.classList.add('closing'); if (VOICE.box && lb.contains(VOICE.box)) voiceStop();",
    "if (lb.hidden) return; lb.classList.add('closing'); if (VOICE.box && lb.contains(VOICE.box)) voiceReset();")
rep("function renderProducts() {\n  voiceStop();\n", "function renderProducts() {\n  voiceReset();\n")

# ---------- JS: replace the voice module ----------
a = h.index('/* ===== 음성 설명: 자체 mp3 > 브라우저 음성(Web Speech) ===== */'); b = h.index('function countUp() {')
js = r'''/* ===== 음성 설명: 원버튼 플레이어. 자체 mp3 > 브라우저 음성(Web Speech) ===== */
const ICON_HEAD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="13" width="4.5" height="7" rx="2"/><rect x="16.5" y="13" width="4.5" height="7" rx="2"/></svg>';
const ICON_PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>';
const ICON_PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.5v13l11-6.5z"/></svg>';
const ICON_REPLAY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/></svg>';
const VOICE = { audio: null, box: null, btn: null, mode: null, idx: -1, sents: [], bounds: [], state: 'idle' };
const TIPS = { idle: '설명 듣기', playing: '멈춤', paused: '이어 듣기', done: '다시 듣기' };
function splitSents(t) { return String(t).split(/(?<=[.!?])\s+/).map(s => s.trim()).filter(Boolean); }
function voiceSec(p) { return p.voice.sec || Math.round((p.voice.say || p.voice.script).length / 5.5); }
function voiceMarkup(p, withText) {
  const sec = voiceSec(p), sents = splitSents(p.voice.script);
  return `<div class="voice${withText ? ' lbv' : ''}" data-id="${esc(p.id)}">
    <button type="button" class="vbtn${p.voice.src ? '' : ' tts-only'}" data-state="idle" data-tip="설명 듣기 · ${sec}초" aria-label="${esc(p.name)} 설명 듣기, ${sec}초" aria-pressed="false"><svg class="ring" viewBox="0 0 56 56" aria-hidden="true"><circle class="bg" cx="28" cy="28" r="26"/><circle class="fg" cx="28" cy="28" r="26"/></svg><span class="ico" aria-hidden="true">${ICON_HEAD}</span></button>
    ${withText ? `<span class="vlbl">음성 설명 · ${sec}초<small>버튼을 누르면 설명이 글로도 따라옵니다</small></span><div class="voice-script">${sents.map(s => `<span>${esc(s)}</span>`).join(' ')}</div>` : ''}
  </div>`;
}
function koVoice() { try { return speechSynthesis.getVoices().find(v => /^ko/i.test(v.lang)) || null; } catch (e) { return null; } }
function checkTTS() { document.body.classList.toggle('no-tts', !('speechSynthesis' in window) || !koVoice()); }
function setState(st) {
  VOICE.state = st; const b = VOICE.btn; if (!b) return;
  b.dataset.state = st; b.querySelector('.ico').innerHTML = { idle: ICON_HEAD, playing: ICON_PAUSE, paused: ICON_PLAY, done: ICON_REPLAY }[st];
  b.dataset.tip = TIPS[st]; b.setAttribute('aria-pressed', String(st === 'playing'));
  if (VOICE.box) VOICE.box.classList.toggle('on', st === 'playing' || st === 'paused');
}
function setProgress(k) { const fg = VOICE.btn && VOICE.btn.querySelector('.ring .fg'); if (fg) fg.style.strokeDashoffset = (164 * (1 - Math.max(0, Math.min(1, k)))).toFixed(1); }
function voiceHighlight(i) { if (!VOICE.box) return; VOICE.box.querySelectorAll('.voice-script span').forEach((s, k) => s.classList.toggle('on', k === i)); VOICE.idx = i; }
function voiceReset(done) {
  if (VOICE.audio) { const a = VOICE.audio; VOICE.audio = null; a.onended = a.onerror = a.ontimeupdate = null; a.pause(); }
  if (VOICE.mode === 'tts') { VOICE.mode = null; try { speechSynthesis.cancel(); } catch (e) {} }
  if (VOICE.btn) { setState(done ? 'done' : 'idle'); setProgress(done ? 1 : 0); if (!done) voiceHighlight(-1); }
  VOICE.btn = null; VOICE.box = null; VOICE.mode = null; VOICE.idx = -1; VOICE.state = 'idle';
}
function voiceFinish(id) { track('voice_complete', { product_id: id }); voiceReset(true); }
function voiceStart(box) {
  const id = box.dataset.id, p = DATA.products.find(x => x.id === id);
  if (!p || !p.voice) return;
  voiceReset();
  VOICE.box = box; VOICE.btn = box.querySelector('.vbtn'); VOICE.sents = splitSents(p.voice.script);
  setProgress(0); voiceHighlight(-1);
  if (p.voice.src) {
    VOICE.mode = 'mp3';
    const a = new Audio(p.voice.src); VOICE.audio = a; a.preload = 'auto';
    const lens = VOICE.sents.map(s => s.length), total = lens.reduce((x, y) => x + y, 0);
    let acc = 0; VOICE.bounds = lens.map(l => (acc += l) / total);
    a.ontimeupdate = () => {
      if (VOICE.audio !== a || !a.duration) return; const k = a.currentTime / a.duration; setProgress(k);
      const i = VOICE.bounds.findIndex(b => k < b); if (i >= 0 && i !== VOICE.idx) voiceHighlight(i);
    };
    a.onended = () => { if (VOICE.audio === a) voiceFinish(id); };
    const fallback = () => { if (VOICE.audio !== a) return; VOICE.audio = null; a.onended = a.onerror = null; voiceTTS(p, 0); };
    a.onerror = fallback;
    a.play().then(() => { if (VOICE.audio === a) { setState('playing'); voiceHighlight(0); } }).catch(fallback);
  } else voiceTTS(p, 0);
  track('voice_play', { product_id: id, mode: VOICE.mode });
}
function voiceTTS(p, from) {
  const v = koVoice();
  if (!v) { const b = VOICE.btn; voiceReset(); if (b) { b.dataset.tip = '이 기기는 음성 미지원 · 전화 주세요'; b.classList.add('tts-only'); } return; }
  VOICE.mode = 'tts'; try { speechSynthesis.cancel(); } catch (e) {}
  const box = VOICE.box, says = splitSents(p.voice.say || p.voice.script), n = says.length;
  says.slice(from).forEach((s, k) => {
    const u = new SpeechSynthesisUtterance(s); u.voice = v; u.lang = 'ko-KR'; u.rate = 1; u.pitch = 0.95;
    u.onstart = () => { if (VOICE.box !== box || VOICE.state !== 'playing') return; voiceHighlight(Math.min(from + k, VOICE.sents.length - 1)); setProgress((from + k) / n); };
    if (from + k === n - 1) u.onend = () => { if (VOICE.box === box && VOICE.state === 'playing') { setProgress(1); voiceFinish(p.id); } };
    speechSynthesis.speak(u);
  });
  setState('playing');
}
function voiceToggle(box) {
  if (VOICE.box === box && VOICE.state === 'playing') {
    setState('paused'); if (VOICE.audio) VOICE.audio.pause(); else { try { speechSynthesis.cancel(); } catch (e) {} }
    track('voice_pause', { product_id: box.dataset.id }); return;
  }
  if (VOICE.box === box && VOICE.state === 'paused') {
    if (VOICE.audio) VOICE.audio.play().then(() => setState('playing')).catch(() => voiceStart(box));
    else { const p = DATA.products.find(x => x.id === box.dataset.id); voiceTTS(p, Math.max(0, VOICE.idx)); }
    return;
  }
  voiceStart(box);
}
function setupVoice() {
  checkTTS(); if ('speechSynthesis' in window) speechSynthesis.addEventListener('voiceschanged', checkTTS);
  document.addEventListener('click', e => { const b = e.target.closest('.vbtn'); if (b) voiceToggle(b.closest('.voice')); });
  document.addEventListener('visibilitychange', () => { if (document.hidden && VOICE.mode === 'tts' && VOICE.state === 'playing') voiceToggle(VOICE.box); });
}

'''
h = h[:a] + js + h[b:]

# ---------- data: display script (digits) + say (TTS) ----------
d = json.load(open('data/site.json', encoding='utf-8'))
REPL = [('이백칠십여 곳', '276곳'), ('일 플러스 일 라이프 오십', '1+1 라이프 50'), ('피엘케이 소멸형 이 년', 'PLK 소멸형 2년'), ('피엘케이 오 년 반환형 삼십', 'PLK 5년 반환형 30'), ('피엘케이 소멸형 위켄드', 'PLK 소멸형 Weekend'),
        ('개인 라이프 이십', '개인 라이프 20'), ('개인 라이프 삼십', '개인 라이프 30'), ('개인 라이프 오십', '개인 라이프 50'), ('법인 라이프 삼십', '법인 라이프 30'), ('법인 라이프 오십', '법인 라이프 50'),
        ('일 년에 스무 번', '1년에 20번'), ('일 년에 서른 번', '1년에 30번'), ('일 년에 쉰 번', '1년에 50번'), ('일 년에 열 번 또는 스무 번', '1년에 10번 또는 20번'),
        ('한 달에 두 번', '한 달에 2번'), ('한 달에 세 번', '한 달에 3번'), ('한 달에 다섯 번', '한 달에 5번'), ('동반 세 분', '동반 3분'), ('네 분까지', '4분까지'),
        ('오 년이 지나면', '5년이 지나면'), ('오 년 뒤', '5년 뒤'), ('이 년 동안', '2년 동안'), ('이 년이 지나면', '2년이 지나면'), ('이용 기간은 이 년', '이용 기간은 2년'), ('서른 번 또는 쉰 번', '30번 또는 50번'), ('서른 번을 모두 주말', '30번을 모두 주말')]
for p in d['products']:
    say = p['voice']['say'] if 'say' in p['voice'] else p['voice']['script']
    disp = say
    for a_, b_ in REPL: disp = disp.replace(a_, b_)
    p['voice']['say'] = say; p['voice']['script'] = disp
    assert len(splitSents := re.split(r'(?<=[.!?])\s+', disp)) == len(re.split(r'(?<=[.!?])\s+', say)), p['id']
json.dump(d, open('data/site.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
s = h.index('window.__SITE_FALLBACK__ = '); e = h.index('\n', s)
h = h[:s] + 'window.__SITE_FALLBACK__ = ' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ';' + h[e:]
open(P, 'w', encoding='utf-8').write(h)
print('patched'); print(d['products'][0]['voice']['script'])
