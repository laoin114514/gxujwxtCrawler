"""业务数据模型"""
from pydantic import BaseModel, Field, ConfigDict


class _AliasedModel(BaseModel):
    """支持字段名和别名同时使用的基类"""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")


# ========== 成绩 ==========

class GradeItem(_AliasedModel):
    """成绩条目"""
    course_name: str = Field(alias="kcmc", description="课程名称")
    score: str = Field(alias="cj", description="成绩")
    grade_point: str = Field(alias="jd", description="绩点")
    credit: str = Field(alias="xf", description="学分")
    course_type: str = Field(default="", alias="kcbj", description="课程标记")
    college: str = Field(default="", alias="kkxy", description="开课学院")
    course_code: str = Field(default="", alias="kch", description="课程号")
    class_id: str = Field(default="", alias="jxb_id", description="教学班ID")
    record_time: str = Field(default="", alias="cjbdsj", description="成绩录入时间")
    is_retake: str = Field(default="", alias="cjsfzf", description="是否重修")


class GradeQueryResult(_AliasedModel):
    """成绩查询结果"""
    items: list[GradeItem] = Field(default_factory=list)
    total: int = Field(default=0, alias="totalResult")


# ========== 考试 ==========

class ExamItem(_AliasedModel):
    """考试安排条目"""
    course_name: str = Field(alias="kcmc", description="课程名称")
    exam_time: str = Field(alias="kssj", description="考试时间")
    location: str = Field(alias="cdmc", description="考场地点")
    exam_name: str = Field(default="", alias="ksmc", description="考试名称")
    method: str = Field(default="", alias="khfs", description="考核方式")
    location_code: str = Field(default="", alias="cdbh", description="考场编号")


class ExamQueryResult(_AliasedModel):
    """考试查询结果"""
    items: list[ExamItem] = Field(default_factory=list)
    total: int = Field(default=0, alias="totalResult")


# ========== 通知 ==========

class NotificationItem(_AliasedModel):
    """通知公告条目"""
    title: str = Field(alias="xwbtqc", description="通知标题（全称）")
    title_short: str = Field(default="", alias="xwbt", description="通知标题（截断）")
    publish_date: str = Field(alias="fbsj", description="发布时间")
    news_id: str = Field(alias="xwbh", description="新闻编号")
    publisher: str = Field(default="", alias="fbrxm", description="发布人")
    is_pinned: str = Field(default="", alias="sfzd", description="是否置顶")
    is_read: str = Field(default="", alias="sfyd", description="是否已读")


class NotificationQueryResult(_AliasedModel):
    """通知查询结果"""
    items: list[NotificationItem] = Field(default_factory=list)
    total: int = Field(default=0, alias="totalResult")


# ========== 待办事项 ==========

class TodoItem(_AliasedModel):
    """待办事项条目"""
    title: str = Field(alias="xxbt", description="事项标题")
    content: str = Field(default="", alias="xxnr", description="事项内容")
    create_time: str = Field(alias="cjsj", description="创建时间")
    status: str = Field(default="0", alias="clzt", description="处理状态 (0=未处理)")
    username: str = Field(default="", alias="yhm", description="用户名")
    item_id: str = Field(default="", alias="id", description="事项ID")


class TodoQueryResult(_AliasedModel):
    """待办查询结果"""
    items: list[TodoItem] = Field(default_factory=list)
    total: int = Field(default=0, alias="totalResult")


# ========== 用户信息 ==========

class UserInfo(_AliasedModel):
    """用户信息（从 HTML 解析）"""
    name: str = Field(default="", description="姓名")
    student_id: str = Field(default="", description="学号")
    college: str = Field(default="", description="学院")
    major: str = Field(default="", description="专业")
    class_name: str = Field(default="", description="班级")
    photo_url: str = Field(default="", description="照片URL")
