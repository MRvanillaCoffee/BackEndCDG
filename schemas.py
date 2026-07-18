from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime

# ฟิลด์ทั้งหมด optional เพราะ user กรอกทีละหน้า/ทีละส่วนได้ (wizard, save draft)
class ProgramBase(BaseModel):
    program_code: str | None = None
    name_th: str | None = None
    name_en: str | None = None
    degree_name_th: str | None = None
    degree_abbr_th: str | None = None
    degree_name_en: str | None = None
    degree_abbr_en: str | None = None
    major: str | None = None
    program_format: str | None = None
    duration_years: Decimal | None = None
    program_category: str | None = None
    language: str | None = None
    admission_req: str | None = None
    degree_granting: str | None = None
    program_type: str | None = None
    open_year: str | None = None
    approval_details: str | None = None
    status: str = "draft"

    philosophy: str | None = None
    importance: str | None = None
    objectives: str | None = None
    uniqueness: str | None = None
    careers: str | None = None

    total_credits: int | None = None


class ProgramCreate(ProgramBase):
    """ใช้ตอน POST (หน้า 1) — บังคับ name_th อย่างน้อย"""
    name_th: str


class ProgramUpdate(ProgramBase):
    """ใช้ตอน PATCH — ทุกฟิลด์ optional หมด"""
    pass


class ProgramOut(ProgramBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)