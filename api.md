# 广西大学教务管理系统 API 文档

> 教务管理信息服务平台 (正方教务系统 v5 - ZFTAL UI)
> 基础 URL: `https://jwxt2018.gxu.edu.cn`

---

## 目录

1. [认证流程](#1-认证流程)
2. [通用说明](#2-通用说明)
3. [认证接口](#3-认证接口)
4. [成绩查询](#4-成绩查询)
5. [课表查询](#5-课表查询)
6. [考试安排](#6-考试安排)
7. [选课管理](#7-选课管理)
8. [学业情况](#8-学业情况)
9. [培养方案](#9-培养方案)
10. [通知公告](#10-通知公告)
11. [待办事项](#11-待办事项)
12. [首页数据](#12-首页数据)
13. [教材管理](#13-教材管理)
14. [学生评价](#14-学生评价)
15. [学籍预警](#15-学籍预警)
16. [系统信息](#16-系统信息)
17. [辅助接口](#17-辅助接口)

---

## 1. 认证流程

### 1.1 登录加密机制

系统使用 **RSA 公钥加密** 保护密码传输：

```
1. GET  /xtgl/login_slogin.html          → 获取 csrftoken, JSESSIONID
2. GET  /xtgl/login_getPublicKey.html    → 获取 RSA 公钥 {modulus, exponent}
3. RSA 加密密码 (PKCS#1 v1.5 padding, base64 输出)
4. POST /xtgl/login_slogin.html?time=... → 提交登录表单
5. GET  /xtgl/index_initMenu.html?jsdm=xs → 初始化会话
```

### 1.2 加密算法细节

```python
# RSA 公钥参数
modulus  → base64 解码 → 整数 n
exponent → base64 解码 → 整数 e (=65537)

# 加密过程
密文 = RSA_PKCS1v15(UTF8(密码), publicKey(n, e))
输出 = Base64(密文)
```

### 1.3 登录表单参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `csrftoken` | 从登录页获取 | 防 CSRF 攻击 |
| `language` | `zh_CN` | 语言 |
| `yhm` | 学号 | 用户名 |
| `mm` | RSA 加密后的 base64 | 密码 |
| `ydType` | `""` | 用户类型（留空） |

---

## 2. 通用说明

### 2.1 请求头

```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Referer: https://jwxt2018.gxu.edu.cn/jwglxt/xtgl/index_initMenu.html
```

**重要:** 不要使用 `Accept-Encoding: br` (Brotli)，requests 库不支持。

### 2.2 分页查询参数

所有数据查询接口使用统一的分页参数格式：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `_search` | `false` | 是否全文搜索 |
| `nd` | 时间戳 | 随机数 |
| `queryModel.showCount` | `100` | 每页条数 |
| `queryModel.currentPage` | `1` | 当前页码 |
| `queryModel.sortName` | `""` | 排序字段 |
| `queryModel.sortOrder` | `"asc"` | 排序方向 |
| `time` | 时间戳 | 防缓存 |

### 2.3 学期编码

| 编码 | 含义 |
|------|------|
| `3` | 第一学期 (9月-次年1月) |
| `12` | 第二学期 (2月-7月) |

学年 `xnm` 使用起始年份：`'2025'` = 2025-2026学年。

### 2.4 响应格式

数据接口返回标准 JSON：

```json
{
  "currentPage": 1,
  "totalResult": 13,
  "items": [...],
  "queryModel": {...}
}
```

页面接口返回 HTML 片段。

---

## 3. 认证接口

### 3.1 获取登录页面

```
GET /jwglxt/xtgl/login_slogin.html
```

返回: HTML 页面（含 `csrftoken` 隐藏域和 JSESSIONID cookie）

### 3.2 获取 RSA 公钥

```
GET /jwglxt/xtgl/login_getPublicKey.html?time={timestamp}
```

响应:
```json
{
  "modulus": "ALzoeF/2QxH1tbSBIxV+80A9...",
  "exponent": "AQAB"
}
```

### 3.3 登录

```
POST /jwglxt/xtgl/login_slogin.html?time={timestamp}
Content-Type: application/x-www-form-urlencoded

csrftoken={token}&language=zh_CN&yhm={学号}&mm={加密密码}&ydType=
```

返回: 302 重定向到首页

### 3.4 退出登录

```
GET /jwglxt/xtgl/login_logoutAccount.html
```

---

## 4. 成绩查询

### 4.1 查询学期成绩

```
POST /jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005
Content-Type: application/x-www-form-urlencoded

xnm={学年}&xqm={学期}&_search=false&nd={ts}&queryModel.showCount=100&...
```

**请求参数:**

| 参数 | 必填 | 说明 |
|------|------|------|
| `xnm` | 是 | 学年，如 `'2025'` |
| `xqm` | 是 | 学期，`'3'` 或 `'12'` |

**响应关键字段:**

| 字段 | 说明 |
|------|------|
| `items[].kcmc` | 课程名称 |
| `items[].cj` | 成绩（数字字符串） |
| `items[].jd` | 绩点 |
| `items[].xf` | 学分 |
| `items[].kcbj` | 课程标记（必修/选修等） |
| `items[].kkxy` | 开课学院 |
| `items[].kssj` | 考试时间 |
| `items[].cjbdsj` | 成绩绑定时间 |
| `items[].kch` | 课程号 |
| `items[].jxb_id` | 教学班ID |

**示例响应:**
```json
{
  "currentPage": 1,
  "totalResult": 13,
  "items": [
    {
      "kcmc": "数据结构",
      "cj": "71",
      "jd": "2.10",
      "xf": "4.5",
      "kcbj": "专业选修课",
      "kch": "1123456"
    }
  ]
}
```

### 4.2 查询分项成绩

```
POST /jwglxt/cjcx/cjcx_cxDgXscj.html?doType=details&gnmkdm=N305005

jxb_id={教学班ID}&xh={学号}
```

### 4.3 成绩统计

```
GET /jwglxt/cjcx/cjcx_cxDgXscj.html?doType=statistics&gnmkdm=N305005&time={ts}
```

返回总学分、平均绩点等统计数据。

---

## 5. 课表查询

### 5.1 课表首页

```
GET /jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default&time={ts}
```

返回: 课表页面 HTML（含课表数据嵌入）

### 5.2 个人课表数据

```
POST /jwglxt/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151

xnm={学年}&xqm={学期}
```

### 5.3 教室课表

```
POST /jwglxt/kbcx/jskbcx_cxJskb.html?gnmkdm=N2151

xnm={学年}&xqm={学期}&jsmc={教室名称}
```

### 5.4 教师课表

```
POST /jwglxt/kbcx/jskbcx_cxJsKb.html?gnmkdm=N2151

xnm={学年}&xqm={学期}&jsmc={教师名称}
```

### 5.5 课表/学分确认

```
GET /jwglxt/kbcx/xskbqr_cxXskbqrIndex.html?gnmkdm=N2158&time={ts}
```

---

## 6. 考试安排

### 6.1 查询考试安排

```
POST /jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N3580

xnm={学年}&xqm={学期}
```

**响应关键字段:**

| 字段 | 说明 |
|------|------|
| `items[].kcmc` | 课程名称 |
| `items[].kssj` | 考试时间 |
| `items[].cdmc` | 考场地点 |
| `items[].ksmc` | 考试名称 |
| `items[].khfs` | 考核方式 |
| `items[].cdbh` | 考场编号 |

**示例响应:**
```json
{
  "items": [
    {
      "kcmc": "毛泽东思想和中国特色社会主义理论体系概论",
      "kssj": "2026-06-09(15:00-17:00)",
      "cdmc": "6A-405",
      "khfs": "集中",
      "ksmc": "2025-2026学年第二学期本科课程期末考试"
    }
  ]
}
```

### 6.2 考试监考信息

```
GET /jwglxt/jkap/ksjkxxcx_cxKsjkxxcxIndex.html?gnmkdm=N353088&time={ts}
```

---

## 7. 选课管理

### 7.1 查询可选课程

```
POST /jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?doType=query&gnmkdm=N253512

xnm={学年}&xqm={学期}&kcmc={课程名(可选)}
```

### 7.2 已选课程

```
POST /jwglxt/xsxk/zzxkyzb_cxZzxkYzb.html?gnmkdm=N253512

xnm={学年}&xqm={学期}
```

---

## 8. 学业情况

```
GET /jwglxt/xsxy/xsxyqk_cxXsxyqkIndex.html?gnmkdm=N105515&time={ts}
```

返回学生学业完成情况（已修学分、培养方案进度等）。

---

## 9. 培养方案

```
GET /jwglxt/pyfa/pyfagl_cxXsPyfaIndex.html?gnmkdm=N2580&time={ts}
```

返回学生培养方案页面。

---

## 10. 通知公告

### 10.1 通知列表

```
POST /jwglxt/xtgl/xwck_cxMoreXwList.html?doType=query

_search=false&nd={ts}&queryModel.showCount=15&queryModel.currentPage=1&queryModel.sortName=+&queryModel.sortOrder=desc&time=0
```

**响应关键字段:**

| 字段 | 说明 |
|------|------|
| `items[].xwbtqc` | 通知标题（全称） |
| `items[].xwbt` | 通知标题（可能截断） |
| `items[].fbsj` | 发布时间 |
| `items[].xwbh` | 新闻编号（用于获取详情） |
| `items[].fbrxm` | 发布人姓名 |
| `items[].sfzd` | 是否置顶 |

### 10.2 通知详情

```
GET /jwglxt/xtgl/xwck_ckXw.html?xwbh={新闻编号}&doType=save
```

返回: 通知详情 HTML 页面。

---

## 11. 待办事项

```
POST /jwglxt/xtgl/index_cxDbsy.html?doType=query

flag=1&sfyy=1&_search=false&nd={ts}&queryModel.showCount=15&queryModel.currentPage=1&queryModel.sortName=cjsj+&queryModel.sortOrder=desc&time=0
```

**响应关键字段:**

| 字段 | 说明 |
|------|------|
| `items[].xxbt` | 事项标题 |
| `items[].xxnr` | 事项内容 |
| `items[].cjsj` | 创建时间 |
| `items[].clzt` | 处理状态 (0=未处理) |

---

## 12. 首页数据

以下接口返回首页各区域的 HTML 片段，采用 POST 方式调用：

### 12.1 首页区域列表

| 区域 | 接口 | 说明 |
|------|------|------|
| 课表 | `POST /xtgl/index_cxAreaOne.html?localeKey=zh_CN&gnmkdm=index` | 本周课表 |
| 文件 | `POST /xtgl/index_cxAreaTwo.html?localeKey=zh_CN&gnmkdm=index` | 文件下载 |
| 消息 | `POST /xtgl/index_cxAreaThree.html?localeKey=zh_CN&gnmkdm=index` | 系统消息 |
| 成绩/考试 | `POST /xtgl/index_cxAreaFour.html?localeKey=zh_CN&gnmkdm=index` | 成绩考试tab |
| 校历 | `POST /xtgl/index_cxAreaFive.html?localeKey=zh_CN&gnmkdm=index` | 校历 |
| 校历文件 | `POST /xtgl/index_cxAreaSix.html?localeKey=zh_CN&gnmkdm=index` | 校历和文件 |
| 通知 | `POST /xtgl/index_cxNews.html?localeKey=zh_CN&gnmkdm=index` | 通知公告 |

### 12.2 我的应用

```
POST /jwglxt/xtgl/index_cxWdyy.html?localeKey=zh_CN&gnmkdm=index&time={ts}
```

### 12.3 最近使用

```
POST /jwglxt/xtgl/index_cxZjsy.html?localeKey=zh_CN&gnmkdm=index&time={ts}
```

### 12.4 用户信息

```
POST /jwglxt/xtgl/index_cxYhxxIndex.html?xt=jw&localeKey=zh_CN&_={ts}&gnmkdm=index
```

返回: HTML 片段（含姓名、学号、院系、照片 `<img>` 标签）

### 12.5 照片

```
GET /jwglxt/xtgl/photo_cxXszp4.html?xh_id={学号}&zplx=rxqzp
```

---

## 13. 教材管理

### 13.1 教材预订

```
GET /jwglxt/jcydgl/xsjcyd_cxXsjcydIndex.html?gnmkdm=N253545&time={ts}
```

### 13.2 教材费用确认

```
GET /jwglxt/jcjsgl/xsjs_cxJcfyqrIndex.html?gnmkdm=N758066&time={ts}
```

---

## 14. 学生评价

```
GET /jwglxt/xspjgl/xspj_cxXspjIndex.html?gnmkdm=N401605&time={ts}
```

---

## 15. 学籍预警

```
GET /jwglxt/xjyj/xjyj_cxXjyjIndex.html?gnmkdm=N105505&time={ts}
```

---

## 16. 系统信息

### 16.1 系统提示

```
POST /jwglxt/xtgl/index_cxXttsxx.html?bj=2
```

返回选课毕业学分提示等系统消息。

### 16.2 旷课预警

```
POST /jwglxt/xtgl/index_cxKkyjxx.html
```

### 16.3 学业预警

```
GET /jwglxt/xtgl/index_cxXsxyyjtxIndex.html
POST /jwglxt/xtgl/index_cxXsxyyjtxView.html
```

### 16.4 其他系统接口

| 接口 | 说明 |
|------|------|
| `POST /xtgl/index_cxJhkcjcsqWtjNum.html` | 教材申请未提交数量 |
| `POST /xtgl/index_cxXsGxkxfwxm.html` | 公选课学分未修满 |
| `POST /xtgl/index_cxXspjWtjNum.html` | 学生评价未提交数 |
| `POST /xtgl/index_cxFxjftsNum.html` | 辅修缴费提醒 |
| `POST /xtgl/index_cxBsxtsj.html` | 毕设选题时间 |
| `POST /xtgl/index_cxXfqrsj.html` | 学分确认时间 |
| `POST /xtgl/index_cxLyyjxx.html` | 劳育预警 |
| `POST /xtgl/index_cxThpjWtjNum.html` | 同行评价未提交数 |
| `POST /xtgl/index_cxDdpjWtjNum.html` | 督导评价未提交数 |
| `POST /xtgl/index_cxLdpjWtjNum.html` | 领导评价未提交数 |
| `POST /xtgl/index_cxXxdlztgx.html` | 信息已读状态更新 |

---

## 17. 辅助接口

### 17.1 获取菜单结构

菜单内嵌在首页 HTML 中，通过解析 `index_initMenu.html` 获取。

### 17.2 功能模块编码 (gnmkdm) 对照表

| 编码 | 功能模块 |
|------|---------|
| `N305005` | 学生成绩查询 |
| `N2151` | 学生课表查询 |
| `N2158` | 课表/学分确认 |
| `N3580` | 考试信息查询 |
| `N253512` | 自主选课 |
| `N105515` | 学生学业情况 |
| `N105505` | 学籍预警 |
| `N2580` | 培养方案管理 |
| `N401605` | 学生评价 |
| `N253545` | 教材预订 |
| `N758066` | 教材费用确认 |
| `N353088` | 考试监考信息 |

---

## SDK 快速入门 (Python)

```python
from jwxt_client import JwxtClient

# 初始化并登录
client = JwxtClient("学号", "密码")
client.login()

# 查询成绩
grades = client.get_grades("2025", "3")  # 2025-2026 第一学期
for item in grades["items"]:
    print(f"{item['kcmc']}: {item['cj']} (绩点 {item['jd']})")

# 查询考试安排
exams = client.get_exam_arrangement("2025", "12")
for item in exams.get("items", []):
    print(f"{item['kcmc']}: {item['kssj']} @ {item['cdmc']}")

# 查询通知
notifs = client.get_notifications(page=1, size=10)
for item in notifs["items"]:
    print(f"[{item['fbsj']}] {item['xwbtqc']}")

# 查询待办事项
todos = client.get_todo_list()
for item in todos["items"]:
    print(f"{item['xxbt']}")

# 查询课表
schedule_html = client.get_schedule_page()
schedule_data = client.get_schedule_data("2025", "12")

# 通用查询
result = client.query(
    "/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005",
    {"xnm": "2025", "xqm": "3"}
)
```

---

## 依赖

```bash
pip install requests beautifulsoup4 cryptography
```

## 注意事项

1. 密码通过 RSA 公钥加密传输，不会以明文发送
2. 所有请求需要携带登录后获取的 JSESSIONID cookie
3. CSRF token 从登录页面获取，提交登录时需携带
4. 服务器可能间歇性返回 Brotli 压缩的内容，建议不从客户端声明支持 `br` 编码
5. 建议在请求间添加适当延迟，避免触发频率限制
