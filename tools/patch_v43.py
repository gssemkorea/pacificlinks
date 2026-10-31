P = 'pacificlinks-branch-mvp.html'
h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:90]; h = h.replace(a, b, 1)

# ---- 풋터: 수상 배지 + 본사 법적 표기 ----
rep('''      <p>퍼시픽링스코리아 수도권지사 · 서울 강남구 역삼로 235 위너스빌딩 6층 · 사업자등록번호·통신판매업 신고번호는 본사 현행 기준으로 표기</p>
      <p>© Pacific Links Korea. 수도권지사 강현식 지사장.</p>''',
'''      <div class="awards" aria-label="수상">
        <figure><img src="img/award-webaward.png" alt="웹어워드코리아"><figcaption><b>2018 웹어워드코리아</b><span>서비스업 분야 최우수상</span></figcaption></figure>
        <figure><img src="img/award-starbrand.png" alt="스타브랜드 대상 2022"><figcaption><b>2022 스타브랜드 대상</b><span>골프멤버십 부문 · 2년 연속</span></figcaption></figure>
      </div>
      <p>퍼시픽링스코리아 유한책임회사 · 법인대표자 장옥영 · 사업자등록번호 481-88-03349 · 통신판매업신고 제2024-서울강남-06189호 · 관광사업 등록 강남-2017-87 · 전화권유판매신고 2024-서울강남-00025호 · 방문판매업신고 2024-서울강남-00059호</p>
      <p>수도권지사 · 서울 강남구 역삼로 235 위너스빌딩 · 담당 강현식 지사장 010-4734-2000</p>
      <p>© Pacific Links Korea. 본 페이지는 퍼시픽링스코리아 수도권지사가 운영합니다.</p>''')
rep('footer img{height:28px;width:auto;margin-bottom:14px;opacity:.8}',
'''footer>.wrap>img{height:28px;width:auto;margin-bottom:14px;opacity:.8}
footer .awards{display:flex;gap:28px;flex-wrap:wrap;margin:6px 0 18px}
footer .awards figure{display:flex;align-items:center;gap:12px;margin:0}
footer .awards img{height:56px;width:auto;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.12)}
footer .awards figcaption{display:grid;gap:2px;line-height:1.3}
footer .awards b{color:var(--fg);font-size:13px}
footer .awards span{font-size:12px}
body.full footer .awards b{color:var(--on-dark)}''')
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok')
