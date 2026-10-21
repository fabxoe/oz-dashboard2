# 대시보드 프로젝트

## 규칙

- 폴더 하나 = 대시보드 하나. `dashboards/<이름>/`에 `index.html`, `main.js`, `README.md` 세 개를 둔다.
- 새 대시보드는 `dashboards/_template/`을 복사해서 시작한다.
- 데이터는 `data/`에 CSV로 둔다 (테이블당 1파일).
- 공통 코드는 두 군데 이상에서 반복될 때만 `shared/`로 옮긴다.
- 빌드 도구 없음. 로컬 확인: `python3 -m http.server` 후 브라우저로 열기.

## 대시보드

(목록은 `index.html`)
