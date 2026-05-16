from jwxt_client import JwxtClient

# ========== CLI 使用示例 ==========
if __name__ == "__main__":
    import sys

    client = JwxtClient("laoin", "NB666")

    try:
        client.login()
        print("登录成功！")
    except Exception as e:
        print(f"登录失败: {e}")
        sys.exit(1)

    print("=== 登录成功 ===\n")

    # 成绩查询
    print("--- 2025-2026 第一学期成绩 ---")
    grades = client.get_grades("2025", "3")
    for item in grades.get("items", []):
        print(f"  {item.get('kcmc','')}: {item.get('cj','')} (绩点: {item.get('jd','')}, 学分: {item.get('xf','')})")
    print(f"  共 {grades.get('totalResult', 0)} 门\n")

    # 考试安排
    print("--- 考试安排 ---")
    exams = client.get_exam_arrangement("2025", "12")
    for item in exams.get("items", []):
        print(f"  {item.get('kcmc','')}: {item.get('kssj','')} @ {item.get('cdmc','')}")

    # 通知公告
    print("\n--- 最新通知 ---")
    notifs = client.get_notifications(size=3)
    for item in notifs.get("items", []):
        print(f"  [{item.get('fbsj','')}] {item.get('xwbtqc','')}")

    # 待办事项
    print("\n--- 待办事项 ---")
    todos = client.get_todo_list(size=3)
    for item in todos.get("items", []):
        print(f"  [{item.get('cjsj','')}] {item.get('xxbtjc','')}")