from _common import resp, TIERS, MIN_N

QUESTION = "같은 종별 안에서도 소득에 따라 진료비가 다른가?"
CHART = "matrix"
WIDE = True
NOTE = f"칸의 숫자는 건당 중앙값(원), 아래는 명세서 수. {MIN_N}건 미만은 표본 부족(빗금)."


def run(t):
    c = resp(t).dropna(subset=["q"])
    qs = sorted(c.q.unique())
    cells = []
    for tier in TIERS:
        row = []
        for q in qs:
            a = c[(c.tier == tier) & (c.q == q)].amt
            row.append({"v": round(float(a.median())) if len(a) else None, "n": int(len(a)), "low": len(a) < MIN_N})
        cells.append(row)
    return {"rows": TIERS, "cols": [f"{q}분위" for q in qs], "cells": cells, "suffix": "원"}
