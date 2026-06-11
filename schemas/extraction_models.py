"""
Pydantic 模型定义 -- 用于 week2 JSONL 抽取结果的校验。

两种记录类型:
  - SubscriptionFlow  : 认缴/增资流水
  - EquitySnapshot     : 股权结构时点快照
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# 枚举 / 公共字段
# ---------------------------------------------------------------------------

class RecordType(str, Enum):
    SUBSCRIPTION_FLOW = "subscription_flow"
    EQUITY_SNAPSHOT = "equity_snapshot"


# ---------------------------------------------------------------------------
# SubscriptionFlow 认缴流水
# ---------------------------------------------------------------------------

class SubscriptionFlow(BaseModel):
    """单条认缴/增资记录"""

    record_type: str = Field(..., description='必须为 "subscription_flow"')
    company_name: str = Field(..., description="公司全称")
    stock_code: str = Field(..., description="股票代码")
    subscription_date: Optional[str] = Field(None, description="认缴日期 (YYYY-MM-DD 或 YYYY-MM 或 YYYY)")
    investor_name: str = Field(..., description="投资者名称")
    investor_type: Optional[str] = Field(None, description="投资者类型 (PE/VC/天使/产业资本/政府引导基金/个人/其他)")
    event_type: Optional[str] = Field(None, description="事件类型 (增资/股权转让/出资认购/其他)")
    subscription_qty_wan: Optional[float] = Field(None, description="认缴股数 (万股)")
    subscription_amount_wan: Optional[float] = Field(None, description="认缴金额 (万元)")
    subscription_price: Optional[float] = Field(None, description="每股认购价格 (元/股)")
    currency: Optional[str] = Field(None, description="货币 (CNY/USD/其他)")
    evidence_text: Optional[str] = Field(None, description="招股书原文证据片段")
    extraction_notes: Optional[str] = Field(None, description="提取备注")

    @field_validator("record_type")
    @classmethod
    def validate_record_type(cls, v: str) -> str:
        if v != RecordType.SUBSCRIPTION_FLOW.value:
            raise ValueError(f'record_type 必须为 "{RecordType.SUBSCRIPTION_FLOW.value}", 实际为 "{v}"')
        return v

    @field_validator("subscription_qty_wan", "subscription_amount_wan", "subscription_price", mode="before")
    @classmethod
    def validate_non_negative(cls, v, info):
        # 允许股权转让场景下的负数（出让方）
        event_type = info.data.get("event_type", "")
        if event_type and ("转让" in event_type or "减资" in event_type):
            return v
        if v is not None and isinstance(v, (int, float)) and v < 0:
            raise ValueError("数值不能为负数（非股权转让/减资场景）")
        return v


# ---------------------------------------------------------------------------
# EquitySnapshot 股权快照 -- 股东级别
# ---------------------------------------------------------------------------

class ShareholderDetail(BaseModel):
    """单个股东在某一时点的持股信息"""

    shareholder_name: str = Field(..., description="股东名称")
    shares: Optional[float] = Field(None, description="持股数量 (万股)")
    shareholding_pct: Optional[float] = Field(None, description="持股比例 (%)")
    shareholder_type: Optional[str] = Field(None, description="股东类型 (创始人/PE/VC/员工持股平台/其他)")


# ---------------------------------------------------------------------------
# EquitySnapshot 股权快照
# ---------------------------------------------------------------------------

class EquitySnapshot(BaseModel):
    """某一时点的股权结构快照"""

    record_type: str = Field(..., description='必须为 "equity_snapshot"')
    company_name: str = Field(..., description="公司全称")
    stock_code: str = Field(..., description="股票代码")
    snapshot_label: str = Field(..., description="时点标签 (如 t0, t1, t2 ...)")
    snapshot_date: Optional[str] = Field(None, description="快照日期 (YYYY-MM-DD 或 YYYY-MM 或 YYYY)")
    total_shares: Optional[float] = Field(None, description="公司总股本 (万股)")
    registered_capital: Optional[float] = Field(None, description="注册资本 (万元)")
    shareholders: list[ShareholderDetail] = Field(default_factory=list, description="股东列表")
    evidence_text: Optional[str] = Field(None, description="招股书原文证据片段")
    extraction_notes: Optional[str] = Field(None, description="提取备注")

    @field_validator("record_type")
    @classmethod
    def validate_record_type(cls, v: str) -> str:
        if v != RecordType.EQUITY_SNAPSHOT.value:
            raise ValueError(f'record_type 必须为 "{RecordType.EQUITY_SNAPSHOT.value}", 实际为 "{v}"')
        return v
