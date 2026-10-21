from _common import resp, TIERS

QUESTION = "종별로 건당 진료비는 얼마나 다른가?"
CHART = "range"
WIDE = True
NOTE = "점은 중앙값, 막대는 25~75% 구간, n은 명세서 수."


def run(t):
    c = resp(t)
    g = c.groupby("tier").amt
    return {"labels": TIERS, "mid": [round(float(g.median()[x])) for x in TIERS],
            "lo": [round(float(g.quantile(.25)[x])) for x in TIERS],
            "hi": [round(float(g.quantile(.75)[x])) for x in TIERS],
            "n": [int(g.size()[x]) for x in TIERS], "suffix": "원", "zero": True}
