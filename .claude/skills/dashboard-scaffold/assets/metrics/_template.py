"""지표 하나 = 파일 하나. metrics/<번호_이름>.py로 복사해서 쓴다 (_로 시작하는 파일은 건너뜀)."""
QUESTION = "이 지표가 답하는 질문"
CHART = "bar"   # headline | range | matrix | bar | monthly | diverge | table
WIDE = False    # True면 한 줄 전체 폭
NOTE = ""       # 차트 아래 한 줄 설명(한계, 기준)


def run(t):  # t: 테이블 이름 -> DataFrame (모든 컬럼은 글자. 필요하면 직접 숫자로 바꾼다)
    # bar     -> {"labels": [...], "values": [...], "n": [...], "suffix": "%"}
    # range   -> {"labels": [...], "lo": [...], "mid": [...], "hi": [...], "n": [...], "suffix": "원"}
    # table   -> {"columns": [...], "rows": [[...], ...]}
    return {"labels": [], "values": []}
