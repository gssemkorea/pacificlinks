# 퍼시픽링스코리아 수도권지사 — 원페이지 MVP

`pacificlinks.kr` 지사 사이트 MVP. 정적 파일(HTML/CSS/JS + JSON 데이터 + 미디어)만으로 동작합니다.

## 구조

```
index.html                     배포용 페이지 (doctype/head 포함)
pacificlinks-branch-mvp.html   작업 원본 (아티팩트 미리보기용, index.html과 본문 동일)
data/
  site.json                    상품·그룹·필터·행사·혜택·섹션 음성 (가격 기준일 포함)
  faq.json                     FAQ 항목·용어집
img/                           로고·상품 시트·인물·행사 이미지
media/
  hero.mp4, cf.mp4             히어로·CF 영상
  voice/*.mp3                  음성 설명 (여성 단일, Google Chirp3-HD 윤서 / loudnorm -16 LUFS)
tools/patch_v*.py              버전별 변경 스크립트 (이력용)
```

## 로컬 확인

```bash
python3 -m http.server 8000
# http://localhost:8000/index.html
```

`fetch`로 `data/*.json`을 읽으므로 `file://`로 열면 인라인 fallback(`window.__SITE_FALLBACK__`)이 대신 쓰입니다.

## 데이터 수정 규칙

- 가격·조건은 `data/site.json` → 수정 후 `pacificlinks-branch-mvp.html`의 `window.__SITE_FALLBACK__`도 같이 갱신 (tools/ 스크립트 참고).
- 음성 파일명: 상품 `media/voice/<product-id>.mp3`, 혜택 `benefit-<id>.mp3`, 섹션 `sec-<id>.mp3`. `src`/`sec`(초)를 JSON에 기록.
- 담당자 육성은 `media/voice/sec-manager.mp3`를 넣고 `sections.manager.src/sec`를 채우면 버튼이 표시됩니다.
