"""通用模型：分页、学期等"""
import time
from typing import Optional, TypeVar
from pydantic import BaseModel, Field, ConfigDict


class _AliasedModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class PageQuery(_AliasedModel):
    """标准分页查询参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=100, ge=1, le=500, alias="showCount", description="每页条数")
    sort_name: str = Field(default="", alias="sortName")
    sort_order: str = Field(default="asc", alias="sortOrder")

    def to_form_data(self, **extra) -> dict:
        ts = int(time.time() * 1000)
        return {
            "_search": "false",
            "nd": ts,
            "queryModel.showCount": self.page_size,
            "queryModel.currentPage": self.page,
            "queryModel.sortName": self.sort_name,
            "queryModel.sortOrder": self.sort_order,
            "time": ts,
            **extra,
        }


class Semester(BaseModel):
    """学年学期"""
    year: str = Field(description="起始年份，如 '2025'")
    term: str = Field(description="学期编码: '3'=第一学期, '12'=第二学期")


T = TypeVar("T")
