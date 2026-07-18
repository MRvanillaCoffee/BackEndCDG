# models.py
from sqlalchemy import (
    String, Integer, Text, DECIMAL, TIMESTAMP, Enum, ForeignKey, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


# ============================================================
# USERS
# ============================================================
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(
        Enum("admin", "coordinator", "reviewer", name="user_role"),
        nullable=False,
        default="coordinator",
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())

    programs: Mapped[list["Program"]] = relationship(back_populates="creator")
    reviews: Mapped[list["ProgramReview"]] = relationship(back_populates="reviewer")


# ============================================================
# PROGRAM (ตารางหลัก)
# ============================================================
class Program(Base):
    __tablename__ = "program"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )

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

    status: Mapped[str] = mapped_column(
        Enum("draft", "submitted", "under_review", "approved", "rejected", name="program_status"),
        nullable=False,
        default="draft",
    )

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

    creator: Mapped["User"] = relationship(back_populates="programs")
    reviews: Mapped[list["ProgramReview"]] = relationship(
        back_populates="program", cascade="all, delete-orphan"
    )


# ============================================================
# PROGRAM_REVIEW (ประวัติการตรวจสอบ/อนุมัติ)
# ============================================================
class ProgramReview(Base):
    __tablename__ = "program_review"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )
    reviewer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    decision: Mapped[str] = mapped_column(
        Enum("approved", "rejected", "comment", name="review_decision"), nullable=False
    )
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())

    program: Mapped["Program"] = relationship(back_populates="reviews")
    reviewer: Mapped["User"] = relationship(back_populates="reviews")