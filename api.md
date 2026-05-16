# 广西大学教务管理系统 API 文档

> 教务管理信息服务平台 (正方教务系统 v5 - ZFTAL UI)
> 基础 URL: `https://jwxt2018.gxu.edu.cn`
> 总计: 6 个 JSON 数据接口 + 23 个 HTML 页面接口 = **29 个可用端点**

---

## 目录

1. [认证流程](#1-认证流程)
2. [通用说明](#2-通用说明)
3. [成绩查询](#3-成绩查询)
4. [课表查询](#4-课表查询)
5. [考试安排](#5-考试安排)
6. [选课管理](#6-选课管理)
7. [学业与预警](#7-学业与预警)
8. [通知公告](#8-通知公告)
9. [待办事项](#9-待办事项)
10. [首页数据](#10-首页数据)
11. [教材管理](#11-教材管理)
12. [学生评价](#12-学生评价)
13. [系统信息](#13-系统信息)
14. [端点汇总表](#14-端点汇总表)
15. [SDK 快速入门](#15-sdk-快速入门)

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

### 1.2 加密算法

```python
modulus  → base64 解码 → 整数 n
exponent → base64 解码 → 整数 e (=65537)
密文 = RSA_PKCS1v15(UTF8(密码), publicKey(n, e))
输出 = Base64(密文)
```

### 1.3 接口列表

| 接口 | 方法 | 说明 |
|------|------|------|
| `/xtgl/login_slogin.html` | GET | 登录页面，获取 csrftoken 和 JSESSIONID |
| `/xtgl/login_getPublicKey.html?time={ts}` | GET | 获取 RSA 公钥 `{modulus, exponent}` |
| `/xtgl/login_slogin.html?time={ts}` | POST | 提交登录表单 (csrftoken, yhm, mm, language, ydType) |
| `/xtgl/login_logoutAccount.html` | GET | 退出登录 |

### 1.4 登录表单参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `csrftoken` | 从登录页获取 | 防 CSRF |
| `language` | `zh_CN` | 语言 |
| `yhm` | 学号 | 用户名 |
| `mm` | RSA 加密的 base64 | 密码 |
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

**重要:** 不要声明 `Accept-Encoding: br`，requests 库不支持 Brotli 解压。

### 2.2 分页查询参数

所有数据查询接口使用统一格式：

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

- **JSON 接口**: `{"currentPage":1, "totalResult":N, "items":[...], "queryModel":{...}}`
- **HTML 接口**: 返回页面 HTML 片段，数据嵌入在 DOM 中

---

## 3. 成绩查询

### 3.1 学期成绩 (JSON)

```
POST /jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005
Content-Type: application/x-www-form-urlencoded

xnm={学年}&xqm={学期}&_search=false&nd={ts}&queryModel.showCount=100&...
```

**响应字段:**

| 字段 | 说明 |
|------|------|
| `items[].kcmc` | 课程名称 |
| `items[].cj` | 成绩 (数字字符串) |
| `items[].jd` | 绩点 |
| `items[].xf` | 学分 |
| `items[].kcbj` | 课程标记 (必修/选修) |
| `items[].kkxy` | 开课学院 |
| `items[].kch` | 课程号 |
| `items[].jxb_id` | 教学班ID |
| `items[].cjbdsj` | 成绩录入时间 |
| `items[].bfzcj` | 百分制成绩 |
| `items[].cjsfzf` | 是否重修 |

### 3.2 成绩详情 (HTML)

```
POST /jwglxt/cjcx/cjcx_cxDgXscj.html?doType=details&gnmkdm=N305005

jxb_id={教学班ID}&xh={学号}
```

返回课程分项成绩 HTML 页面。

### 3.3 成绩统计 (HTML)

```
GET /jwglxt/cjcx/cjcx_cxDgXscj.html?doType=statistics&gnmkdm=N305005&time={ts}
```

返回总学分、平均绩点等统计 HTML 页面。

---

## 4. 课表查询

### 4.1 课表首页 (HTML)

```
GET /jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default&time={ts}
```

返回课表页面 HTML（含本学期课表数据）。

### 4.2 个人课表 (JSON)

```
POST /jwglxt/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151

xnm={学年}&xqm={学期}
```

返回学生个人课表数据，需先加载课表首页初始化上下文。

### 4.3 教室课表 (HTML)

```
POST /jwglxt/kbcx/jskbcx_cxJskb.html?gnmkdm=N2151

xnm={学年}&xqm={学期}&jsmc={教室名称}
```

### 4.4 教师课表 (JSON)

```
POST /jwglxt/kbcx/jskbcx_cxJsKb.html?gnmkdm=N2151

xnm={学年}&xqm={学期}&jsmc={教师名称}
```

### 4.5 班级课表 (HTML)

```
POST /jwglxt/kbcx/xskbcx_cxBjKb.html?gnmkdm=N253501

xnm={学年}&xqm={学期}
```

### 4.6 学分确认 (HTML)

```
POST /jwglxt/kbcx/xskbqr_cxXskbqr.html?gnmkdm=N2158
GET  /jwglxt/kbcx/xskbqr_cxXskbqrIndex.html?gnmkdm=N2158&time={ts}
```

---

## 5. 考试安排

### 5.1 考试安排 (JSON)

```
POST /jwglxt/kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N3580

xnm={学年}&xqm={学期}
```

**响应字段:**

| 字段 | 说明 |
|------|------|
| `items[].kcmc` | 课程名称 |
| `items[].kssj` | 考试时间 |
| `items[].cdmc` | 考场地点 |
| `items[].cdbh` | 考场编号 |
| `items[].ksmc` | 考试名称 |
| `items[].khfs` | 考核方式 |

### 5.2 考试监考信息 (HTML)

```
GET /jwglxt/jkap/ksjkxxcx_cxKsjkxxcxIndex.html?gnmkdm=N353088&time={ts}
```

---

## 6. 选课管理

### 6.1 可选课程 (HTML)

```
POST /jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?doType=query&gnmkdm=N253512

xnm={学年}&xqm={学期}&kcmc={课程名(可选)}
```

### 6.2 已选课程 (HTML)

```
POST /jwglxt/xsxk/zzxkyzb_cxZzxkYzb.html?gnmkdm=N253512

xnm={学年}&xqm={学期}
```

---

## 7. 学业与预警

### 7.1 学业情况 (HTML)

```
GET /jwglxt/xsxy/xsxyqk_cxXsxyqkIndex.html?gnmkdm=N105515&time={ts}
```

返回学业完成情况（已修学分、培养方案进度等），页面约 1.6MB。

### 7.2 学籍预警 (HTML)

```
GET /jwglxt/xjyj/xjyj_cxXjyjIndex.html?gnmkdm=N105505&time={ts}
```

---

## 8. 通知公告

### 8.1 通知列表 (JSON)

```
POST /jwglxt/xtgl/xwck_cxMoreXwList.html?doType=query

_search=false&nd={ts}&queryModel.showCount=15&queryModel.currentPage=1&queryModel.sortName=+&queryModel.sortOrder=desc&time=0
```

**响应字段:**

| 字段 | 说明 |
|------|------|
| `items[].xwbtqc` | 通知标题（全称） |
| `items[].xwbt` | 通知标题（可能截断） |
| `items[].fbsj` | 发布时间 |
| `items[].xwbh` | 新闻编号（用于获取详情） |
| `items[].fbrxm` | 发布人姓名 |
| `items[].sfzd` | 是否置顶 |
| `items[].sfyd` | 是否已读 |

### 8.2 通知详情 (HTML)

```
GET /jwglxt/xtgl/xwck_ckXw.html?xwbh={新闻编号}&doType=save
```

### 8.3 通知列表页 (HTML)

```
GET /jwglxt/xtgl/xwck_cxMoreXwList.html?doType=save
```

---

## 9. 待办事项

### 9.1 待办列表 (JSON)

```
POST /jwglxt/xtgl/index_cxDbsy.html?doType=query

flag=1&sfyy=1&_search=false&nd={ts}&queryModel.showCount=15&queryModel.currentPage=1&queryModel.sortName=cjsj+&queryModel.sortOrder=desc&time=0
```

**响应字段:**

| 字段 | 说明 |
|------|------|
| `items[].xxbt` | 事项标题 |
| `items[].xxnr` | 事项内容 |
| `items[].cjsj` | 创建时间 |
| `items[].clzt` | 处理状态 (0=未处理) |
| `items[].yhm` | 用户名 |

---

## 10. 首页数据

以下接口返回首页各区域的 HTML 片段，采用 **POST** 方式调用：

| 区域 | 接口 | 说明 |
|------|------|------|
| 课表 | `POST /xtgl/index_cxAreaOne.html?localeKey=zh_CN&gnmkdm=index` | 本周课表 |
| 文件 | `POST /xtgl/index_cxAreaTwo.html?localeKey=zh_CN&gnmkdm=index` | 文件下载 |
| 消息 | `POST /xtgl/index_cxAreaThree.html?localeKey=zh_CN&gnmkdm=index` | 系统消息 |
| 成绩/考试 | `POST /xtgl/index_cxAreaFour.html?localeKey=zh_CN&gnmkdm=index` | 成绩考试 tab |
| 校历 | `POST /xtgl/index_cxAreaFive.html?localeKey=zh_CN&gnmkdm=index` | 校历 |
| 校历文件 | `POST /xtgl/index_cxAreaSix.html?localeKey=zh_CN&gnmkdm=index` | 校历和文件 |
| 通知 | `POST /xtgl/index_cxNews.html?localeKey=zh_CN&gnmkdm=index` | 通知公告 |

其他首页接口：

| 接口 | 方法 | 说明 |
|------|------|------|
| `/xtgl/index_cxWdyy.html?localeKey=zh_CN&gnmkdm=index` | POST | 我的应用列表 |
| `/xtgl/index_cxZjsy.html?localeKey=zh_CN&gnmkdm=index` | POST | 最近使用 |
| `/xtgl/index_cxYhxxIndex.html?xt=jw&localeKey=zh_CN&gnmkdm=index` | POST | 用户信息 HTML (姓名/学号/院系/照片) |
| `/xtgl/photo_cxXszp4.html?xh_id={学号}&zplx=rxqzp` | GET | 学生照片 |
| `/xtgl/index_cxKczywIndex.html` | GET | 可选业务 |
| `/xtgl/index_cxGnjsView.html` | GET | 功能检索 |

---

## 11. 教材管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/jcydgl/xsjcyd_cxXsjcydIndex.html?gnmkdm=N253545` | GET | 教材预订 |
| `/jcjsgl/xsjs_cxJcfyqrIndex.html?gnmkdm=N758066` | GET | 教材费用确认 |
| `/jczdgl/jhjczdsq_cxJhjczdsqIndex.html?gnmkdm=N757010` | GET | 计划教材申请 |

---

## 12. 学生评价

| 接口 | 方法 | 说明 |
|------|------|------|
| `/xspjgl/xspj_cxXspjIndex.html?gnmkdm=N401605` | GET | 学生评价 |
| `/jxbpjgl/ddpjkc_cxDdpjkcIndex.html?gnmkdm=N401637` | GET | 督导评价 |
| `/jxbpjgl/ldpjkc_cxLdpjkcIndex.html?gnmkdm=N401642` | GET | 领导评价 |

> 注: 同行评价 (`N401622`) 连接被服务器拒绝，可能未开放。

---

## 13. 系统信息

| 接口 | 方法 | 说明 |
|------|------|------|
| `/xtgl/index_cxXttsxx.html` | POST | 系统提示信息 |
| `/xtgl/index_cxXttsxx.html?bj=2` | POST | 选修课毕业学分提示 |
| `/xtgl/index_cxKkyjxx.html` | POST | 旷课预警 |
| `/xtgl/index_cxLyyjxx.html` | POST | 劳育预警 |
| `/xtgl/index_cxXsxyyjtxIndex.html` | GET | 学业预警列表 |
| `/xtgl/index_cxXsxyyjtxView.html` | POST | 学业预警详情 |
| `/xtgl/index_cxJhkcjcsqWtjNum.html` | POST | 教材申请未提交数 |
| `/xtgl/index_cxXsGxkxfwxm.html` | POST | 公选课学分未修满 |
| `/xtgl/index_cxXspjWtjNum.html` | POST | 学生评价未提交数 |
| `/xtgl/index_cxFxjftsNum.html` | POST | 辅修缴费提醒 |
| `/xtgl/index_cxBsxtsj.html` | POST | 毕设选题时间 |
| `/xtgl/index_cxXfqrsj.html` | POST | 学分确认时间 |
| `/xtgl/index_cxThpjWtjNum.html` | POST | 同行评价未提交数 |
| `/xtgl/index_cxDdpjWtjNum.html` | POST | 督导评价未提交数 |
| `/xtgl/index_cxLdpjWtjNum.html` | POST | 领导评价未提交数 |
| `/xtgl/index_cxXxdlztgx.html` | POST | 信息已读状态更新 |
| `/xtgl/index_cxJssfqy.html` | POST | 角色是否启用 |
| `/xtgl/index_cxSzmrjs.html` | POST | 设置默认角色 |
| `/xtgl/index_cxJsjkxxList.html` | POST | 教师监考列表 |
| `/xtgl/index_cxJsjkxxView.html` | POST | 监考信息视图 |
| `/xtgl/index_yhqhAccount.html` | POST | 用户切换 |

---

## 14. 端点汇总表

### JSON 数据接口 (6 个)

| # | 接口 | 返回 |
|---|------|------|
| 1 | `POST /cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005` | 学期成绩 (13条) |
| 2 | `POST /kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151` | 个人课表 |
| 3 | `POST /kbcx/jskbcx_cxJsKb.html?gnmkdm=N2151` | 教师课表 |
| 4 | `POST /kwgl/kscx_cxXsksxxIndex.html?doType=query&gnmkdm=N3580` | 考试安排 |
| 5 | `POST /xtgl/xwck_cxMoreXwList.html?doType=query` | 通知列表 |
| 6 | `POST /xtgl/index_cxDbsy.html?doType=query` | 待办事项 |

### HTML 页面接口 (23 个，含成绩详情/统计/课表/选课/学业/评价/教材等)

见上述各模块章节。

### 不可用 (返回 404)

| 接口 | 说明 |
|------|------|
| `GET /pyfa/*` (3个) | 培养方案模块不可用 |
| `GET /xsxxxggl/xsxxck_cxXsxxIndex.html` | 学籍信息不可用 |
| `POST /xjyd/xjyd_cxXjydIndex.html` | 学籍异动不可用 |
| `POST /xsxk/xsxk_cxCxxkzy.html` | 选课结果不可用 |

### gnmkdm 编码表

| 编码 | 功能模块 |
|------|---------|
| `N305005` | 学生成绩查询 |
| `N2151` | 学生课表查询 |
| `N2158` | 课表/学分确认 |
| `N253501` | 班级课表 |
| `N3580` | 考试信息查询 |
| `N253512` | 自主选课 |
| `N105515` | 学生学业情况 |
| `N105505` | 学籍预警 |
| `N401605` | 学生评价 |
| `N401622` | 同行评价 (不可用) |
| `N401637` | 督导评价 |
| `N401642` | 领导评价 |
| `N253545` | 教材预订 |
| `N758066` | 教材费用确认 |
| `N757010` | 计划教材申请 |
| `N353088` | 考试监考信息 |

---

## 15. SDK 快速入门

```python
from jwxt_client import JwxtClient, LoginError

client = JwxtClient("学号", "密码")

try:
    client.login()
except LoginError as e:
    print(f"登录失败: {e}")
    exit(1)

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

# 获取首页全部区域
homepage = client.get_homepage_data()

# 获取学业情况
academic = client.get_academic_status()

# 通用查询 — 调用任意接口
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
2. 所有请求需携带登录后的 JSESSIONID cookie
3. 不要在请求头中声明 `br` (Brotli) 编码
4. 建议请求间添加适当延迟，避免触发频率限制
5. 部分接口需要先加载对应页面获取上下文，才能查询数据
