# term_utils.py
import re

def extract_term(text, enroll_year=None):
    """
    从课程介绍或课程名中提取学期标签。
    enroll_year: 入学年份，用于将“第X学期”映射为具体学年，如 2024。
    """
    text = text.replace(" ", "").replace("　", "")

    # 模式1：2025-2026学年第一学期 / 2025-2026-1
    m = re.search(r"(20\d{2})[-—](20\d{2})学年(第一|第二|1|2)学期", text)
    if m:
        y1, y2, t = m.groups()
        t = {"第一": "1", "第二": "2", "1": "1", "2": "2"}.get(t, "1")
        return f"{y1}-{y2}-{t}"

    # 模式2：2025年秋季 / 2025年春季
    m = re.search(r"(20\d{2})年(春|秋)季", text)
    if m:
        y = int(m.group(1))
        s = m.group(2)
        if s == "秋":
            return f"{y}-{y+1}-1"
        return f"{y-1}-{y}-2"

    # 模式3：第X学期（需结合入学年份）
    m = re.search(r"第(\d+)学期", text)
    if m and enroll_year:
        seq = int(m.group(1))
        offset = (seq - 1) // 2
        half = 1 if seq % 2 == 1 else 2
        y1 = enroll_year + offset
        return f"{y1}-{y1+1}-{half}"

    return None

def group_by_term(courses, enroll_year=None):
    groups = {}
    for c in courses:
        term = extract_term(c.get("intro", "") + c.get("name", ""), enroll_year)
        term = term or "未知学期"
        groups.setdefault(term, []).append(c)
    # 按学期排序
    sorted_groups = dict(sorted(groups.items()))
    return sorted_groups