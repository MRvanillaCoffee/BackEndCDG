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


class ProgramLearningAttributeCreate(BaseModel):
    category: str
    outcomes: str | None = None
    strategy: str | None = None
    assessment: str | None = None
    sort_order: int = 0


class ProgramLearningAttributeOut(ProgramLearningAttributeCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramLearningDimensionIn(BaseModel):
    d1: str | None = None
    d2: str | None = None
    d3: str | None = None
    d4: str | None = None
    d5: str | None = None


class ProgramLearningDimensionOut(ProgramLearningDimensionIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class PloCreate(BaseModel):
    plo_code: str | None = None
    domain: str | None = None
    description_th: str | None = None
    sort_order: int = 0
    outcome_type: str | None = None
    branch: str = ""


class PloOut(PloCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class PloTqfMappingCreate(BaseModel):
    plo_id: int | None = None
    plo_code: str | None = None
    d1: bool = False
    d2: bool = False
    d3: bool = False
    d4: bool = False
    d5: bool = False


class PloTqfMappingOut(PloTqfMappingCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramEvaluationIn(BaseModel):
    grading_rules: str | None = None
    achievement_verify: str | None = None
    graduation_criteria: str | None = None
    achievement_verify_during: str | None = None
    achievement_verify_after: str | None = None


class ProgramEvaluationOut(ProgramEvaluationIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramGraduationCriteriaCreate(BaseModel):
    criterion: str
    sort_order: int = 0


class ProgramGraduationCriteriaOut(ProgramGraduationCriteriaCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramFacultyDevelopmentCreate(BaseModel):
    section_no: str
    activity: str | None = None
    sort_order: int = 0


class ProgramFacultyDevelopmentOut(ProgramFacultyDevelopmentCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramQualitySectionCreate(BaseModel):
    section_no: str
    title: str | None = None
    content: str | None = None
    sort_order: int = 0


class ProgramQualitySectionOut(ProgramQualitySectionCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class QualityKpiCreate(BaseModel):
    kpi_name: str | None = None
    description: str | None = None
    y1: bool = False
    y2: bool = False
    y3: bool = False
    y4: bool = False
    y5: bool = False


class QualityKpiOut(QualityKpiCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramEvaluationProcessCreate(BaseModel):
    section_no: str
    content: str | None = None
    sort_order: int = 0


class ProgramEvaluationProcessOut(ProgramEvaluationProcessCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class QualityAssuranceIn(BaseModel):
    std_grad: str | None = None
    std_student: str | None = None
    std_faculty: str | None = None
    teaching_quality: str | None = None
    learning_support: str | None = None
    quality_plan: str | None = None
    risk_mgmt: str | None = None
    complaints: str | None = None
    data_review: str | None = None
    communication: str | None = None


class QualityAssuranceOut(QualityAssuranceIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramAdmissionIn(BaseModel):
    qualifications: str | None = None
    selection_criteria: str | None = None
    other_conditions: str | None = None


class ProgramAdmissionOut(ProgramAdmissionIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramStudentPlanCreate(BaseModel):
    year_label: str
    student_count: int | None = None
    graduate_count: int | None = None
    sort_order: int = 0


class ProgramStudentPlanOut(ProgramStudentPlanCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramSemesterCreate(BaseModel):
    year: int
    term: int


class ProgramSemesterOut(ProgramSemesterCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class CourseCreate(BaseModel):
    id: str
    name_th: str | None = None
    name_en: str | None = None
    credits: str | None = None
    credit_lecture: int | None = None
    credit_lab: int | None = None
    credit_selfstudy: int | None = None
    description_th: str | None = None
    description_en: str | None = None
    prereq: str | None = None
    note: str | None = None


class CourseOut(CourseCreate):
    model_config = ConfigDict(from_attributes=True)


class ProgramCourseCreate(BaseModel):
    semester_id: int
    course_id: str
    sort_order: int = 0
    category_id: int | None = None
    branch: str = ""


class ProgramCourseOut(ProgramCourseCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CourseInstructorCreate(BaseModel):
    course_id: str
    instructor_id: int | None = None
    instructor_name: str | None = None
    sort_order: int = 0


class CourseInstructorOut(CourseInstructorCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class PloCourseMappingCreate(BaseModel):
    plo_id: int
    course_id: str
    mapping_level: str | None = None


class PloCourseMappingOut(PloCourseMappingCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramReviewCreate(BaseModel):
    reviewer_id: int
    decision: str
    comment: str | None = None


class ProgramReviewOut(ProgramReviewCreate):
    id: int
    program_id: int
    created_at: datetime
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
    learning_attributes: list[ProgramLearningAttributeOut] = []
    plos: list[PloOut] = []
    plo_tqf_mappings: list[PloTqfMappingOut] = []
    graduation_criteria: list[ProgramGraduationCriteriaOut] = []
    faculty_development: list[ProgramFacultyDevelopmentOut] = []
    quality_sections: list[ProgramQualitySectionOut] = []
    quality_kpis: list[QualityKpiOut] = []
    evaluation_processes: list[ProgramEvaluationProcessOut] = []
    student_plans: list[ProgramStudentPlanOut] = []
    semesters: list[ProgramSemesterOut] = []
    course_instructors: list[CourseInstructorOut] = []
    plo_course_mappings: list[PloCourseMappingOut] = []
    reviews: list[ProgramReviewOut] = []

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