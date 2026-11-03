from typing import Annotated, Literal
from pydantic import AfterValidator, BaseModel, ConfigDict, Field, StringConstraints
from decimal import Decimal
from datetime import datetime, date

# VARCHAR(n) columns: reject over-long input with a 422 instead of letting
# MariaDB refuse it and surface as a 500. Lengths come from the live database.
Str20 = Annotated[str, StringConstraints(max_length=20)]
Str50 = Annotated[str, StringConstraints(max_length=50)]
Str100 = Annotated[str, StringConstraints(max_length=100)]
Str255 = Annotated[str, StringConstraints(max_length=255)]

# ENUM columns: only the values the database allows (anything else would be a 500).
CreditType = Literal['credit', 'hour']
CurriculumType = Literal['new', 'revision']
InstructorType = Literal['responsible', 'teaching', 'both']
ProgramStatus = Literal['draft', 'submitted', 'under_review', 'approved', 'rejected']
ReviewDecision = Literal['approved', 'rejected', 'comment']
SemesterType = Literal['semester1', 'semester2', 'summer']

# TEXT holds at most 65,535 BYTES, and a Thai character takes 3 bytes (so roughly
# 21,800 Thai characters). MEDIUMTEXT holds 16 MB; the API caps it at 10,000,000
# bytes, safely under MariaDB's default 16 MB packet size.
def _max_bytes(limit: int):
    def check(value: str) -> str:
        if len(value.encode("utf-8")) > limit:
            raise ValueError(
                f"text is too long: at most {limit:,} bytes in UTF-8 (a Thai character takes 3 bytes)"
            )
        return value
    return check

Text64K = Annotated[str, AfterValidator(_max_bytes(65_535))]
TextMedium = Annotated[str, AfterValidator(_max_bytes(10_000_000))]

# INT columns: stay inside the database's range (ids / foreign keys are checked by the routers).
Int32 = Annotated[int, Field(ge=-2_147_483_648, le=2_147_483_647)]

# DECIMAL(p,s): reject anything that would ROUND UP past the largest storable value
# (e.g. 99.95 rounds to 100.0 and does not fit DECIMAL(3,1); 99.94 does).
Decimal15_2 = Annotated[Decimal, Field(gt=Decimal('-9999999999999.995'), lt=Decimal('9999999999999.995'))]
Decimal3_1 = Annotated[Decimal, Field(gt=Decimal('-99.95'), lt=Decimal('99.95'))]
Decimal8_2 = Annotated[Decimal, Field(gt=Decimal('-999999.995'), lt=Decimal('999999.995'))]

# ฟิลด์ทั้งหมด optional เพราะ user กรอกทีละหน้า/ทีละส่วนได้ (wizard, save draft)
class ProgramBase(BaseModel):
    program_code: Str50 | None = None
    name_th: Str255 | None = None
    name_en: Str255 | None = None
    degree_name_th: Str255 | None = None
    degree_abbr_th: Str50 | None = None
    degree_name_en: Str255 | None = None
    degree_abbr_en: Str50 | None = None
    major: Str255 | None = None
    program_format: Str100 | None = None
    duration_years: Decimal3_1 | None = None
    program_category: Str255 | None = None
    language: Str255 | None = None
    admission_req: Text64K | None = None
    degree_granting: Str255 | None = None
    program_type: Str100 | None = None
    open_year: Str100 | None = None
    approval_details: Text64K | None = None
    status: ProgramStatus = "draft"
    curriculum_type: CurriculumType = "new"

    philosophy: Text64K | None = None
    importance: Text64K | None = None
    objectives: Text64K | None = None
    uniqueness: Text64K | None = None
    careers: Text64K | None = None

    total_credits: Int32 | None = None

    # section 1.5 (cont.) — already on the model, missing here before
    cooperation: Text64K | None = None

    # section 1.7
    readiness: Text64K | None = None

    # section 1.10
    location: Str255 | None = None

    # section 1.11
    economic_situation: Text64K | None = None
    social_situation: Text64K | None = None

    # section 1.12
    development_plan: Text64K | None = None
    university_mission: Text64K | None = None

    # section 1.13
    other_courses_in: Text64K | None = None
    other_courses_out: Text64K | None = None
    administration: Text64K | None = None

    # institution / bookkeeping — already on the model, missing here before
    university_name: Str255 | None = None
    campus: Str255 | None = None


class ProgramCreate(ProgramBase):
    """ใช้ตอน POST (หน้า 1) — บังคับ name_th อย่างน้อย"""
    name_th: Str255
    created_by: int | None = None


class ProgramUpdate(ProgramBase):
    """ใช้ตอน PATCH — ทุกฟิลด์ optional หมด"""
    pass


class ProgramMajorCreate(BaseModel):
    major_name: Str255
    sort_order: Int32 = 0


class ProgramMajorOut(ProgramMajorCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramCareerCreate(BaseModel):
    career_name: Str255
    sort_order: Int32 = 0


class ProgramCareerOut(ProgramCareerCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramApprovalCreate(BaseModel):
    committee: Str255 | None = None
    approval_date: date | None = None
    note: Text64K | None = None
    sort_order: Int32 = 0


class ProgramApprovalOut(ProgramApprovalCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramInstructorCreate(BaseModel):
    name: Str255
    position: Str255 | None = None
    degree: Str255 | None = None
    branch: Str100 | None = None
    research: Text64K | None = None
    load_now: Decimal8_2 | None = None
    load_new: Decimal8_2 | None = None
    instructor_type: InstructorType = "responsible"
    sort_order: Int32 = 0


class ProgramInstructorOut(ProgramInstructorCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramInstructorUpdate(BaseModel):
    name: Str255 | None = None
    position: Str255 | None = None
    degree: Str255 | None = None
    branch: Str100 | None = None
    research: Text64K | None = None
    load_now: Decimal8_2 | None = None
    load_new: Decimal8_2 | None = None
    instructor_type: InstructorType | None = None
    sort_order: Int32 | None = None


class ProgramDevelopmentPlanCreate(BaseModel):
    plan: Text64K | None = None
    strategy: Text64K | None = None
    indicator: Text64K | None = None
    sort_order: Int32 = 0


class ProgramDevelopmentPlanOut(ProgramDevelopmentPlanCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramEloFrameworkIn(BaseModel):
    framework: Text64K | None = None


class ProgramEloFrameworkOut(ProgramEloFrameworkIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class YloCreate(BaseModel):
    year: Int32 | None = None
    description: Text64K | None = None
    branch: Str100 = ""


class YloOut(YloCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramLearningTopicCreate(BaseModel):
    topic_no: Str20
    title: Str255 | None = None
    content: TextMedium | None = None
    sort_order: Int32 = 0


class ProgramLearningTopicOut(ProgramLearningTopicCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramScheduleCreate(BaseModel):
    semester_type: SemesterType
    schedule_text: Str255 | None = None


class ProgramScheduleOut(ProgramScheduleCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramBudgetIncomeCreate(BaseModel):
    detail: Str255 | None = None
    year_label: Str20
    amount: Decimal15_2 | None = None
    sort_order: Int32 = 0


class ProgramBudgetIncomeOut(ProgramBudgetIncomeCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramBudgetExpenseCreate(BaseModel):
    category: Str255 | None = None
    year_label: Str20
    amount: Decimal15_2 | None = None
    sort_order: Int32 = 0


class ProgramBudgetExpenseOut(ProgramBudgetExpenseCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class CourseCategoryCreate(BaseModel):
    name_th: Str255 | None = None
    required_credits: Int32 | None = None
    credit_type: CreditType = "credit"
    note: Text64K | None = None
    sort_order: Int32 = 0
    branch: Str100 = ""
    parent_id: int | None = None


class CourseCategoryOut(CourseCategoryCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramLearningAttributeCreate(BaseModel):
    category: Str50
    outcomes: Text64K | None = None
    strategy: Text64K | None = None
    assessment: Text64K | None = None
    sort_order: Int32 = 0


class ProgramLearningAttributeOut(ProgramLearningAttributeCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramLearningDimensionIn(BaseModel):
    d1: Text64K | None = None
    d2: Text64K | None = None
    d3: Text64K | None = None
    d4: Text64K | None = None
    d5: Text64K | None = None


class ProgramLearningDimensionOut(ProgramLearningDimensionIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class PloCreate(BaseModel):
    plo_code: Str20 | None = None
    domain: Str100 | None = None
    description_th: Text64K | None = None
    sort_order: Int32 = 0
    outcome_type: Str20 | None = None
    branch: Str100 = ""


class PloOut(PloCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class PloTqfMappingCreate(BaseModel):
    plo_id: int | None = None
    plo_code: Str20 | None = None
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
    grading_rules: Text64K | None = None
    achievement_verify: Text64K | None = None
    graduation_criteria: Text64K | None = None
    achievement_verify_during: Text64K | None = None
    achievement_verify_after: Text64K | None = None


class ProgramEvaluationOut(ProgramEvaluationIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramLearningProcessIn(BaseModel):
    # edu_system and schedule are VARCHAR(255) in the database, so the limit is
    # enforced here and an over-long value is rejected with a 422 instead of
    # reaching MariaDB and failing as a 500.
    edu_system: Str255 | None = None
    summer_edu: Text64K | None = None
    credit_transfer: Text64K | None = None
    schedule: Str255 | None = None
    freshman_issues: Text64K | None = None
    strategies: Text64K | None = None
    fieldwork: Text64K | None = None
    research_req: Text64K | None = None
    growth_mindset: Text64K | None = None
    real_world_learning: Text64K | None = None


class ProgramLearningProcessOut(ProgramLearningProcessIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramGraduationCriteriaCreate(BaseModel):
    criterion: Text64K
    sort_order: Int32 = 0


class ProgramGraduationCriteriaOut(ProgramGraduationCriteriaCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramFacultyDevelopmentCreate(BaseModel):
    section_no: Str20
    activity: Text64K | None = None
    sort_order: Int32 = 0


class ProgramFacultyDevelopmentOut(ProgramFacultyDevelopmentCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramQualitySectionCreate(BaseModel):
    section_no: Str20
    title: Str255 | None = None
    content: Text64K | None = None
    sort_order: Int32 = 0


class ProgramQualitySectionOut(ProgramQualitySectionCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class QualityKpiCreate(BaseModel):
    kpi_name: Str255 | None = None
    description: Text64K | None = None
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
    section_no: Str20
    content: Text64K | None = None
    sort_order: Int32 = 0


class ProgramEvaluationProcessOut(ProgramEvaluationProcessCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class QualityAssuranceIn(BaseModel):
    std_grad: Text64K | None = None
    std_student: Text64K | None = None
    std_faculty: Text64K | None = None
    teaching_quality: Text64K | None = None
    learning_support: Text64K | None = None
    quality_plan: Text64K | None = None
    risk_mgmt: Text64K | None = None
    complaints: Text64K | None = None
    data_review: Text64K | None = None
    communication: Text64K | None = None


class QualityAssuranceOut(QualityAssuranceIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramAdmissionIn(BaseModel):
    qualifications: Text64K | None = None
    selection_criteria: Text64K | None = None
    other_conditions: Text64K | None = None


class ProgramAdmissionOut(ProgramAdmissionIn):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramStudentPlanCreate(BaseModel):
    year_label: Str20
    student_count: Int32 | None = None
    graduate_count: Int32 | None = None
    sort_order: Int32 = 0


class ProgramStudentPlanOut(ProgramStudentPlanCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramSemesterCreate(BaseModel):
    year: Int32
    term: Int32


class ProgramSemesterOut(ProgramSemesterCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class CourseCreate(BaseModel):
    id: Str20
    name_th: Str255 | None = None
    name_en: Str255 | None = None
    credits: Str20 | None = None
    credit_total: Int32 | None = None
    credit_lecture: Int32 | None = None
    credit_lab: Int32 | None = None
    credit_selfstudy: Int32 | None = None
    description_th: Text64K | None = None
    description_en: Text64K | None = None
    prereq: Text64K | None = None
    note: Text64K | None = None
    created_by: int | None = None
    prerequisites: list[str] = []
    corequisites: list[str] = []


class CourseOut(BaseModel):
    id: str
    name_th: str | None = None
    name_en: str | None = None
    credits: str | None = None
    credit_total: int | None = None
    credit_lecture: int | None = None
    credit_lab: int | None = None
    credit_selfstudy: int | None = None
    description_th: str | None = None
    description_en: str | None = None
    prereq: str | None = None
    note: str | None = None
    created_by: int | None = None
    prerequisites: list[str] = []
    corequisites: list[str] = []
    model_config = ConfigDict(from_attributes=True)


class ProgramCourseCreate(BaseModel):
    semester_id: int
    course_id: Str20
    sort_order: Int32 = 0
    category_id: int | None = None
    branch: Str100 = ""


class ProgramCourseOut(ProgramCourseCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CourseInstructorCreate(BaseModel):
    course_id: Str20
    instructor_id: int | None = None
    instructor_name: Str255 | None = None
    sort_order: Int32 = 0


class CourseInstructorOut(CourseInstructorCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class PloCourseMappingCreate(BaseModel):
    plo_id: int
    course_id: Str20
    mapping_level: Str50 | None = None


class PloCourseMappingOut(PloCourseMappingCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramReviewCreate(BaseModel):
    reviewer_id: int
    decision: ReviewDecision
    comment: Text64K | None = None


class ProgramReviewOut(ProgramReviewCreate):
    id: int
    program_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CourseCategoryAssignmentCreate(BaseModel):
    category_id: int
    course_id: Str20
    sort_order: Int32 = 0


class CourseCategoryAssignmentOut(CourseCategoryAssignmentCreate):
    id: int
    program_id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramFavoriteOut(BaseModel):
    id: int
    program_id: int
    user_id: int
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
    category_assignments: list[CourseCategoryAssignmentOut] = []

    # Computed at request time by the router, not stored columns —
    # avoids stale data. Defaults let ProgramOut still validate from a
    # bare ORM object; the router overwrites these before returning.
    progress: int = 0
    is_starred: bool = False

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