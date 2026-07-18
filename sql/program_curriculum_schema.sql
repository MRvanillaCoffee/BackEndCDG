-- ============================================================
-- Program / Curriculum Database Schema (มคอ.2)
-- Generated from frontend forms: number1.vue - number9.vue
-- Dialect: PostgreSQL
-- ============================================================

-- ------------------------------------------------------------
-- 1. PROGRAM  (ตารางหลัก - หน้า 1, 2)
-- ------------------------------------------------------------
CREATE TABLE program (
    id                  SERIAL PRIMARY KEY,
    program_code        VARCHAR(50),
    name_th             VARCHAR(255),
    name_en             VARCHAR(255),
    degree_name_th      VARCHAR(255),
    degree_abbr_th      VARCHAR(50),
    degree_name_en      VARCHAR(255),
    degree_abbr_en      VARCHAR(50),
    major               VARCHAR(255),
    program_format      VARCHAR(100),          -- หลักสูตรระดับปริญญาตรี/โท/เอก
    duration_years      DECIMAL(3,1),
    program_category    VARCHAR(255),
    language            VARCHAR(255),
    admission_req        TEXT,
    degree_granting     VARCHAR(255),
    program_type        VARCHAR(100),          -- หลักสูตรใหม่ / หลักสูตรปรับปรุง
    open_year           VARCHAR(100),
    approval_details    TEXT,
    status              VARCHAR(20) NOT NULL DEFAULT 'draft',  -- draft / submitted / approved

    -- หน้า 2: ปรัชญา วัตถุประสงค์
    philosophy          TEXT,
    importance          TEXT,                  -- AI-assisted
    objectives          TEXT,                  -- AI-assisted
    uniqueness          TEXT,                  -- AI-assisted
    careers             TEXT,                  -- AI-assisted

    -- หน้า 3: หน่วยกิตรวม
    total_credits       INT,

    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ------------------------------------------------------------
-- 2. PLO - Program Learning Outcomes (หน้า 2)
-- ------------------------------------------------------------
CREATE TABLE plo (
    id                  SERIAL PRIMARY KEY,
    program_id          INT NOT NULL REFERENCES program(id) ON DELETE CASCADE,
    plo_code            VARCHAR(20),            -- เช่น PLO1
    domain              VARCHAR(100),           -- ด้านความรู้ / ทักษะ / ทัศนคติ / สมรรถนะ
    description_th      TEXT,
    sort_order          INT DEFAULT 0
);

CREATE INDEX idx_plo_program_id ON plo(program_id);

-- ------------------------------------------------------------
-- 3. YLO - Yearly Learning Outcomes (หน้า 2)
-- ------------------------------------------------------------
CREATE TABLE ylo (
    id                  SERIAL PRIMARY KEY,
    program_id          INT NOT NULL REFERENCES program(id) ON DELETE CASCADE,
    year                INT,                    -- ชั้นปีที่
    description          TEXT
);

CREATE INDEX idx_ylo_program_id ON ylo(program_id);

-- ------------------------------------------------------------
-- 4. COURSE - คลังรายวิชากลาง (หน้า 3)
-- ------------------------------------------------------------
CREATE TABLE course (
    id                  VARCHAR(20) PRIMARY KEY,   -- รหัสวิชา เช่น 010313005
    name_th             VARCHAR(255),
    name_en             VARCHAR(255),
    credits             VARCHAR(20),               -- เช่น "3(3-0-6)"
    credit_lecture      INT,
    credit_lab          INT,
    credit_selfstudy    INT
);

-- ------------------------------------------------------------
-- 5. COURSE_CATEGORY - หมวดวิชา (หน้า 3)
-- ------------------------------------------------------------
CREATE TABLE course_category (
    id                  SERIAL PRIMARY KEY,
    program_id          INT NOT NULL REFERENCES program(id) ON DELETE CASCADE,
    name_th             VARCHAR(255),           -- เช่น หมวดวิชาศึกษาทั่วไป
    required_credits    INT,
    sort_order          INT DEFAULT 0
);

CREATE INDEX idx_course_category_program_id ON course_category(program_id);

-- ------------------------------------------------------------
-- 6. PROGRAM_SEMESTER - ภาคการศึกษา (หน้า 3)
-- ------------------------------------------------------------
CREATE TABLE program_semester (
    id                  SERIAL PRIMARY KEY,
    program_id          INT NOT NULL REFERENCES program(id) ON DELETE CASCADE,
    year                INT NOT NULL,           -- ปีที่
    term                INT NOT NULL,           -- ภาคเรียนที่
    UNIQUE (program_id, year, term)
);

CREATE INDEX idx_program_semester_program_id ON program_semester(program_id);

-- ------------------------------------------------------------
-- 7. PROGRAM_COURSE - Mapping รายวิชา <-> ภาคการศึกษา (หน้า 3)
-- ------------------------------------------------------------
CREATE TABLE program_course (
    id                  SERIAL PRIMARY KEY,
    semester_id         INT NOT NULL REFERENCES program_semester(id) ON DELETE CASCADE,
    course_id           VARCHAR(20) NOT NULL REFERENCES course(id) ON DELETE RESTRICT,
    sort_order          INT DEFAULT 0,
    UNIQUE (semester_id, course_id)
);

CREATE INDEX idx_program_course_semester_id ON program_course(semester_id);
CREATE INDEX idx_program_course_course_id ON program_course(course_id);

-- ------------------------------------------------------------
-- 8. PROGRAM_LEARNING_PROCESS - การจัดกระบวนการเรียนรู้ (หน้า 4) - 1:1
-- ------------------------------------------------------------
CREATE TABLE program_learning_process (
    id                  SERIAL PRIMARY KEY,
    program_id          INT NOT NULL UNIQUE REFERENCES program(id) ON DELETE CASCADE,
    edu_system          VARCHAR(255),           -- ระบบทวิภาค ฯลฯ
    summer_edu          TEXT,
    credit_transfer     TEXT,
    schedule            VARCHAR(255),
    freshman_issues     TEXT,                   -- AI-assisted
    strategies          TEXT,                   -- AI-assisted
    fieldwork           TEXT,                   -- AI-assisted
    research_req        TEXT,
    growth_mindset      TEXT,                   -- AI-assisted
    real_world_learning TEXT                    -- AI-assisted
);

-- ------------------------------------------------------------
-- 9. PROGRAM_ADMISSION - คุณสมบัติของผู้เข้าศึกษา (หน้า 6) - 1:1
-- ------------------------------------------------------------
CREATE TABLE program_admission (
    id                  SERIAL PRIMARY KEY,
    program_id          INT NOT NULL UNIQUE REFERENCES program(id) ON DELETE CASCADE,
    qualifications      TEXT,
    selection_criteria  TEXT,
    other_conditions    TEXT
);

-- ------------------------------------------------------------
-- 10. PROGRAM_EVALUATION - การประเมินผลและเกณฑ์การสำเร็จ (หน้า 7) - 1:1
-- ------------------------------------------------------------
CREATE TABLE program_evaluation (
    id                  SERIAL PRIMARY KEY,
    program_id          INT NOT NULL UNIQUE REFERENCES program(id) ON DELETE CASCADE,
    grading_rules       TEXT,
    achievement_verify  TEXT,
    graduation_criteria TEXT
);

-- ------------------------------------------------------------
-- 11. QUALITY_KPI - ตัวบ่งชี้ผลการดำเนินงาน (หน้า 8) - 1:many
-- ------------------------------------------------------------
CREATE TABLE quality_kpi (
    id                  SERIAL PRIMARY KEY,
    program_id          INT NOT NULL REFERENCES program(id) ON DELETE CASCADE,
    kpi_name            VARCHAR(255),
    description          TEXT
);

CREATE INDEX idx_quality_kpi_program_id ON quality_kpi(program_id);

-- ------------------------------------------------------------
-- 12. QUALITY_ASSURANCE - องค์ประกอบ 8-9 ที่เหลือ (หน้า 8/9) - 1:1
-- ------------------------------------------------------------
CREATE TABLE quality_assurance (
    id                  SERIAL PRIMARY KEY,
    program_id          INT NOT NULL UNIQUE REFERENCES program(id) ON DELETE CASCADE,
    std_grad            TEXT,                   -- การกำกับมาตรฐาน (บัณฑิต)
    std_student         TEXT,                   -- การกำกับมาตรฐาน (นักศึกษา)
    std_faculty         TEXT,                   -- การกำกับมาตรฐาน (อาจารย์)
    teaching_quality    TEXT,                   -- ยังไม่มี UI ในหน้าปัจจุบัน (เตรียมไว้)
    learning_support    TEXT,                   -- ยังไม่มี UI ในหน้าปัจจุบัน (เตรียมไว้)
    quality_plan        TEXT,
    risk_mgmt           TEXT,
    complaints          TEXT,                   -- ยังไม่มี UI ในหน้าปัจจุบัน (เตรียมไว้)
    data_review         TEXT,                   -- ยังไม่มี UI ในหน้าปัจจุบัน (เตรียมไว้)
    communication       TEXT                    -- ยังไม่มี UI ในหน้าปัจจุบัน (เตรียมไว้)
);

-- เพิ่มต่อจาก schema เดิม (program_curriculum_schema_mysql.sql)

CREATE TABLE users (
    id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email               VARCHAR(255) NOT NULL UNIQUE,
    hashed_password     VARCHAR(255) NOT NULL,
    full_name           VARCHAR(255),
    role                ENUM('admin', 'coordinator', 'reviewer') NOT NULL DEFAULT 'coordinator',
    is_active           TINYINT(1) NOT NULL DEFAULT 1,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- program ต้องรู้ว่าใครเป็นเจ้าของ (coordinator คนไหนสร้าง)
ALTER TABLE program
    ADD COLUMN created_by INT UNSIGNED NULL AFTER id,
    ADD CONSTRAINT fk_program_created_by
        FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;

-- ขยาย status ให้รองรับ flow ตรวจสอบ-อนุมัติ
ALTER TABLE program
    MODIFY COLUMN status ENUM('draft', 'submitted', 'under_review', 'approved', 'rejected')
        NOT NULL DEFAULT 'draft';

-- เก็บ comment ของ reviewer ตอนตรวจ
CREATE TABLE program_review (
    id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    program_id          INT UNSIGNED NOT NULL,
    reviewer_id         INT UNSIGNED NOT NULL,
    decision            ENUM('approved', 'rejected', 'comment') NOT NULL,
    comment             TEXT,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_program FOREIGN KEY (program_id) REFERENCES program(id) ON DELETE CASCADE,
    CONSTRAINT fk_review_reviewer FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- ============================================================
-- Trigger: auto-update program.updated_at on row change
-- ============================================================
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_program_updated_at
BEFORE UPDATE ON program
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();
