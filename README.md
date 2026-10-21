# 대시보드 프로젝트

## 규칙

- 폴더 하나 = 대시보드 하나. `dashboards/<이름>/`에 `index.html`, `main.js`, `README.md` 세 개를 둔다.
- 새 대시보드는 `dashboards/_template/`을 복사해서 시작한다.
- 데이터는 `data/`에 CSV로 둔다 (테이블당 1파일).
- 공통 코드는 두 군데 이상에서 반복될 때만 `shared/`로 옮긴다.
- 빌드 도구 없음. 로컬 확인: `python3 -m http.server` 후 브라우저로 열기.

## 대시보드

(목록은 `index.html`)

## 디자인 시스템

색, 반경, 글꼴은 Wanted의 [Montage](https://github.com/wanteddev/montage-web)(MIT) 토큰을 따른다. 글꼴은 Wanted Sans(jsDelivr), 없으면 Noto Sans KR. 토큰은 `shared/style.css` 맨 위 `:root`에 모여 있다.
