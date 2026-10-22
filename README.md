# Tsubasa Bicycles Korea

tsubasabicycles.co.kr 원페이지 정적 사이트 (GitHub Pages).

- `index.html` 원페이지 본체 (ORIGIN · CROW · PROCESS · ARTWORK · CONCEPT)
- `404.html` 기존 아임웹 하위 주소(/crow 등)를 섹션으로 연결
- `images/` 섹션별 이미지 (`hero`, `origin`, `crow`, `process`, `artwork`, `concept`)
- `.github/image-manifest.txt` + `fetch-images.yml` 아임웹 CDN 이미지 이전용 워크플로

## 구글 애널리틱스 (GA4)
루비컴퍼니 브랜드 사이트(츠바사·바스티온·팔리·크러스트) 공통 코드입니다.

- 측정 ID는 `index.html` 맨 위의 `var GA_ID = '';` 한 곳에 넣습니다. 비어 있으면 GA를 불러오지 않습니다.
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
