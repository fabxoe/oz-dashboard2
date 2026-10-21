"""호흡기 지표 공통 범위: 외래(031) 명세서 중 주상병이 J코드인 것."""
import pandas as pd

TIERS = ["상급종합병원", "종합병원", "병원", "의원"]
MIN_N = 30  # 이보다 적은 칸은 "표본 부족"으로 표시한다
_cache = {}


def resp(t):
    if id(t) not in _cache:
        c = t["claim"]
        c = c[c.main_sick.str.startswith("J") & (c.fom_tp_cd == "031")].copy()
        c["amt"] = pd.to_numeric(c.rvd_rpe_tamt_amt)
        c["self_amt"] = pd.to_numeric(c.rvd_slf_brdn_amt)
        c["days"] = pd.to_numeric(c.vst_ddcnt).clip(lower=1)
        c = c.merge(t["institution"][["yid", "cl_cd"]], on="yid")
        c = c.merge(t["patient"][["jid", "sido_cd", "prem_quintile", "birth_yr"]], on="jid")
        names = t["code_table"][t["code_table"].code_type == "종별코드"].set_index("code").code_nm
        c["tier"] = c.cl_cd.map(names)
        c["acute"] = c.main_sick.str[1:3].astype(int) <= 22
        c["month"] = c.recu_fr_dd.str[:7]
        c["age"] = c.recu_fr_dd.str[:4].astype(int) - pd.to_numeric(c.birth_yr)
        c["ageband"] = pd.cut(c.age, [-1, 9, 19, 39, 64, 200], labels=["0~9세", "10~19세", "20~39세", "40~64세", "65세 이상"])
        c["q"] = c.prem_quintile
        _cache[id(t)] = c
    return _cache[id(t)]
