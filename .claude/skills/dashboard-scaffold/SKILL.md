---
name: dashboard-scaffold
description: 시트/CSV 데이터를 파이썬으로 계산해 정적 HTML 대시보드 한 장으로 만드는 프로젝트 구조(build.py + metrics/ + template.html)를 만들고, 지표를 파일 하나씩 추가하는 스킬. "대시보드 만들어줘", "지표 추가", "대시보드 구조 잡아줘", "대시보드 인터뷰" 같은 요청에 사용한다.
---

# dashboard-scaffold

규칙은 하나: **지표 하나 = 파일 하나.** 작게 시작하고 필요할 때만 늘린다.

## 구조
```
<프로젝트>/
├─ build.py            # 시트 받기(data/ 캐시) → metrics 실행 → template에 끼워 dist/index.html
├─ template.html       # 화면 전체 (HTML/CSS/JS). Montage 토큰
├─ metrics/
│  ├─ _template.py     # 복사해서 새 지표 시작
│  ├─ _common.py       # 공통 범위와 파생 컬럼 (프로젝트마다 작성)
│  └─ 00_headline.py … # 지표 하나씩
├─ requirements.txt    # pandas
└─ .github/workflows/pages.yml   # 푸시와 매월 1일 빌드·배포
```
`data/`, `dist/`, `.venv/`는 git에서 뺀다.

## 절차
1. **초기화**: 루트에 `build.py`가 없으면 `assets/`의 파일을 같은 경로로 복사한다 (`pages.yml`은 `.github/workflows/`로). 이미 있는 파일은 덮어쓰지 않는다. `build.py` 상단의 `SHEET_ID`, `TABS`(탭 이름: gid)를 프로젝트에 맞게 고친다.
2. **데이터 확인**: 쓸 테이블의 컬럼과 값 범위를 실제로 계산해 본다. 가정한 이야기가 데이터와 다를 수 있다 (예: 소득 격차가 사실은 없었음). 차이가 없는 지표는 넣지 않는다.
3. **인터뷰** (한 번에 2~3개씩): 목적, 화면의 한 가지 질문, 비교 축, 범위(코드, 기간), 금액 지표, 보정 여부, 갱신 주기. 결정 사항은 README에 적는다.
4. **지표 추가**: `metrics/_template.py`를 `metrics/NN_이름.py`로 복사해 `QUESTION`, `CHART`, `SPAN`, `NOTE`, `run(t)`를 채운다. 차트 종류는 headline, range, matrix, bar, monthly, diverge, table. 새 종류가 필요하면 `template.html`의 `R` 객체에 함수를 하나 더한다.
5. **빌드 확인**: `python build.py`로 만들고 브라우저로 `dist/index.html`을 열어 콘솔 에러와 겹침이 없는지 본다.

## 화면 원칙
- **한 가지 질문**: 가장 큰 숫자(`kpi.lead`)가 그 질문에 답한다. 제목 아래 한 줄(`finding`)은 데이터로 계산한 문장이다.
- **제품 표식**: 맨 위에 이름, 담당/범위, 데이터 기준일.
- **정보 밀도**: 모든 값에 n을 붙이고 30건 미만은 "표본 부족"으로 표시한다. 중앙값만이 아니라 25~75% 구간을 함께 보여준다. 차이가 작은 값은 0부터 그린 막대 대신 구간이나 편차(%)로 보여준다.
- 숫자 띠는 타일 여러 장이 아니라 선으로 나뉜 한 칸짜리 컨테이너. 색은 Montage 토큰(파랑 하나)만 쓴다.

## 하지 않는 것
- 프레임워크, 번들러를 넣지 않는다. 차이가 없는 지표로 화면을 채우지 않는다.
- 늘어날 때만 키운다: 지표 10개 초과 → `metrics/` 하위 폴더, 화면 여러 개 → `pages/`, 템플릿 500줄 초과 → `assets/`.
