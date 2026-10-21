from _common import resp, TIERS

QUESTION = "연령대를 맞춰도 종별 격차가 그대로인가?"
CHART = "table"
WIDE = True
NOTE = "연령대별 종별 건당 중앙값(원). 환자 구성 차이가 격차의 원인인지 확인한다."


def run(t):
    c = resp(t)
    p = c.pivot_table(index="ageband", columns="tier", values="amt", aggfunc="median", observed=True)[TIERS]
    n = c.groupby("ageband", observed=True).size()
    rows = [[str(a), f"{int(n[a]):,}"] + [f"{round(p.loc[a, x]):,}" for x in TIERS] + [f"{p.loc[a, TIERS[0]] / p.loc[a, TIERS[3]]:.1f}배"] for a in p.index]
    return {"columns": ["연령대", "명세서 수"] + TIERS + ["상급종합÷의원"], "rows": rows, "align": [0, 1, 1, 1, 1, 1, 1]}
