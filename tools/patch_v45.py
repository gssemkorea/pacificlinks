P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

# 헤더 B안: 공식 락업 + 지사 배지 + 메뉴 우측, 헤더 '자료 받기' 제거(플로팅 버튼이 담당), 버전 버튼 최소화
rep('      <small>수도권지사</small>\n', '      <span class="pill">수도권지사</span>\n')
rep('    <a class="hdr-cta" href="#contact" data-track="header_form_click">자료 받기</a>\n', '')
rep('<button class="ver" id="verBtn" type="button" title="배경 버전 전환">버전 A · 섹션형</button>',
    '<button class="ver" id="verBtn" type="button" title="배경 버전 전환 (A 섹션형 / B 전체 배경)" aria-label="배경 버전 전환, 현재 A 섹션형">Ver. A</button>')
rep("  document.getElementById('verBtn').textContent = full ? '버전 B · 전체 배경' : '버전 A · 섹션형';",
    "  const vb = document.getElementById('verBtn'); vb.textContent = full ? 'Ver. B' : 'Ver. A'; vb.setAttribute('aria-label', '배경 버전 전환, 현재 ' + (full ? 'B 전체 배경' : 'A 섹션형'));")

rep('@media (max-width:860px){.brand img{height:28px}.ver{font-size:12px;padding:0 8px}}', '@media (max-width:860px){.brand img{height:28px}}')
rep('.brand small{font-size:12.5px;font-weight:700;color:#5F6B76;white-space:nowrap;border-left:1px solid rgba(14,28,46,.18);padding-left:12px}',
    '.brand .pill{font-size:11.5px;font-weight:800;letter-spacing:.04em;color:#16599E;background:#E9F1FA;border:1px solid #CFE0F3;border-radius:999px;padding:4px 10px;white-space:nowrap;line-height:1}')
rep('.hdr-cta,.ver{white-space:nowrap}\n', '')
rep('@media (max-width:1320px){.anchors{gap:15px;font-size:13.5px}.brand small{display:none}.brand img{height:36px}}',
    '.brand img{height:36px}\n@media (max-width:1320px){.anchors{gap:15px;font-size:13.5px}}\n@media (max-width:1100px){.brand .pill{display:none}}')
h = h.replace(h[h.index('.hdr-cta{display:inline-flex;'):h.index('\n', h.index('.hdr-cta:hover{'))+1], '')
rep('.ver{display:inline-flex;align-items:center;min-height:36px;padding:0 12px;border:1px solid rgba(14,28,46,.25);color:#14202C;background:transparent;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;font-family:var(--body);white-space:nowrap}',
    '.ver{display:inline-flex;align-items:center;min-height:26px;padding:0 8px;border:1px solid rgba(14,28,46,.2);color:#5F6B76;background:transparent;border-radius:6px;font-size:11px;font-weight:700;letter-spacing:.02em;cursor:pointer;font-family:var(--latin);white-space:nowrap}')
rep('@media (max-width:860px){.anchors,.hdr-cta{display:none}.brand small{display:none}.ver{margin-left:auto}}',
    '@media (max-width:860px){.anchors{display:none}.ver{margin-left:auto}}')
assert 'hdr-cta' not in h and 'brand small' not in h
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
