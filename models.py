# models.py
from sqlalchemy import (
    String, Integer, Text, DECIMAL, TIMESTAMP, Enum, ForeignKey, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from datetime import date, datetime
from decimal import Decimal


class Base(DeclarativeBase):
    pass


# ============================================================
# PROGRAM
# ============================================================
class Program(Base):
    __tablename__ = "program"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    created_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    # ==========================================
    # Basic information - Section 1.1
    # ==========================================

    program_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    name_th: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # ==========================================
    # Degree information - Section 1.2
    # ==========================================

    degree_name_th: Mapped[str | None] = mapped_column(String(255), nullable=True)
    degree_abbr_th: Mapped[str | None] = mapped_column(String(50), nullable=True)
    degree_name_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    degree_abbr_en: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # ==========================================
    # Section 1.3 (major stored on program itself, in addition
    # to the per-major rows in ProgramMajor)
    # ==========================================

    major: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # ==========================================
    # Section 1.4
    # ==========================================

    total_credits: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # ==========================================
    # Program format - Section 1.5
    # ==========================================

    program_format: Mapped[str | None] = mapped_column(String(100), nullable=True)
    duration_years: Mapped[Decimal | None] = mapped_column(DECIMAL(3, 1), nullable=True)
    program_category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    program_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    language: Mapped[str | None] = mapped_column(String(255), nullable=True)
    admission_req: Mapped[str | None] = mapped_column(Text, nullable=True)
    cooperation: Mapped[str | None] = mapped_column(Text, nullable=True)
    degree_granting: Mapped[str | None] = mapped_column(String(255), nullable=True)
    open_year: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # ==========================================
    # Approval / workflow
    # ==========================================

    approval_details: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(
        Enum("draft", "submitted", "under_review", "approved", "rejected"),
        nullable=False,
        default="draft",
        server_default="draft"
    )

    # ==========================================
    # Narrative sections (used by later pages of the wizard)
    # ==========================================

    philosophy: Mapped[str | None] = mapped_column(Text, nullable=True)
    importance: Mapped[str | None] = mapped_column(Text, nullable=True)
    objectives: Mapped[str | None] = mapped_column(Text, nullable=True)
    uniqueness: Mapped[str | None] = mapped_column(Text, nullable=True)
    careers: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ==========================================
    # Timestamps
    # ==========================================

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ==========================================
    # Institution
    # ==========================================

    university_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    campus: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # ==========================================
    # Section 1.7
    # ==========================================

    readiness: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ==========================================
    # Section 1.10
    # ==========================================

    location: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # ==========================================
    # Section 1.11
    # ==========================================

    economic_situation: Mapped[str | None] = mapped_column(Text, nullable=True)
    social_situation: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ==========================================
    # Section 1.12
    # ==========================================

    development_plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    university_mission: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ==========================================
    # Section 1.13
    # ==========================================

    other_courses_in: Mapped[str | None] = mapped_column(Text, nullable=True)
    other_courses_out: Mapped[str | None] = mapped_column(Text, nullable=True)
    administration: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ==========================================
    # Relationships
    # ==========================================

    majors: Mapped[list["ProgramMajor"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    careers_list: Mapped[list["ProgramCareer"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    approvals: Mapped[list["ProgramApproval"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    instructors: Mapped[list["ProgramInstructor"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    development_plans: Mapped[list["ProgramDevelopmentPlan"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    elo_framework: Mapped["ProgramEloFramework | None"] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
        uselist=False
    )

    ylos: Mapped[list["Ylo"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    learning_topics: Mapped[list["ProgramLearningTopic"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    schedules: Mapped[list["ProgramSchedule"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    budget_incomes: Mapped[list["ProgramBudgetIncome"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    budget_expenses: Mapped[list["ProgramBudgetExpense"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    course_categories: Mapped[list["CourseCategory"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    # Keep your existing relationships
    # such as creator / reviews here.


# ============================================================
# PROGRAM MAJOR
# ============================================================
class ProgramMajor(Base):
    __tablename__ = "program_major"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )
    major_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="majors")


# ============================================================
# PROGRAM CAREER
# ============================================================
class ProgramCareer(Base):
    __tablename__ = "program_career"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )
    career_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="careers_list")


# ============================================================
# PROGRAM APPROVAL
# (columns match the SQL dump: `committee`, `approval_date`)
# ============================================================
class ProgramApproval(Base):
    __tablename__ = "program_approval"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    committee: Mapped[str | None] = mapped_column(String(255), nullable=True)
    approval_date: Mapped[date | None] = mapped_column(nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="approvals")


# ============================================================
# PROGRAM INSTRUCTOR
# ============================================================
class ProgramInstructor(Base):
    __tablename__ = "program_instructor"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[str | None] = mapped_column(String(255), nullable=True)
    degree: Mapped[str | None] = mapped_column(String(255), nullable=True)
    branch: Mapped[str | None] = mapped_column(String(100), nullable=True)
    research: Mapped[str | None] = mapped_column(Text, nullable=True)
    load_now: Mapped[Decimal | None] = mapped_column(DECIMAL(8, 2), nullable=True)
    load_new: Mapped[Decimal | None] = mapped_column(DECIMAL(8, 2), nullable=True)
    instructor_type: Mapped[str] = mapped_column(
        Enum("responsible", "teaching", "both"),
        nullable=False,
        default="responsible",
        server_default="responsible"
    )
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="instructors")


# ============================================================
# PROGRAM DEVELOPMENT PLAN  (matches SQL: program_development_plan)
# ============================================================
class ProgramDevelopmentPlan(Base):
    __tablename__ = "program_development_plan"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    strategy: Mapped[str | None] = mapped_column(Text, nullable=True)
    indicator: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="development_plans")


# ============================================================
# PROGRAM ELO FRAMEWORK  (matches SQL: program_elo_framework)
# One row per program — holds the four YLO-by-branch lists as one
# JSON blob in `framework`.
# ============================================================
class ProgramEloFramework(Base):
    __tablename__ = "program_elo_framework"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    framework: Mapped[str | None] = mapped_column(Text, nullable=True)

    program: Mapped["Program"] = relationship(back_populates="elo_framework")


# ============================================================
# YLO  (matches SQL: ylo)
# Itemized year-level learning outcomes, one row per year per branch.
# ============================================================
class Ylo(Base):
    __tablename__ = "ylo"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    branch: Mapped[str] = mapped_column(String(100), nullable=False, default="")

    program: Mapped["Program"] = relationship(back_populates="ylos")


# ============================================================
# PROGRAM LEARNING TOPIC  (generic catch-all — matches SQL: program_learning_topic)
# Used for any page-3 section that has no dedicated table: free-text
# sections store plain text in `content`; list sections store a JSON
# array string in `content`.
# ============================================================
class ProgramLearningTopic(Base):
    __tablename__ = "program_learning_topic"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    topic_no: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="learning_topics")


# ============================================================
# PROGRAM SCHEDULE  (matches SQL: program_schedule) — 3.4
# ============================================================
class ProgramSchedule(Base):
    __tablename__ = "program_schedule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    semester_type: Mapped[str] = mapped_column(
        Enum("semester1", "semester2", "summer"), nullable=False
    )
    schedule_text: Mapped[str | None] = mapped_column(String(255), nullable=True)

    program: Mapped["Program"] = relationship(back_populates="schedules")


# ============================================================
# PROGRAM BUDGET INCOME / EXPENSE  — 3.9 / 3.10
# (matches SQL: program_budget_income / program_budget_expense)
# One row per (item, year) cell — the frontend's year-columns table
# gets flattened into rows here.
# ============================================================
class ProgramBudgetIncome(Base):
    __tablename__ = "program_budget_income"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    detail: Mapped[str | None] = mapped_column(String(255), nullable=True)
    year_label: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[Decimal | None] = mapped_column(DECIMAL(15, 2), nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="budget_incomes")


class ProgramBudgetExpense(Base):
    __tablename__ = "program_budget_expense"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    year_label: Mapped[str] = mapped_column(String(20), nullable=False)
    amount: Mapped[Decimal | None] = mapped_column(DECIMAL(15, 2), nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="budget_expenses")


# ============================================================
# COURSE CATEGORY  (matches SQL: course_category) — 3.13
# ============================================================
class CourseCategory(Base):
    __tablename__ = "course_category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    name_th: Mapped[str | None] = mapped_column(String(255), nullable=True)
    required_credits: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)
    branch: Mapped[str] = mapped_column(String(100), nullable=False, default="")

    program: Mapped["Program"] = relationship(back_populates="course_categories")




