# 广西大学教务管理系统 Python SDK

> 正方教务系统 v5 (ZFTAL UI) — 非官方 Python 客户端  
> 覆盖 **53 个 API 端点**，支持成绩、课表、考试、选课、评价、教材、学业预警等全部功能模块

## 快速开始

```python
from python_sdk import JwxtClient, LoginError

client = JwxtClient("学号", "密码")

try:
    client.login()
except LoginError as e:
    print(f"登录失败: {e}")
    exit(1)

# 成绩查询 → 返回 Pydantic 模型
grades = client.grades.query("2025", "3")
for item in grades.items:
    print(f"{item.course_name}: {item.score} (绩点 {item.grade_point})")

# 考试安排
exams = client.exams.query("2025", "12")
for item in exams.items:
    print(f"{item.course_name}: {item.exam_time} @ {item.location}")

# 通知公告
notifs = client.notifications.list()
for item in notifs.items:
    print(f"[{item.publish_date}] {item.title}")

# 待办事项
todos = client.notifications.todos()
for item in todos.items:
    print(f"{item.title}")

# 课表
schedule_html = client.schedule.page()
schedule_data = client.schedule.personal("2025", "12")

# 首页所有区域
areas = client.homepage.all()
user_html = client.homepage.user_info_html()
photo_url = client.homepage.photo_url()

# 系统信息
pending = client.system.pending_student_evaluation()   # 待评价数
warnings = client.system.absentee_warning()            # 旷课预警
client.system.elective_credit_deficiency()             # 学分未修满
```

## 安装

```bash
pip install requests beautifulsoup4 cryptography pydantic
```

Python 版本要求: **3.9+**

## 项目结构

```
教务管理系统爬虫/
├── README.md
├── api.md                     # API 接口文档 (53 个端点详解)
├── test.py                    # 快速测试脚本
├── discover_apis.py           # Playwright API 发现工具
└── python_sdk/                # SDK 源码
    ├── __init__.py            # 公开 API: JwxtClient, LoginError, PageQuery, Semester
    ├── exceptions.py          # LoginError / NotLoggedInError / RequestError
    ├── base.py                # 核心层: HTTP 请求、RSA 加密、登录认证
    ├── jwxt_client.py         # 门面入口，组装所有业务模块
    ├── models/
    │   ├── common.py          # PageQuery(分页) / Semester(学期) / PaginatedResponse
    │   └── data.py            # GradeItem / ExamItem / NotificationItem / TodoItem
    └── modules/               # 业务模块 (10 个)
        ├── grades.py          # 成绩查询
        ├── schedule.py        # 课表查询
        ├── exams.py           # 考试安排
        ├── courses.py         # 选课管理
        ├── notifications.py   # 通知公告 + 待办事项
        ├── academic.py        # 学业情况 + 学籍预警
        ├── homepage.py        # 首页区域 + 用户信息 + 照片
        ├── evaluation.py      # 学生/督导/领导评价
        ├── textbooks.py       # 教材预订/费用/申请
        └── system.py          # 预警/未提交计数/时间状态/监考
```

## 架构设计

```
┌─────────────────────────────────────────────┐
│                 JwxtClient                  │  ← 门面入口
├─────────────────────────────────────────────┤
│  grades │ schedule │ exams │ courses │ ...  │  ← 10 个业务模块
├─────────────────────────────────────────────┤
│                 JwxtBase                    │  ← 核心层
│   HTTP · RSA加密 · 登录 · Session管理      │
├─────────────────────────────────────────────┤
│            Pydantic Models                  │  ← 数据模型层
│   PageQuery · GradeItem · ExamItem · ...    │
└─────────────────────────────────────────────┘
```

- **分层解耦**: base 提供 HTTP/加密/认证，modules 实现业务逻辑，models 定义数据类型
- **组合优于继承**: 业务模块通过组合持有 `JwxtBase` 引用，可独立测试
- **Pydantic 强类型**: 输入参数和返回数据均有模型约束，`model_dump()` 输出英文，`model_dump(by_alias=True)` 兼容原始中文字段

## API 概览

| 模块 | 属性 | 核心方法 |
|------|------|---------|
| 成绩 | `client.grades` | `query(year, term)` `detail(class_id)` `statistics()` |
| 课表 | `client.schedule` | `page()` `personal(year, term)` `classroom()` `teacher()` |
| 考试 | `client.exams` | `query(year, term)` |
| 选课 | `client.courses` | `available(year, term)` `selected(year, term)` |
| 通知 | `client.notifications` | `list()` `detail(news_id)` `todos()` |
| 学业 | `client.academic` | `status()` `warning()` |
| 首页 | `client.homepage` | `all()` `user_info_html()` `photo_url()` `my_apps()` |
| 评价 | `client.evaluation` | `student()` `supervisor()` `leader()` |
| 教材 | `client.textbooks` | `booking()` `fee_confirm()` `plan_apply()` |
| 系统 | `client.system` | `tips()` `absentee_warning()` `pending_*()` 等 26 个方法 |

完整接口文档见 **[api.md](api.md)**。

## 学期编码

| 编码 | 含义 |
|------|------|
| `3` | 第一学期 (9月-次年1月) |
| `12` | 第二学期 (2月-7月) |

学年 `year` 使用起始年份：`"2025"` = 2025-2026 学年。

## 分页查询

```python
from python_sdk import PageQuery

# 自定义分页
q = PageQuery(page=2, page_size=20, sort_order="desc")

# 传给查询方法
grades = client.grades.query("2025", "3", query=q)
notifs = client.notifications.list(query=q)
```

## 异常处理

```python
from python_sdk import LoginError, NotLoggedInError

client = JwxtClient("学号", "密码")

try:
    client.login()
except LoginError as e:
    # 用户名或密码错误、账号锁定等
    print(f"登录失败: {e}")

try:
    grades = client.grades.query("2025", "3")
except NotLoggedInError:
    print("请先登录")
```

## 通用查询

对于未封装的接口，可直接使用通用方法：

```python
# 任意 POST 接口
result = client.query(
    "/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005",
    {"xnm": "2025", "xqm": "3"}
)

# 任意 GET 页面
html = client.query_page("/jwglxt/xtgl/index_cxKczywIndex.html")
```

## 认证机制

系统使用 **RSA 公钥加密** 保护密码：

1. 访问登录页 → 获取 `csrftoken` 和 `JSESSIONID`
2. 请求公钥 `/login_getPublicKey.html` → `{modulus, exponent}`
3. RSA PKCS#1 v1.5 加密密码 → base64 输出
4. 提交登录表单 → 302 重定向到首页
5. 初始化会话 `/index_initMenu.html?jsdm=xs`

SDK 封装了完整流程，调用 `client.login()` 即可。

## 注意事项

- 不要在请求头中声明 `br` (Brotli) 编码，`requests` 库不支持
- 建议在连续请求间添加适当延迟，避免触发频率限制
- 密码仅通过 RSA 加密传输，不会明文发送
- 部分接口（如个人课表）需要先加载对应页面初始化上下文

## 依赖

| 包 | 用途 |
|----|------|
| `requests` | HTTP 客户端 |
| `beautifulsoup4` | HTML 解析 |
| `cryptography` | RSA 公钥加密 |
| `pydantic` | 数据模型与验证 |

## License

本项目仅供学习研究使用。
