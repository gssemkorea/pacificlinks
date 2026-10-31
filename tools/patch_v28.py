import json, re
P = 'pacificlinks-branch-mvp.html'
d = json.load(open('data/site.json', encoding='utf-8'))
byid = {p['id']: p for p in d['products']}

# ---------- verified figures from HQ sheets ----------
U = {
 'personal-life-30': dict(priceText='2,900만원', priceNote='입회비 · VAT 포함 · 연회비 60만원 · 2026.05.01 본사 기준',
    keys=['연 30회 (해외 추가 연 5회)', '제휴 골프장 그린피 50%', '평생 이용 · 양도 가능'],
    details=['월 3회 · 주중·주말 구분 없음 (수도권 성수기 주중 2회·주말 1회)', '동일 골프장 월 2회 · 주중 2회를 주말 1회로 변경 가능', '위임·명의개서 해당 없음', '입회 5년 후 2회 양도·양수 가능 (최초 입회일부터 15년까지)', '미사용 횟수 이월 불가'],
    sheet='img/sheet-personal-30-50.jpg'),
 'personal-life-50': dict(priceText='4,500만원', priceNote='입회비 · VAT 포함 · 연회비 78만원 · 2026.05.01 본사 기준',
    keys=['연 50회 (해외 추가 연 10회)', '제휴 골프장 그린피 50%', '평생 이용 · 양도 가능 · 위임 연 12회'],
    details=['월 5회 · 주중·주말 구분 없음 (수도권 성수기 주중 3회·주말 2회)', '동일 골프장 월 2회 · 주중 2회를 주말 1회로 변경 가능', '위임 연 12회(월 1회) · 명의개서 해당 없음', '입회 5년 후 2회 양도·양수 가능 (최초 입회일부터 15년까지)', '미사용 횟수 이월 불가'],
    sheet='img/sheet-personal-30-50.jpg'),
 'personal-1plus1-50': dict(who='부부 또는 파트너 두 명이 함께 (기명 2인 지정 가능)', priceText='8,500만원', priceNote='입회비 · VAT 포함 · 연회비 150만원 · 2026.05.01 본사 기준',
    keys=['기명 1 + 무기명 1 · 두 명이 연 50회 공유', '제휴 골프장 그린피 50%', '평생 이용 · 양도 가능'],
    details=['연 50회 (해외 추가 연 10회) · 월 5회 (주중 3회·주말 2회)', '동일 골프장 월 2회 · 주중 2회를 주말 1회로 변경 가능', '위임·명의개서 해당 없음', '입회 5년 후 2회 양도·양수 가능 (최초 입회일부터 15년까지)', '미사용 횟수 이월 불가'],
    sheet='img/sheet-life50-trio.jpg'),
 'corp-life-30': dict(priceText='1억 1,900만원', priceNote='입회비 · VAT 포함 · 연회비 220만원 · 2026.06.01 본사 기준',
    keys=['기명 1 + 무기명 3 · 연 30회 (해외 추가 연 5회)', '제휴 골프장 그린피 50% · 위임 연 30회', '평생 이용 · 양도 가능'],
    details=['월 3회 · 주중·주말 구분 없음 (수도권 성수기 주중 2회·주말 1회)', '동일 골프장 월 2회 · 주중 2회를 주말 1회로 변경 가능', '명의개서: 입회 1년 경과 후 연 1회 기명인 변경', '입회 5년 후 2회 양도·양수 가능 (최초 입회일부터 15년까지)', '법인 비용 처리는 세무 확인 후 안내'],
    sheet='img/sheet-corp-30-50.jpg'),
 'corp-life-50': dict(priceText='1억 6,900만원', priceNote='입회비 · VAT 포함 · 연회비 280만원 · 2026.06.01 본사 기준',
    keys=['기명 1 + 무기명 3 · 연 50회 (해외 추가 연 10회)', '제휴 골프장 그린피 50% · 위임 연 50회', '평생 이용 · 양도 가능'],
    details=['월 5회 · 주중·주말 구분 없음 (수도권 성수기 주중 3회·주말 2회)', '해외 위임은 최대 10회 (총 50회 중)', '명의개서: 입회 1년 경과 후 연 1회 기명인 변경', '입회 5년 후 2회 양도·양수 가능 (최초 입회일부터 15년까지)', '미사용 횟수 이월 불가'],
    sheet='img/sheet-corp-30-50.jpg'),
}
for k, v in U.items(): byid[k].update(v)
byid['corp-delegate']['priceNote'] = '본사 기준표 미수령 · 확인 후 표기'

# ---------- new products ----------
def voice(say_m, say_f=None):
    return {'m': {'say': say_m}, 'f': {'say': say_f or say_m}}
NEW = [
 dict(id='premium-expire-long', group='premium', name='프리미엄 소멸형 3년 · 5년', badge='기업 맞춤형', bg='img/bg-dusk.jpg', sheet='img/sheet-premium-expire-3y5y.jpg',
      who='그린피 면제와 100% 위임이 필요한 법인, 3년 또는 5년',
      keys=['연 30회 (주중 20·주말 10) 또는 연 50회 (주중 30·주말 20)', '4인 정산 그린피 면제 · 100% 위임', '이용기간 3년 또는 5년 · 해외 연간 횟수 내 제한 없음'],
      priceText='7,800만원 ~ 1억 9,000만원', priceNote='3년: 30회 7,800만 · 50회 1억 2,600만 / 5년: 30회 1억 2,500만 · 50회 1억 9,000만 · VAT 별도 · 2026.05.01 본사 기준',
      details=['월 5회(30) / 월 7회(50)', '양도·양수 해당 없음', '동일 골프장 월 2회 · 주중 2회를 주말 1회로 변경 가능', '미사용 횟수 이월 불가 · 해외 골프장은 골프장별 상이'], featured=False,
      voice=voice('퍼시픽링스 수도권지사 강현식입니다. 프리미엄 소멸형 삼 년, 오 년 상품은, 그린피 면제와 백 퍼센트 위임이 필요한 법인을 위한 상품입니다. 일 년에 서른 번 또는 쉰 번, 네 분까지 정산 그린피가 면제되고 손님에게 전부 위임하실 수 있습니다. 이용 기간은 삼 년 또는 오 년 중에 고르시고, 기간이 끝나면 입회금은 돌아오지 않습니다. 가격은 화면의 금액을 확인해 주시고, 부가세는 별도입니다. 궁금한 점은 전화 주세요. 제가 직접 받습니다.')),
 dict(id='premium-refund-5y-50', group='premium', name='PLK 5년 반환형 50 · 올그린 60', badge='전액 반환', bg='img/bg-tee.jpg', sheet='img/sheet-refund5-50-60.jpg',
      who='입회금 전액 반환이 조건인 법인·개인',
      keys=['입회금 전액 반환: 50회 3억원 · 올그린 60회 6억원', '4인 정산 그린피 50% (올그린 60회는 100%)', '연 50회 월 5회 / 연 60회 월 6회 · 명의개서 1년 후 연 1회'],
      priceText='3억원 · 6억원', priceNote='전액 반환 · 연회비 400만 · 800만원(VAT 별도) · 2026.02.01 본사 기준 — 현행 여부 본사 확인 중',
      details=['50회 → 올그린 25회(4인 그린피 100%, 연 25회·월 3회)로 변경 선택 가능', '양도·양수 해당 없음 · 이용기간 5년', '반환형 상품으로 세금계산서 미발행 (계약서·회원권 확인서 발급)', '동일 골프장 월 2회 · 주중 2회를 주말 1회로 변경 · 이월 불가'], featured=False,
      voice=voice('퍼시픽링스 수도권지사 강현식입니다. 피엘케이 오 년 반환형 쉰 번과 올그린 예순 번은, 입회금 전액이 돌아오는 것이 조건인 분을 위한 상품입니다. 오 년 뒤 입회금 전액을 돌려받으시고, 네 분 정산 그린피는 쉰 번 상품이 절반, 올그린은 전액 면제입니다. 한 달에 다섯 번 또는 여섯 번까지 쓰시고, 입회 일 년 뒤부터는 해마다 한 번 명의를 바꾸실 수 있습니다. 금액과 연회비는 화면을 확인해 주시고, 자세한 조건은 전화 주시면 제가 직접 설명드립니다.')),
 dict(id='premium-gold', group='premium', name='프리미엄 골드 (1+3)', badge='본사 확인 중', bg='img/bg-warm.jpg', sheet='img/sheet-premium-gold.jpg', hidden=True,
      who='8년간 고정 그린피(국내 주중 8만원·해외 $60)로 라운드하는 법인',
      keys=['국내 주중 8만원 · 주말 12만원(수도권·강원) 고정 그린피 · 해외 $60', '연 60회 (국내 48 · 해외 12) · 100% 위임', '해외여행 상품권 1,000만원 또는 메이저 대회 직관 투어'],
      priceText='1억 9,900만원', priceNote='VAT 포함 · 8년 소멸형 · 2024.01.01 기준 (현재 판매 여부 본사 확인 필요)',
      details=['명의개서: 입회 1년 후 연 1회', '동일 골프장 월 2회 · 주중 2회를 주말 1회로 변경 가능', '미사용 횟수 이월 불가 · 해외는 골프장별 2~12회'], featured=False,
      voice=voice('퍼시픽링스 수도권지사 강현식입니다. 프리미엄 골드는, 팔 년 동안 국내 주중 그린피 팔만 원, 해외 육십 달러로 라운드하시는 법인 맞춤 상품입니다. 일 년에 예순 번, 국내 마흔여덟 번과 해외 열두 번을 쓰시고, 전부 위임이 됩니다. 천만 원 상당 해외여행 상품권도 드립니다. 현재 판매 조건은 본사 확인 후 안내드리겠습니다. 전화 주시면 제가 직접 받습니다.')),
 dict(id='resort-lotus', group='resort', name='로터스밸리CC 5년 멤버십 (태국)', badge='그린피·숙박·조식 0원', bg='img/px-sunset.jpg', sheet='img/sheet-lotus-valley.jpg',
      who='태국에서 한 번에 열흘씩 머물며 라운드하는 분·법인',
      keys=['그린피 + 숙박 + 조식 0원 (Grand Sappaya Hotel)', '3~10월 무제한 · 11~2월 연 30박', '2인용 699만원 (기명 1+무기명 1) · 4인용 1,399만원 (무기명 4)'],
      priceText='699만원 · 1,399만원', priceNote='이용기간 5년 · 2인용 위임 불가 · 4인용 위임 제한 없음',
      details=['카트비·캐디피·중석식·샌딩·이동수단 불포함', '1회 방문 시 최대 10일 체류(성수기) · 재방문은 체크아웃 후 15일 경과', '골프장 이용은 1일 1회 18홀 기준', '11월 지사 해외 골프여행(로터스밸리)과 함께 안내 — 행사 섹션 참고'], featured=True,
      voice=voice('퍼시픽링스 수도권지사 강현식입니다. 로터스밸리 오 년 멤버십은, 태국 로터스밸리 골프장에서 그린피와 숙박, 조식을 내지 않고 머무시는 상품입니다. 삼월부터 시월까지는 횟수 제한 없이, 십일월부터 이월까지는 일 년에 서른 박을 쓰실 수 있습니다. 두 분용과 네 분용이 있고, 카트비와 캐디피, 항공은 따로 내십니다. 지사에서 가는 해외 골프여행과 함께 보시면 좋습니다. 가격은 화면의 금액을 확인해 주시고, 궁금한 점은 전화 주세요. 제가 직접 받습니다.')),
]
REPL = [('이백칠십여 곳', '276곳'), ('삼 년, 오 년', '3년·5년'), ('삼 년 또는 오 년', '3년 또는 5년'), ('백 퍼센트', '100%'), ('일 년에 서른 번 또는 쉰 번', '1년에 30번 또는 50번'),
        ('피엘케이 오 년 반환형 쉰 번과 올그린 예순 번', 'PLK 5년 반환형 50회와 올그린 60회'), ('오 년 뒤', '5년 뒤'), ('쉰 번 상품', '50회 상품'), ('다섯 번 또는 여섯 번', '5번 또는 6번'), ('입회 일 년 뒤', '입회 1년 뒤'),
        ('팔 년 동안', '8년 동안'), ('팔만 원', '8만 원'), ('육십 달러', '60달러'), ('일 년에 예순 번', '1년에 60번'), ('마흔여덟 번', '48번'), ('열두 번', '12번'), ('천만 원', '1,000만 원'),
        ('로터스밸리 오 년 멤버십', '로터스밸리 5년 멤버십'), ('삼월부터 시월', '3월부터 10월'), ('십일월부터 이월', '11월부터 2월'), ('일 년에 서른 박', '1년에 30박'), ('두 분용과 네 분용', '2인용과 4인용')]
F = [('퍼시픽링스 수도권지사 강현식입니다.', '퍼시픽링스 수도권지사입니다.'), ('제가 직접 받습니다.', '강현식 지사장이 직접 받습니다.'), ('제가 직접 설명드립니다.', '강현식 지사장이 직접 설명드립니다.')]
for p in NEW:
    say = p['voice']['m']['say']; disp = say
    for a, b in REPL: disp = disp.replace(a, b)
    fs = say; fd = disp
    for a, b in F: fs = fs.replace(a, b); fd = fd.replace(a, b)
    p['voice'] = {'m': {'script': disp, 'say': say}, 'f': {'script': fd, 'say': fs}}
    assert len(re.split(r'(?<=[.!?])\s+', disp)) == len(re.split(r'(?<=[.!?])\s+', say))
    d['products'].append(p)
d['groups'].append({'id': 'resort', 'name': '해외 리조트', 'desc': '해외 골프장 체류형 멤버십 — 그린피·숙박 포함'})
d['branch']['priceAsOf'] = '2026-11-01'
json.dump(d, open('data/site.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

h = open(P, encoding='utf-8').read()
def rep(a, b):
    global h
    assert a in h, a[:70]; h = h.replace(a, b, 1)
s = h.index('window.__SITE_FALLBACK__ = '); e = h.index('\n', s)
h = h[:s] + 'window.__SITE_FALLBACK__ = ' + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + ';' + h[e:]
# hidden products stay out of the grid and the form
rep("  const list = DATA.products.filter(p => activeGroup === 'all' ? true : p.group === activeGroup);",
    "  const list = DATA.products.filter(p => !p.hidden && (activeGroup === 'all' ? true : p.group === activeGroup));")
rep("DATA.products.map(p => `<option value=\"${esc(p.id)}\">${esc(p.name)}</option>`).join('')",
    "DATA.products.filter(p => !p.hidden).map(p => `<option value=\"${esc(p.id)}\">${esc(p.name)}</option>`).join('')")
rep("  const mark = t => t === 'personal' ? 'img/logo-korea.png' : 'img/logo-white.png';\n  const lock = t => t === 'personal' ? 'img/lockup-blue.png' : 'img/lockup-white.png';",
    "  const light = t => t === 'personal' || t === 'resort';\n  const mark = t => light(t) ? 'img/logo-korea.png' : 'img/logo-white.png';\n  const lock = t => light(t) ? 'img/lockup-blue.png' : 'img/lockup-white.png';")
# resort tier: light sky card with dark text
rep('.card[data-tier="personal"] .g{color:#2E7D4F}',
    '.card[data-tier="personal"] .g{color:#2E7D4F}\n.card[data-tier="resort"]{--c-bg:linear-gradient(180deg,#FFFFFF 0%,#EAF4FD 100%);--c-fg:#0E1C2E;--c-mut:#4F6478;--c-acc:#1A5AA3;--c-soft:#DCEBFA;--c-line:#C8DCEF}\n.card[data-tier="resort"] .who,.card[data-tier="resort"] .details,.card[data-tier="resort"] .price small{color:#4F6478}\n.card[data-tier="resort"] .price b,.card[data-tier="resort"] h3,.card[data-tier="resort"] .keys{color:#0E1C2E}\n.card[data-tier="resort"] .g{color:#1A5AA3}\n.card[data-tier="resort"] .badge{background:#1A5AA3;color:#fff;border-color:#1A5AA3}\n.card[data-tier="resort"] .vbtn{color:#fff}')
open(P, 'w', encoding='utf-8').write(h)
i = h.index('</style>') + len('</style>')
open('index.html', 'w', encoding='utf-8').write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + h[:i] + '</head><body>' + h[i:] + '</body></html>')
print('ok', len(d['products']), [p['id'] for p in d['products']])
