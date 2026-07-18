from sqlalchemy import String, Integer, Text, DECIMAL, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Program(Base):
    __tablename__ = "program"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_code: Mapped[str | None] = mapped_column(String(50))
    name_th: Mapped[str | None] = mapped_column(String(255))
    name_en: Mapped[str | None] = mapped_column(String(255))
    degree_name_th: Mapped[str | None] = mapped_column(String(255))
    degree_abbr_th: Mapped[str | None] = mapped_column(String(50))
    degree_name_en: Mapped[str | None] = mapped_column(String(255))
    degree_abbr_en: Mapped[str | None] = mapped_column(String(50))
    major: Mapped[str | None] = mapped_column(String(255))
    program_format: Mapped[str | None] = mapped_column(String(100))
    duration_years: Mapped[float | None] = mapped_column(DECIMAL(3, 1))
    program_category: Mapped[str | None] = mapped_column(String(255))
    language: Mapped[str | None] = mapped_column(String(255))
    admission_req: Mapped[str | None] = mapped_column(Text)
    degree_granting: Mapped[str | None] = mapped_column(String(255))
    program_type: Mapped[str | None] = mapped_column(String(100))
    open_year: Mapped[str | None] = mapped_column(String(100))
    approval_details: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="draft")

    philosophy: Mapped[str | None] = mapped_column(Text)
    importance: Mapped[str | None] = mapped_column(Text)
    objectives: Mapped[str | None] = mapped_column(Text)
    uniqueness: Mapped[str | None] = mapped_column(Text)
    careers: Mapped[str | None] = mapped_column(Text)

    total_credits: Mapped[int | None] = mapped_column(Integer)

    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )