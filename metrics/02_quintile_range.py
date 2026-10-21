from _common import resp

QUESTION = "소득 5분위가 높을수록 건당 진료비가 다른가?"
CHART = "range"
NOTE = "1분위가 가장 낮은 소득. 점은 중앙값, 막대는 25~75% 구간."


def run(t):
    c = resp(t).dropna(subset=["q"])
    g = c.groupby("q").amt
    qs = sorted(c.q.unique())
    return {"labels": [f"{q}분위" for q in qs], "mid": [round(float(g.median()[q])) for q in qs],
            "lo": [round(float(g.quantile(.25)[q])) for q in qs], "hi": [round(float(g.quantile(.75)[q])) for q in qs],
            "n": [int(g.size()[q]) for q in qs], "suffix": "원", "zero": True}
