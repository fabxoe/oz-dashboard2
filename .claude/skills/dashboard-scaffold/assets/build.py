"""시트 탭 받기 -> metrics/*.py 실행 -> dist/index.html.  사용법: python build.py [--refresh]"""
import importlib.util, json, pathlib, sys, urllib.request
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "metrics"))  # metrics가 metrics/_common.py를 import할 수 있게 한다
SHEET_ID = "1nPuY8AKFAs2r9da4xUBV3WMKdLEBZJGpmd3kP7xKNvU"
TABS = {"claim": 78768174, "patient": 80354650, "institution": 991582107, "sick_master": 1345263105,
        "code_table": 173633388, "sido_code": 2036727743}  # {"테이블 이름": gid}. 쓰는 탭만 둔다


def fetch(refresh):
    (ROOT / "data").mkdir(exist_ok=True)
    for name, gid in TABS.items():
        f = ROOT / "data" / f"{name}.csv"
        if refresh or not f.exists():
            url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
            f.write_bytes(urllib.request.urlopen(url).read())
            print("받음", name)
    # 앞자리 0 코드(031, 01)가 깨지지 않도록 전부 글자로 읽는다
    return {n: pd.read_csv(ROOT / "data" / f"{n}.csv", dtype=str) for n in TABS}


def run_metrics(tables):
    out = []
    for p in sorted((ROOT / "metrics").rglob("*.py")):
        if p.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(p.stem, p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        out.append({"id": p.stem, "question": m.QUESTION, "chart": m.CHART,
                    "span": getattr(m, "SPAN", 12 if getattr(m, "WIDE", False) else 6), "note": getattr(m, "NOTE", ""), "data": m.run(tables)})
        print("지표", p.stem)
    return out


if __name__ == "__main__":
    metrics = run_metrics(fetch("--refresh" in sys.argv))
    html = (ROOT / "template.html").read_text(encoding="utf-8")
    html = html.replace("/*__METRICS__*/[]", json.dumps(metrics, ensure_ascii=False))
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "index.html").write_text(html, encoding="utf-8")
    print("만듦 dist/index.html")
