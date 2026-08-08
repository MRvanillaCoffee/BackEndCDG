from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime, date

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

    # section 1.5 (cont.) — already on the model, missing here before
    cooperation: str | None = None

    # section 1.7
    readiness: str | None = None

    # section 1.10
    location: str | None = None

    # section 1.11
    economic_situation: str | None = None
    social_situation: str | None = None

    # section 1.12
    development_plan: str | None = None
    university_mission: str | None = None

    # section 1.13
    other_courses_in: str | None = None
    other_courses_out: str | None = None
    administration: str | None = None

    # institution / bookkeeping — already on the model, missing here before
    university_name: str | None = None
    campus: str | None = None


class ProgramCreate(ProgramBase):
    """ใช้ตอน POST (หน้า 1) — บังคับ name_th อย่างน้อย"""
    name_th: str
    created_by: int | None = None


class ProgramUpdate(ProgramBase):
    """ใช้ตอน PATCH — ทุกฟิลด์ optional หมด"""
    pass


class ProgramMajorCreate(BaseModel):
    major_name: str
    sort_order: int = 0


class ProgramMajorOut(ProgramMajorCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramCareerCreate(BaseModel):
    career_name: str
    sort_order: int = 0


class ProgramCareerOut(ProgramCareerCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramApprovalCreate(BaseModel):
    committee: str | None = None
    approval_date: date | None = None
    note: str | None = None
    sort_order: int = 0


class ProgramApprovalOut(ProgramApprovalCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramInstructorCreate(BaseModel):
    name: str
    position: str | None = None
    degree: str | None = None
    branch: str | None = None
    research: str | None = None
    load_now: Decimal | None = None
    load_new: Decimal | None = None
    instructor_type: str = "responsible"
    sort_order: int = 0


class ProgramInstructorOut(ProgramInstructorCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramInstructorUpdate(BaseModel):
    name: str | None = None
    position: str | None = None
    degree: str | None = None
    branch: str | None = None
    research: str | None = None
    load_now: Decimal | None = None
    load_new: Decimal | None = None
    instructor_type: str | None = None
    sort_order: int | None = None


class ProgramDevelopmentPlanCreate(BaseModel):
    plan: str | None = None
    strategy: str | None = None
    indicator: str | None = None
    sort_order: int = 0


class ProgramDevelopmentPlanOut(ProgramDevelopmentPlanCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramEloFrameworkIn(BaseModel):
    framework: str | None = None


class ProgramEloFrameworkOut(ProgramEloFrameworkIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class YloCreate(BaseModel):
    year: int | None = None
    description: str | None = None
    branch: str = ""


class YloOut(YloCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramLearningTopicCreate(BaseModel):
    topic_no: str
    title: str | None = None
    content: str | None = None
    sort_order: int = 0


class ProgramLearningTopicOut(ProgramLearningTopicCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramScheduleCreate(BaseModel):
    semester_type: str
    schedule_text: str | None = None


class ProgramScheduleOut(ProgramScheduleCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramBudgetIncomeCreate(BaseModel):
    detail: str | None = None
    year_label: str
    amount: Decimal | None = None
    sort_order: int = 0


class ProgramBudgetIncomeOut(ProgramBudgetIncomeCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramBudgetExpenseCreate(BaseModel):
    category: str | None = None
    year_label: str
    amount: Decimal | None = None
    sort_order: int = 0


class ProgramBudgetExpenseOut(ProgramBudgetExpenseCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class CourseCategoryCreate(BaseModel):
    name_th: str | None = None
    required_credits: int | None = None
    sort_order: int = 0
    branch: str = ""


class CourseCategoryOut(CourseCategoryCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramOut(ProgramBase):
    id: int
    created_by: int | None = None
    created_at: datetime
    updated_at: datetime

    majors: list[ProgramMajorOut] = []
    careers_list: list[ProgramCareerOut] = []
    approvals: list[ProgramApprovalOut] = []
    instructors: list[ProgramInstructorOut] = []
    development_plans: list[ProgramDevelopmentPlanOut] = []
    ylos: list[YloOut] = []
    learning_topics: list[ProgramLearningTopicOut] = []
    schedules: list[ProgramScheduleOut] = []
    budget_incomes: list[ProgramBudgetIncomeOut] = []
    budget_expenses: list[ProgramBudgetExpenseOut] = []
    course_categories: list[CourseCategoryOut] = []

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str | None = None
    role: str = "coordinator"   # admin ตั้งตอนสร้างเท่านั้น

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str | None
    role: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ReviewIn(BaseModel):
    decision: str    # "approved" | "rejected" | "comment"
    comment: str | None = None