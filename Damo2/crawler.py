from bs4 import BeautifulSoup

def fetch_courses(session, base_url, term=None):
    """
    term: 若平台课程页支持学期参数，传入如 "2025-2026-1"；
          若不支持，传 None，后续从课程介绍中提取。
    """
    url = f"{base_url}/student/course"  # 根据实际路径修改
    params = {"term": term} if term else {}

    r = session.get(url, params=params, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    courses = []
    # 根据实际表格的 CSS 选择器修改，常见为 table 或 .course-list
    table = soup.find("table")
    if not table:
        print("[!] 未找到课程表格，检查页面路径或选择器")
        return courses

    rows = table.find_all("tr")
    header = [th.get_text(" ", strip=True) for th in rows[0].find_all(["th", "td"])]
    print(f"[+] 表头：{header}")  # 打印表头，方便对照字段

    for tr in rows[1:]:
        tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        if len(tds) < 3:
            continue

        # 根据表头顺序映射字段，替换为你学校实际的列顺序
        courses.append({
            "code": tds[0] if len(tds) > 0 else "",
            "name": tds[1] if len(tds) > 1 else "",
            "teacher": tds[2] if len(tds) > 2 else "",
            "credits": tds[3] if len(tds) > 3 else "",
            "intro": tds[-1] if len(tds) > 4 else "",
        })

    print(f"[+] 共抓取 {len(courses)} 条课程记录")
    return courses