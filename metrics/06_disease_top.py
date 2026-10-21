from _common import resp, TIERS

QUESTION = "어떤 호흡기 질환이 많고, 진료비는 전체 대비 어떤가?"
CHART = "table"
SPAN = 7  # 12칸 중 차지하는 칸 수 (6=반, 12=전체)
NOTE = "주상병 3자리 코드 상위 10개. 전체 대비는 건당 중앙값이 전체 중앙값보다 몇 % 높고 낮은지."


def run(t):
    c = resp(t).assign(code=lambda d: d.main_sick.str[:3])
    names = t["sick_master"].drop_duplicates("sickcd").set_index("sickcd").krnm
    all_med = c.amt.median()
    g = c.groupby("code").agg(n=("amt", "size"), med=("amt", "median"),
                              top=("tier", lambda s: (s == TIERS[0]).mean())).sort_values("n", ascending=False).head(10)
    rows = [[k, names.get(k, ""), f"{int(r.n):,}", f"{round(r.med):,}", f"{(r.med / all_med - 1) * 100:+.0f}%", f"{r.top * 100:.1f}%"]
            for k, r in g.iterrows()]
    return {"columns": ["코드", "상병명", "명세서 수", "중앙값(원)", "전체 대비", "상급종합 비중"], "rows": rows,
            "align": [0, 0, 1, 1, 1, 1]}
