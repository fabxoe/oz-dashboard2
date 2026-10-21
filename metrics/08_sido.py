from _common import resp, MIN_N

QUESTION = "환자 거주 시도별로 건당 진료비는 얼마나 다른가?"
CHART = "diverge"
WIDE = True
NOTE = f"전국 중앙값 대비 편차(%). 환자 거주 시도 기준. 명세서 {MIN_N}건 미만은 표시하지 않는다."


def run(t):
    c = resp(t).merge(t["sido_code"][["sido_cd", "sido_nm"]], on="sido_cd")
    nat = c.amt.median()
    g = c.groupby("sido_nm").amt.agg(n="size", med="median")
    g = g[g.n >= MIN_N].sort_values("med", ascending=False)
    return {"labels": list(g.index), "values": [round(float((m / nat - 1) * 100), 1) for m in g.med],
            "mid": [round(float(m)) for m in g.med], "n": [int(n) for n in g.n], "ref": round(float(nat))}
