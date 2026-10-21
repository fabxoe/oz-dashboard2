from _common import resp, TIERS

QUESTION = "소득 5분위별로 상급종합·종합병원을 얼마나 이용하는가?"
CHART = "bar"
NOTE = "외래 호흡기 명세서 중 상급종합·종합병원 비중. 5분위 간 차이는 %p로 본다."


def run(t):
    c = resp(t).dropna(subset=["q"])
    s = c.tier.isin(TIERS[:2]).groupby(c.q).mean() * 100
    n = c.groupby("q").size()
    return {"labels": [f"{q}분위" for q in s.index], "values": [round(float(v), 1) for v in s.values],
            "n": [int(n[q]) for q in s.index], "suffix": "%", "max": 25,
            "caption": f"5분위 − 1분위 = {s.iloc[-1] - s.iloc[0]:+.1f}%p"}
