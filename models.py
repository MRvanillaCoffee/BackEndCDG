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

    learning_attributes: Mapped[list["ProgramLearningAttribute"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    learning_dimension: Mapped["ProgramLearningDimension | None"] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
        uselist=False
    )

    plos: Mapped[list["Plo"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    plo_tqf_mappings: Mapped[list["PloTqfMapping"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    evaluation: Mapped["ProgramEvaluation | None"] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
        uselist=False
    )

    graduation_criteria: Mapped[list["ProgramGraduationCriteria"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    faculty_development: Mapped[list["ProgramFacultyDevelopment"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    quality_sections: Mapped[list["ProgramQualitySection"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    quality_kpis: Mapped[list["QualityKpi"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    evaluation_processes: Mapped[list["ProgramEvaluationProcess"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    quality_assurance: Mapped["QualityAssurance | None"] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
        uselist=False
    )

    admission: Mapped["ProgramAdmission | None"] = relationship(
        back_populates="program",
        cascade="all, delete-orphan",
        uselist=False
    )

    student_plans: Mapped[list["ProgramStudentPlan"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    semesters: Mapped[list["ProgramSemester"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    course_instructors: Mapped[list["CourseInstructor"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    plo_course_mappings: Mapped[list["PloCourseMapping"]] = relationship(
        back_populates="program",
        cascade="all, delete-orphan"
    )

    reviews: Mapped[list["ProgramReview"]] = relationship(
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


# ============================================================
# PROGRAM LEARNING ATTRIBUTE  (matches SQL: program_learning_attribute) — 4.2-4.6
# One row per domain (category = 'moral' | 'knowledge' | 'cognitive' |
# 'interpersonal' | 'numerical', etc.)
# ============================================================
class ProgramLearningAttribute(Base):
    __tablename__ = "program_learning_attribute"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    category: Mapped[str] = mapped_column(String(50), nullable=False)
    outcomes: Mapped[str | None] = mapped_column(Text, nullable=True)
    strategy: Mapped[str | None] = mapped_column(Text, nullable=True)
    assessment: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="learning_attributes")


# ============================================================
# PROGRAM LEARNING DIMENSION  (matches SQL: program_learning_dimension) — 4.7
# Singleton — one row per program, d1-d5 legend text.
# ============================================================
class ProgramLearningDimension(Base):
    __tablename__ = "program_learning_dimension"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    d1: Mapped[str | None] = mapped_column(Text, nullable=True)
    d2: Mapped[str | None] = mapped_column(Text, nullable=True)
    d3: Mapped[str | None] = mapped_column(Text, nullable=True)
    d4: Mapped[str | None] = mapped_column(Text, nullable=True)
    d5: Mapped[str | None] = mapped_column(Text, nullable=True)

    program: Mapped["Program"] = relationship(back_populates="learning_dimension")


# ============================================================
# PLO  (matches SQL: plo) — 4.9 (core, branch='') and 4.10 (branch-specific)
# ============================================================
class Plo(Base):
    __tablename__ = "plo"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    plo_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    domain: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description_th: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)
    outcome_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    branch: Mapped[str] = mapped_column(String(100), nullable=False, default="")

    program: Mapped["Program"] = relationship(back_populates="plos")


# ============================================================
# PLO TQF MAPPING  (matches SQL: plo_tqf_mapping) — 4.11
# ============================================================
class PloTqfMapping(Base):
    __tablename__ = "plo_tqf_mapping"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    plo_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    plo_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    d1: Mapped[bool] = mapped_column(default=False)
    d2: Mapped[bool] = mapped_column(default=False)
    d3: Mapped[bool] = mapped_column(default=False)
    d4: Mapped[bool] = mapped_column(default=False)
    d5: Mapped[bool] = mapped_column(default=False)

    program: Mapped["Program"] = relationship(back_populates="plo_tqf_mappings")


# ============================================================
# PROGRAM EVALUATION  (matches SQL: program_evaluation) — 5.1-5.3
# Singleton — one row per program.
# ============================================================
class ProgramEvaluation(Base):
    __tablename__ = "program_evaluation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    grading_rules: Mapped[str | None] = mapped_column(Text, nullable=True)
    achievement_verify: Mapped[str | None] = mapped_column(Text, nullable=True)
    graduation_criteria: Mapped[str | None] = mapped_column(Text, nullable=True)
    achievement_verify_during: Mapped[str | None] = mapped_column(Text, nullable=True)
    achievement_verify_after: Mapped[str | None] = mapped_column(Text, nullable=True)

    program: Mapped["Program"] = relationship(back_populates="evaluation")


# ============================================================
# PROGRAM GRADUATION CRITERIA  (matches SQL: program_graduation_criteria) — 5.4
# ============================================================
class ProgramGraduationCriteria(Base):
    __tablename__ = "program_graduation_criteria"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    criterion: Mapped[str] = mapped_column(Text, nullable=False)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="graduation_criteria")


# ============================================================
# PROGRAM FACULTY DEVELOPMENT  (matches SQL: program_faculty_development) — 6.1-6.3
# Generic per-section list — section_no keys each row to a page-6 topic
# (6.1 stores a single row, 6.2/6.3 store one row per list item).
# ============================================================
class ProgramFacultyDevelopment(Base):
    __tablename__ = "program_faculty_development"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    section_no: Mapped[str] = mapped_column(String(20), nullable=False)
    activity: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="faculty_development")


# ============================================================
# PROGRAM QUALITY SECTION  (matches SQL: program_quality_section) — 7.1-7.6
# ============================================================
class ProgramQualitySection(Base):
    __tablename__ = "program_quality_section"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    section_no: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="quality_sections")


# ============================================================
# QUALITY KPI  (matches SQL: quality_kpi) — 7.7
# ============================================================
class QualityKpi(Base):
    __tablename__ = "quality_kpi"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    kpi_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    y1: Mapped[bool] = mapped_column(default=False)
    y2: Mapped[bool] = mapped_column(default=False)
    y3: Mapped[bool] = mapped_column(default=False)
    y4: Mapped[bool] = mapped_column(default=False)
    y5: Mapped[bool] = mapped_column(default=False)

    program: Mapped["Program"] = relationship(back_populates="quality_kpis")


# ============================================================
# PROGRAM EVALUATION PROCESS  (matches SQL: program_evaluation_process) — 8.1-8.5
# ============================================================
class ProgramEvaluationProcess(Base):
    __tablename__ = "program_evaluation_process"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    section_no: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="evaluation_processes")


# ============================================================
# QUALITY ASSURANCE  (matches SQL: quality_assurance) — page 9
# Singleton — one row per program.
# ============================================================
class QualityAssurance(Base):
    __tablename__ = "quality_assurance"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    std_grad: Mapped[str | None] = mapped_column(Text, nullable=True)
    std_student: Mapped[str | None] = mapped_column(Text, nullable=True)
    std_faculty: Mapped[str | None] = mapped_column(Text, nullable=True)
    teaching_quality: Mapped[str | None] = mapped_column(Text, nullable=True)
    learning_support: Mapped[str | None] = mapped_column(Text, nullable=True)
    quality_plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_mgmt: Mapped[str | None] = mapped_column(Text, nullable=True)
    complaints: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_review: Mapped[str | None] = mapped_column(Text, nullable=True)
    communication: Mapped[str | None] = mapped_column(Text, nullable=True)

    program: Mapped["Program"] = relationship(back_populates="quality_assurance")


# ============================================================
# PROGRAM ADMISSION  (matches SQL: program_admission)
# Singleton — one row per program. Not currently used by any wired page
# (page 3's 3.5 uses the generic program_learning_topic fallback instead).
# ============================================================
class ProgramAdmission(Base):
    __tablename__ = "program_admission"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    qualifications: Mapped[str | None] = mapped_column(Text, nullable=True)
    selection_criteria: Mapped[str | None] = mapped_column(Text, nullable=True)
    other_conditions: Mapped[str | None] = mapped_column(Text, nullable=True)

    program: Mapped["Program"] = relationship(back_populates="admission")


# ============================================================
# PROGRAM STUDENT PLAN  (matches SQL: program_student_plan)
# One row per calendar year — no year-level breakdown, so this doesn't
# fit page 3's 3.8 matrix shape (which uses the JSON fallback instead).
# ============================================================
class ProgramStudentPlan(Base):
    __tablename__ = "program_student_plan"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    year_label: Mapped[str] = mapped_column(String(20), nullable=False)
    student_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    graduate_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="student_plans")


# ============================================================
# PROGRAM SEMESTER  (matches SQL: program_semester)
# Part of the deferred relational course-catalog subsystem.
# ============================================================
class ProgramSemester(Base):
    __tablename__ = "program_semester"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )

    year: Mapped[int] = mapped_column(Integer, nullable=False)
    term: Mapped[int] = mapped_column(Integer, nullable=False)

    program: Mapped["Program"] = relationship(back_populates="semesters")
    program_courses: Mapped[list["ProgramCourse"]] = relationship(back_populates="semester")


# ============================================================
# COURSE  (matches SQL: course)
# Global course catalog — NOT scoped to a single program (PK is the
# course code itself, a string, not an autoincrement id). Part of the
# deferred relational course-catalog subsystem.
# ============================================================
class Course(Base):
    __tablename__ = "course"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)

    name_th: Mapped[str | None] = mapped_column(String(255), nullable=True)
    name_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    credits: Mapped[str | None] = mapped_column(String(20), nullable=True)
    credit_lecture: Mapped[int | None] = mapped_column(Integer, nullable=True)
    credit_lab: Mapped[int | None] = mapped_column(Integer, nullable=True)
    credit_selfstudy: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description_th: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    prereq: Mapped[str | None] = mapped_column(Text, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)


# ============================================================
# PROGRAM COURSE  (matches SQL: program_course)
# Junction: which course, in which semester, under which category/branch.
# Part of the deferred relational course-catalog subsystem.
# ============================================================
class ProgramCourse(Base):
    __tablename__ = "program_course"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    semester_id: Mapped[int] = mapped_column(
        ForeignKey("program_semester.id", ondelete="CASCADE"), nullable=False
    )
    course_id: Mapped[str] = mapped_column(ForeignKey("course.id"), nullable=False)
    sort_order: Mapped[int | None] = mapped_column(default=0)
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("course_category.id"), nullable=True
    )
    branch: Mapped[str] = mapped_column(String(100), nullable=False, default="")

    semester: Mapped["ProgramSemester"] = relationship(back_populates="program_courses")


# ============================================================
# COURSE INSTRUCTOR  (matches SQL: course_instructor)
# Junction: which instructor teaches which course, for a given program.
# Part of the deferred relational course-catalog subsystem.
# ============================================================
class CourseInstructor(Base):
    __tablename__ = "course_instructor"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )
    course_id: Mapped[str] = mapped_column(ForeignKey("course.id"), nullable=False)
    instructor_id: Mapped[int | None] = mapped_column(
        ForeignKey("program_instructor.id"), nullable=True
    )
    instructor_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sort_order: Mapped[int] = mapped_column(default=0)

    program: Mapped["Program"] = relationship(back_populates="course_instructors")


# ============================================================
# PLO COURSE MAPPING  (matches SQL: plo_course_mapping)
# Which PLOs a given course addresses, and to what level.
# Part of the deferred relational course-catalog subsystem.
# ============================================================
class PloCourseMapping(Base):
    __tablename__ = "plo_course_mapping"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )
    plo_id: Mapped[int] = mapped_column(ForeignKey("plo.id", ondelete="CASCADE"), nullable=False)
    course_id: Mapped[str] = mapped_column(ForeignKey("course.id"), nullable=False)
    mapping_level: Mapped[str | None] = mapped_column(String(50), nullable=True)

    program: Mapped["Program"] = relationship(back_populates="plo_course_mappings")


# ============================================================
# USER  (matches SQL: users)
# Not scoped to a program — application-wide accounts. No endpoints
# exist yet; this is schema-only until auth is built.
# ============================================================
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(
        Enum("admin", "coordinator", "reviewer"), nullable=False, default="coordinator"
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)


# ============================================================
# PROGRAM REVIEW  (matches SQL: program_review)
# Approval workflow — a reviewer's decision on a program. No endpoints
# exist yet; this is schema-only until auth/review workflow is built.
# ============================================================
class ProgramReview(Base):
    __tablename__ = "program_review"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    program_id: Mapped[int] = mapped_column(
        ForeignKey("program.id", ondelete="CASCADE"), nullable=False
    )
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    decision: Mapped[str] = mapped_column(Enum("approved", "rejected", "comment"), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    program: Mapped["Program"] = relationship(back_populates="reviews")