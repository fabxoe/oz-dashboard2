from _common import resp

QUESTION = "월별로 진료 건수와 진료비는 어떻게 움직이는가?"
CHART = "monthly"
WIDE = True
NOTE = "진료 시작일 기준. 건수는 겨울에 늘고 건당 중앙값은 거의 변하지 않는다."


def run(t):
    g = resp(t).groupby("month").amt
    return {"labels": list(g.size().index), "count": [int(v) for v in g.size().values],
            "median": [round(float(v)) for v in g.median().values]}
