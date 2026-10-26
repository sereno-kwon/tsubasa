# Tsubasa Bicycles Korea

tsubasabicycles.co.kr 원페이지 정적 사이트 (GitHub Pages).

- `index.html` 원페이지 본체, 한국어 원본 (ORIGIN · CROW · PROCESS · ARTWORK · CONCEPT)
- `en/index.html`, `ja/index.html` 영어·일본어 페이지 (자동 생성, 직접 수정하지 않음)
- `i18n/en.json`, `i18n/ja.json` 번역 사전 (한국어 문장 → 번역)
- `tools/build_i18n.py` 번역 페이지 생성 스크립트 (bastioncycles.co.kr과 같은 방식)
- `404.html` 기존 아임웹 하위 주소(/crow 등)와 /en/crow, /ja/process 같은 언어별 주소를 섹션으로 연결
- `images/` 섹션별 이미지 (`hero`, `origin`, `crow`, `process`, `artwork`, `concept`)
- `.github/image-manifest.txt` + `fetch-images.yml` 아임웹 CDN 이미지 이전용 워크플로

## 다국어 (한국어 · English · 日本語)
수정은 항상 한국어 `index.html`에서 합니다. 푸시하면 `build-i18n.yml`이 `en/`, `ja/` 페이지를 다시 만들어 커밋합니다.

- 한국어 문장을 바꾸거나 새로 넣으면 `i18n/en.json`, `i18n/ja.json`의 `text`에 같은 한국어 문장을 키로 번역을 추가해야 합니다.
- 번역이 빠진 문장이 있으면 Actions가 실패하고 빠진 문장을 로그에 보여줍니다. 그동안 영어·일본어 페이지는 이전 버전 그대로 유지됩니다.
- 로컬 확인: `python3 tools/build_i18n.py --check`
- 푸터 사업자 정보처럼 문단 단위로 통째로 바꿔야 하는 부분은 `blocks`에 HTML 그대로 넣습니다.

## 구글 애널리틱스 (GA4)
루비컴퍼니 브랜드 사이트(츠바사·바스티온·팔리·크러스트) 공통 코드입니다.

- 측정 ID가 있는 사이트는 head 맨 위에 구글 태그(gtag.js) 원본 코드를 그대로 넣고, 같은 ID를 `var GA_ID`에도 적습니다(공통 이벤트 스크립트가 사용). ID가 없는 사이트는 `var GA_ID = '';` 자리만 비워 두고 GA를 불러오지 않습니다.
- 페이지 언어가 콘텐츠 그룹(`content_group`: ko, en, ja)으로 기록됩니다.
- 이벤트
  - `section_view` 섹션 도달 (section_name), 섹션별 1회
  - `consulting_click` 상담 링크(rubiworkshop.com/models) 클릭 (link_location: header, menu, 섹션 id, footer)
  - `dealer_click` 루비서플라이 링크 클릭 (link_location)
  - `language_switch` 언어 전환 (from, to)
  - `social_click` 인스타그램·카카오·유튜브 클릭 (network, link_location)
  - `image_view` 사진 확대 보기 (gallery)
- GA 관리 > 이벤트에서 `consulting_click`을 주요 이벤트로 표시하면 상담 전환을 따로 볼 수 있습니다.

## 운영시간
루비워크샵 쇼룸 운영시간은 모든 브랜드 사이트에서 월~금 12:00~18:00으로 통일합니다.
