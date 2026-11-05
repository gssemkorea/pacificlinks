import re
P='pacificlinks-branch-mvp.html'; h=open(P,encoding='utf-8').read()
def rep(a,b):
    global h
    assert a in h, a[:90]; h=h.replace(a,b,1)
# 오버레이 CSS 제거
h=re.sub(r'\.cfh-unmute\{[^\n]*\n\.cfh-unmute svg\{[^\n]*\n\.cfh-unmute:hover\{[^\n]*\n\.cf-box\.playing\.muted-auto \.cfh-unmute\{[^\n]*\n@media \(max-width:860px\)\{\.cfh-unmute\{[^\n]*\n','',h)
assert '.cfh-unmute' not in h
# 오버레이 버튼 제거
h,n=re.subn(r'\n[ \t]*<button class="cfh-unmute" type="button" id="cfHeroUnmute">.*?</button>','',h,flags=re.S); assert n==1
rep("  document.getElementById('cfHeroUnmute').addEventListener('click', () => { soundOff = false; v.muted = false; v.currentTime = 0; userPaused = false; play(); syncSnd(); track('hero_cf_unmute_overlay'); });\n",'')
rep("ev.target.closest('#cfHeroSound, #cfHeroPause, #cfHeroUnmute')","ev.target.closest('#cfHeroSound, #cfHeroPause')")
# 첫 입력 때 소리 켜기 + 앞부분(15초 이내)이면 처음부터 다시
rep("if (!soundOff && v.muted) { v.muted = false; if (v.paused && started && !userPaused) play(); } };",
    "if (!soundOff && v.muted) { v.muted = false; if (v.currentTime < 15) v.currentTime = 0; if (v.paused && started && !userPaused) play(); track('hero_cf_unmute_gesture'); } };")
assert 'cfHeroUnmute' not in h
open(P,'w',encoding='utf-8').write(h)
i=h.index('</style>')+len('</style>')
open('index.html','w',encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'+h[:i]+'</head><body>'+h[i:]+'</body></html>')
print('ok')
