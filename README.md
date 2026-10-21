# 호흡기 진료비 격차 대시보드

시트 데이터를 받아 파이썬으로 계산하고, 정적 HTML 한 장으로 만든다. `python build.py [--refresh]` → `dist/index.html`.

## 구조
- `build.py`: 시트 탭을 `data/`에 받고(캐시) → `metrics/` 실행 → `template.html`에 끼워 `dist/`에 쓴다. 시트 ID와 탭 gid는 맨 위 상수.
- `metrics/`: 지표 하나 = 파일 하나. `_template.py`를 복사해서 `QUESTION`, `CHART`, `run(t)`를 채운다. `_common.py`가 공통 범위(외래, 주상병 J)와 파생 컬럼을 만든다.
- `template.html`: 화면 전체(HTML, CSS, JS). 차트 종류: headline, range, matrix, bar, monthly, diverge, table.
- `data/`, `dist/`, `.venv/`는 생성물이라 git에서 뺀다.

## 규칙
- 지표를 더하려면 `metrics/`에 파일 하나만 더한다. `SPAN`(12칸 중 차지하는 칸)으로 폭을 정한다.
- CSV는 전부 글자로 읽고(`dtype=str`) 필요한 컬럼만 숫자로 바꾼다. 앞자리 0 코드가 깨지지 않게.
- 모든 값에 n을 함께 보여주고, 30건 미만은 "표본 부족"으로 표시한다.
- 늘어날 때만 키운다: 지표 10개 초과 → `metrics/` 하위 폴더, 화면 여러 개 → `pages/`, 템플릿 500줄 초과 → `assets/`.

## 실행
```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build.py --refresh
```
배포는 `.github/workflows/pages.yml`이 푸시와 매월 1일에 빌드해서 GitHub Pages에 올린다. 시트 CSV는 빌드 중에만 받고 저장소에는 올리지 않는다.

## 디자인
색, 반경, 글꼴은 Wanted의 [Montage](https://github.com/wanteddev/montage-web)(MIT) 토큰을 따른다. 글꼴은 Wanted Sans, 없으면 시스템 한글 글꼴. 토큰은 `template.html` 맨 위 `:root`.

## 결정 사항 (사용자 확인)
- 비교 축: 종별(claim→institution.cl_cd), 소득 5분위(patient.prem_quintile), 시도.
- 범위: 외래(fom_tp_cd=031), 주상병 J00~J99. J00~J22는 급성 감염으로 따로 보여준다.
- 금액: 건당 총진료비(rvd_rpe_tamt_amt)의 중앙값과 분위수.
- 보정: 먼저 단순 비교, 연령대 층화 확인표만. 서술은 실태 제시이고 인과를 주장하지 않는다.
- 주기: 월 단위 갱신.

## 데이터 메모
- 실습 데이터(OZ 코딩 SQL 3기), 2024-01~2025-12. 기관 이름은 없고 종별과 권역만 있다.
- 소득 5분위는 건당 중앙값이 거의 같다(18,050~18,500원). 종별 격차(상급종합 ÷ 의원 약 3.0배)가 큰 축이다.
- 본인부담률(약 26%)과 내원일당 진료비는 종별 간 차이가 없거나 건당과 같아서 지표에서 뺐다.
- 기관 단위 분석은 표본 30건 이상인 기관이 약 102곳뿐이라 얇다.
