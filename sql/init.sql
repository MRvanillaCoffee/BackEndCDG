-- ============================================================
--  Curriculum Management System — MariaDB Schema
--  Engine: InnoDB | Charset: utf8mb4
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ─── ผู้ใช้งานและสิทธิ์ ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name     VARCHAR(200) NOT NULL,
    email         VARCHAR(200) NOT NULL UNIQUE,
    role          ENUM('admin','department_head','instructor') NOT NULL,
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── ภาควิชา ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS departments (
    id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    code       VARCHAR(20)  NOT NULL UNIQUE,
    name_th    VARCHAR(200) NOT NULL,
    name_en    VARCHAR(200) NOT NULL,
    faculty    VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── หลักสูตร ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS curriculums (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    department_id   INT UNSIGNED NOT NULL,
    name_th         VARCHAR(300) NOT NULL,
    name_en         VARCHAR(300) NOT NULL,
    degree_th       VARCHAR(100) NOT NULL,  -- ชื่อปริญญา ไทย
    degree_en       VARCHAR(100) NOT NULL,
    version_year    YEAR        NOT NULL,   -- ปี พ.ศ. ของหลักสูตร
    status          ENUM('draft','active','archived') DEFAULT 'draft',
    parent_id       INT UNSIGNED NULL,      -- อ้างอิงหลักสูตรเดิม (ก่อนปรับปรุง)
    total_credits   SMALLINT UNSIGNED,
    created_by      INT UNSIGNED NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (parent_id)     REFERENCES curriculums(id),
    FOREIGN KEY (created_by)    REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── PLO (Program Learning Outcomes) ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS plo (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    curriculum_id INT UNSIGNED NOT NULL,
    code          VARCHAR(20)  NOT NULL,   -- e.g. PLO1, PLO2
    tqf_domain    TINYINT UNSIGNED NOT NULL, -- 1-5 ตาม TQF
    description   TEXT         NOT NULL,
    sort_order    TINYINT UNSIGNED DEFAULT 0,
    UNIQUE KEY uq_plo (curriculum_id, code),
    FOREIGN KEY (curriculum_id) REFERENCES curriculums(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── YLO (Year Learning Outcomes) ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ylo (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    curriculum_id INT UNSIGNED NOT NULL,
    year_level    TINYINT UNSIGNED NOT NULL, -- 1-4
    branch        VARCHAR(100) NULL,          -- แขนงวิชา (ถ้ามี)
    description   TEXT         NOT NULL,
    FOREIGN KEY (curriculum_id) REFERENCES curriculums(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── YLO → PLO mapping ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ylo_plo_mapping (
    ylo_id INT UNSIGNED NOT NULL,
    plo_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (ylo_id, plo_id),
    FOREIGN KEY (ylo_id) REFERENCES ylo(id) ON DELETE CASCADE,
    FOREIGN KEY (plo_id) REFERENCES plo(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── หมวดหมู่รายวิชา ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS course_categories (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    curriculum_id INT UNSIGNED NOT NULL,
    name_th       VARCHAR(200) NOT NULL,  -- e.g. วิชาศึกษาทั่วไป
    name_en       VARCHAR(200) NOT NULL,
    required_credits  SMALLINT UNSIGNED DEFAULT 0,
    elective_credits  SMALLINT UNSIGNED DEFAULT 0,
    sort_order    TINYINT UNSIGNED DEFAULT 0,
    FOREIGN KEY (curriculum_id) REFERENCES curriculums(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── รายวิชา ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS courses (
    id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    curriculum_id   INT UNSIGNED NOT NULL,
    category_id     INT UNSIGNED NOT NULL,
    code            VARCHAR(20)  NOT NULL,
    name_th         VARCHAR(300) NOT NULL,
    name_en         VARCHAR(300) NOT NULL,
    credits         TINYINT UNSIGNED NOT NULL,
    lecture_hours   TINYINT UNSIGNED DEFAULT 0,
    lab_hours       TINYINT UNSIGNED DEFAULT 0,
    self_hours      TINYINT UNSIGNED DEFAULT 0,
    year_level      TINYINT UNSIGNED NOT NULL,  -- 1-4
    semester        TINYINT UNSIGNED NOT NULL,  -- 1-3 (3=ฤดูร้อน)
    description_th  TEXT,
    description_en  TEXT,
    is_elective     BOOLEAN DEFAULT FALSE,
    instructor_id   INT UNSIGNED NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_course (curriculum_id, code),
    FOREIGN KEY (curriculum_id) REFERENCES curriculums(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id)   REFERENCES course_categories(id),
    FOREIGN KEY (instructor_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── วิชาบังคับก่อน ──────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS course_prerequisites (
    course_id      INT UNSIGNED NOT NULL,
    prerequisite_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (course_id, prerequisite_id),
    FOREIGN KEY (course_id)       REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (prerequisite_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── CLO (Course Learning Outcomes) ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS clo (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_id   INT UNSIGNED NOT NULL,
    code        VARCHAR(20)  NOT NULL,   -- e.g. CLO1
    description TEXT         NOT NULL,
    sort_order  TINYINT UNSIGNED DEFAULT 0,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── PLO Mapping (Course → PLO) ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS course_plo_mapping (
    course_id  INT UNSIGNED NOT NULL,
    plo_id     INT UNSIGNED NOT NULL,
    level      ENUM('main','minor') NOT NULL DEFAULT 'minor',
    PRIMARY KEY (course_id, plo_id),
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (plo_id)    REFERENCES plo(id)     ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── CLO → PLO mapping ───────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS clo_plo_mapping (
    clo_id INT UNSIGNED NOT NULL,
    plo_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (clo_id, plo_id),
    FOREIGN KEY (clo_id) REFERENCES clo(id) ON DELETE CASCADE,
    FOREIGN KEY (plo_id) REFERENCES plo(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── ประวัติการแก้ไข (Audit Log) ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_logs (
    id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id     INT UNSIGNED NOT NULL,
    action      VARCHAR(50)  NOT NULL,  -- CREATE, UPDATE, DELETE
    table_name  VARCHAR(100) NOT NULL,
    record_id   INT UNSIGNED NOT NULL,
    old_value   JSON NULL,
    new_value   JSON NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── AI Generation Log ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_generation_logs (
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id      INT UNSIGNED NOT NULL,
    feature      ENUM('course_description','plo_mapping','ylo','spell_check') NOT NULL,
    input_data   JSON NOT NULL,
    output_data  JSON NOT NULL,
    model_used   VARCHAR(100) NOT NULL,
    source       ENUM('local','openrouter') NOT NULL,
    is_accepted  BOOLEAN DEFAULT FALSE,  -- อาจารย์อนุมัติหรือไม่
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

-- ─── Seed: Default Admin ──────────────────────────────────────────────────────
INSERT IGNORE INTO users (username, password_hash, full_name, email, role)
VALUES ('admin', '$2b$12$placeholder_change_this', 'System Administrator', 'admin@curriculum.local', 'admin');
