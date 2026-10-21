from _common import resp, TIERS

QUESTION = "급성 감염과 만성·알레르기 질환의 진료비는 다른가?"
CHART = "table"
SPAN = 5  # 12칸 중 차지하는 칸 수 (6=반, 12=전체)
NOTE = "급성 감염은 J00~J22, 만성·알레르기는 J30~J99."


def run(t):
    c = resp(t)
    rows = []
    for flag, name in ((True, "급성 감염"), (False, "만성·알레르기")):
        d = c[c.acute == flag]
        rows.append([name, f"{len(d):,}", f"{round(d.amt.median()):,}", f"{d.tier.isin(TIERS[:2]).mean() * 100:.1f}%"])
    return {"columns": ["질환군", "명세서 수", "중앙값(원)", "상급·종합 비중"], "rows": rows, "align": [0, 1, 1, 1]}
