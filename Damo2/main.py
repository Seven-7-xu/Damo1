# main.py
import json
from login import create_session, login, BASE
from crawler import fetch_courses
from term_utils import group_by_term

def main():
    session = create_session()
    login(session)

    # 若平台支持学期参数，可循环传入；否则先抓取全部，靠介绍文本分组
    courses = fetch_courses(session, BASE)

    # 根据你的入学年份修改，用于“第X学期”映射
    ENROLL_YEAR = 2025
    groups = group_by_term(courses, enroll_year=ENROLL_YEAR)

    with open("output/courses_by_term.json", "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)

    for term, items in groups.items():
        print(f"{term}: {len(items)} 门课")

if __name__ == "__main__":
    main()