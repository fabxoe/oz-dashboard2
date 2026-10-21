from _common import resp, TIERS, MIN_N

QUESTION = "한 줄 결론과 핵심 숫자"
CHART = "headline"
DATA_DATE = "2026-10-06"  # 시트 백업 날짜 (시트 첫 줄에 적힌 값)


def _rank_corr(a, b):
    return a.rank().corr(b.rank())


def run(t):
    c = resp(t)
    med = c.groupby("tier").amt.median()
    top, base = med["상급종합병원"], med["의원"]
    cq = c.dropna(subset=["q"]).assign(qn=lambda d: d.q.astype(int))
    q = cq.groupby("q").amt.median()
    rho = [_rank_corr(cq[cq.tier == x].qn, cq[cq.tier == x].amt) for x in TIERS]
    big = max(abs(r) for r in rho)
    text = (f"상급종합병원의 건당 중앙값은 <em>{round(top):,}원</em>으로 의원({round(base):,}원)의 <em>{top / base:.1f}배</em>입니다. "
            f"소득 5분위 간 중앙값은 {round(q.min()):,}~{round(q.max()):,}원이고, 소득과 진료비의 순위상관(−1~1)은 "
            f"모든 종별에서 절댓값 {big:.2f} 이하로 0에 가깝습니다.")
    kpis = [
        {"label": "종별 격차: 상급종합 ÷ 의원", "value": f"{top / base:.1f}배", "note": f"건당 중앙값 {round(top - base):,}원 차이", "lead": True},
        {"label": "건당 중앙값 (전체)", "value": f"{round(c.amt.median()):,}원", "note": "주상병 J00~J99, 외래"},
        {"label": "대상 명세서", "value": f"{len(c):,}건", "note": f"급성 감염 J00~J22 {int(c.acute.sum()):,}건"},
        {"label": "소득 5분위 간 최대 차이", "value": f"{round(q.max() - q.min()):,}원", "note": f"중앙값 대비 {(q.max() - q.min()) / c.amt.median() * 100:.1f}%"},
    ]
    return {"finding": text, "kpis": kpis,
            "period": f"{c.recu_fr_dd.min()} ~ {c.recu_fr_dd.max()}", "stamp": f"{DATA_DATE} 기준"}
