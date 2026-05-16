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


# ========== 选课 ==========

class CourseItem(_AliasedModel):
    """可选课程条目"""
    course_code: str = Field(default="", alias="kch", description="课程号")
    course_name: str = Field(default="", alias="kcmc", description="课程名称")
    credit: str = Field(default="", alias="xf", description="学分")
    is_retake: str = Field(default="", alias="cxbj", description="是否重修 (0/1)")
    is_minor: str = Field(default="", alias="fxbj", description="是否辅修 (0/1)")
    is_limited: str = Field(default="", alias="xxkbj", description="是否限制选课")
    is_recommended: str = Field(default="", alias="sftj", description="是否推荐课程")
    class_type: str = Field(default="", alias="kclxmc", description="课程类型名称")
    group_name: str = Field(default="", alias="kzmc", description="课程组名称")
    class_id: str = Field(default="", alias="jxb_id", description="教学班ID")
    class_name: str = Field(default="", alias="jxbmc", description="教学班名称")
    capacity: str = Field(default="", alias="jxbzrl", description="教学班容量")
    selected_count: str = Field(default="", alias="yxzrs", description="已选人数")
    kc_row: str = Field(default="", alias="kcrow", description="课程行号")


class CourseClassDetail(_AliasedModel):
    """教学班详情"""
    class_id: str = Field(default="", alias="jxb_id", description="教学班ID")
    is_minor: str = Field(default="", alias="fxbj", description="辅修标记")
    is_required: str = Field(default="", alias="bxbj", description="必修标记")
    selected_count: str = Field(default="", alias="yxzrs", description="已选人数")
    capacity: str = Field(default="", alias="jxbrl", description="容量")
    schedule: str = Field(default="", alias="sksj", description="上课时间")
    classroom: str = Field(default="", alias="ktmc", description="课堂名称")
    location: str = Field(default="", alias="jxdd", description="教学地点")
    teach_mode: str = Field(default="", alias="jxms", description="教学模式")
    credit: str = Field(default="", alias="xf", description="学分")
    teach_method: str = Field(default="", alias="skfsmc", description="授课方式")
    exam_time: str = Field(default="", alias="kssj", description="考试时间")
    course_category: str = Field(default="", alias="kclbmc", description="课程类别")
    course_nature: str = Field(default="", alias="kcxzmc", description="课程性质")
    campus_name: str = Field(default="", alias="xqumc", description="校区名称")
    area_name: str = Field(default="", alias="yqmc", description="园区名称")
    college_name: str = Field(default="", alias="kkxymc", description="开课学院")
    teacher_info: str = Field(default="", alias="jsxx", description="教师信息")
    remark: str = Field(default="", alias="xkbz", description="选课备注")
    textbook_flag: str = Field(default="", alias="sfydjc", description="是否预定教材")
    pending_capacity: str = Field(default="", alias="dsfrl", description="待释放容量")


class CourseQueryResult(_AliasedModel):
    """选课查询结果"""
    items: list[CourseItem] = Field(default_factory=list, alias="tmpList")


class CourseClassResult(_AliasedModel):
    """教学班详情列表"""
    items: list[CourseClassDetail] = Field(default_factory=list)


# ========== 用户信息 ==========

class UserInfo(_AliasedModel):
    """用户信息（从 HTML 解析）"""
    name: str = Field(default="", description="姓名")
    student_id: str = Field(default="", description="学号")
    college: str = Field(default="", description="学院")
    major: str = Field(default="", description="专业")
    class_name: str = Field(default="", description="班级")
    photo_url: str = Field(default="", description="照片URL")
