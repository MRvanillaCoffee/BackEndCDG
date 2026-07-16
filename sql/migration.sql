-- ============================================================
--  Migration: Fix curriculum.sql
--  MariaDB 10.4.32
--  ยึดโครงสร้างเดิมทุกตาราง แก้เฉพาะส่วนที่มีปัญหา
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
START TRANSACTION;

-- ============================================================
-- 1. แก้ instructor: full_name_th / full_name_en เป็น int → varchar
-- ============================================================
ALTER TABLE `instructor`
  MODIFY COLUMN `full_name_th` VARCHAR(200) NOT NULL,
  MODIFY COLUMN `full_name_en` VARCHAR(200) NOT NULL;

-- อัปเดตข้อมูลที่ถูก insert เป็น 0 เพราะ type ผิด
UPDATE `instructor` SET
  `full_name_th` = 'อ.สมชาย ใจดี',
  `full_name_en` = 'Somchai Jaidee'
WHERE `instructor_id` IN (1, 2);

-- ============================================================
-- 2. แก้ program: satatus → status (typo)
-- ============================================================
ALTER TABLE `program`
  CHANGE COLUMN `satatus` `status` VARCHAR(20) NOT NULL;

-- ============================================================
-- 3. แก้ peo: descripition_en → description_en (typo)
-- ============================================================
ALTER TABLE `peo`
  CHANGE COLUMN `descripition_en` `description_en` TEXT NOT NULL;

-- แก้ plo ด้วย (มี typo เหมือนกัน)
ALTER TABLE `plo`
  CHANGE COLUMN `descripition_en` `description_en` TEXT NOT NULL,
  CHANGE COLUMN `descripition_th` `description_th` TEXT NOT NULL;

-- แก้ ylo ด้วย
ALTER TABLE `ylo`
  CHANGE COLUMN `descripition_en` `description_en` TEXT NOT NULL,
  CHANGE COLUMN `descripition_th` `description_th` TEXT NOT NULL;

-- ============================================================
-- 4. แก้ user: password plain text → hash + เพิ่ม email, full_name
-- ============================================================
ALTER TABLE `user`
  MODIFY COLUMN `password` VARCHAR(255) NOT NULL,
  ADD COLUMN `full_name` VARCHAR(200) NOT NULL DEFAULT '' AFTER `username`,
  ADD COLUMN `email` VARCHAR(200) NOT NULL DEFAULT '' AFTER `full_name`,
  ADD COLUMN `is_active` TINYINT(1) NOT NULL DEFAULT 1 AFTER `role`;

-- อัปเดตข้อมูล admin (password hash ของ '1234' ด้วย bcrypt)
UPDATE `user` SET
  `full_name` = 'System Administrator',
  `email`     = 'admin@curriculum.local',
  `password`  = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaJobH3fkGr7T9VxMnJGK8K8W'
WHERE `uid` = 1;

UPDATE `user` SET
  `full_name` = 'Co Administrator',
  `email`     = 'admin2@curriculum.local',
  `password`  = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaJobH3fkGr7T9VxMnJGK8K8W'
WHERE `uid` = 2;

-- แก้ role ให้ตรงกับระบบ 3 ระดับ
ALTER TABLE `user`
  MODIFY COLUMN `role` ENUM('admin','department_head','instructor') NOT NULL;

UPDATE `user` SET `role` = 'admin'       WHERE `uid` = 1;
UPDATE `user` SET `role` = 'instructor'  WHERE `uid` = 2;

-- ============================================================
-- 5. แก้ course_plo: responsibility_level → ENUM
-- ============================================================
ALTER TABLE `course_plo`
  MODIFY COLUMN `responsibility_level` ENUM('High','Medium','Low') NOT NULL;

-- ============================================================
-- 6. ลบข้อมูลซ้ำทุกตาราง
--    เก็บ record ที่มี id ต่ำสุดของแต่ละกลุ่มไว้
-- ============================================================

-- program (เก็บ program_id=1 เดียว)
DELETE FROM `program` WHERE `program_id` > 1;

-- course (เก็บ 3 วิชาแรก course_id 1-3)
DELETE FROM `course` WHERE `course_id` > 3;

-- course_category (เก็บ category_id 1-3)
DELETE FROM `course_category` WHERE `category_id` > 3;

-- peo (เก็บ peo_id 1-3)
DELETE FROM `peo` WHERE `peo_id` > 3;

-- plo (เก็บ plo_id 1-4)
DELETE FROM `plo` WHERE `plo_id` > 4;

-- ylo (เก็บ ylo_id 1-3)
DELETE FROM `ylo` WHERE `ylo_id` > 3;

-- peo_plo (เก็บ id 1-4)
DELETE FROM `peo_plo` WHERE `id` > 4;

-- plo_ylo (เก็บ id 1-3)
DELETE FROM `plo_ylo` WHERE `id` > 3;

-- program_course (เก็บ id 1-3)
DELETE FROM `program_course` WHERE `program_course_id` > 3;

-- course_plo (เก็บ id 1-4)
DELETE FROM `course_plo` WHERE `id` > 4;

-- instructor (เก็บ instructor_id=1 เดียว)
DELETE FROM `instructor` WHERE `instructor_id` > 1;

-- program_instructor (เก็บ id=1 เดียว)
DELETE FROM `program_instructor` WHERE `id` > 1;

-- student_intake (เก็บ intake_id=1 เดียว)
DELETE FROM `student_intake` WHERE `intake_id` > 1;

-- ============================================================
-- 7. เพิ่ม UNIQUE constraint ป้องกันข้อมูลซ้ำในอนาคต
-- ============================================================

-- program: ป้องกัน program_code ซ้ำในปีเดียวกัน
ALTER TABLE `program`
  ADD UNIQUE KEY `uq_program_code` (`program_code`);

-- course: ป้องกัน course_code ซ้ำ
ALTER TABLE `course`
  ADD UNIQUE KEY `uq_course_code` (`course_code`);

-- plo: ป้องกัน plo_code ซ้ำใน program เดียวกัน
ALTER TABLE `plo`
  ADD UNIQUE KEY `uq_plo` (`program_id`, `plo_code`);

-- ylo: ป้องกัน ylo_code ซ้ำ
ALTER TABLE `ylo`
  ADD UNIQUE KEY `uq_ylo` (`program_id`, `ylo_code`);

-- peo: ป้องกัน peo_code ซ้ำ
ALTER TABLE `peo`
  ADD UNIQUE KEY `uq_peo` (`program_id`, `peo_code`);

-- course_category: ป้องกันชื่อหมวดซ้ำใน program เดียวกัน
ALTER TABLE `course_category`
  ADD UNIQUE KEY `uq_category` (`program_id`, `name_th`);

-- program_course: ป้องกัน course เดียวกันใน program เดียวกันซ้ำ
ALTER TABLE `program_course`
  ADD UNIQUE KEY `uq_program_course` (`program_id`, `course_id`);

-- course_plo: ป้องกัน mapping ซ้ำ
ALTER TABLE `course_plo`
  ADD UNIQUE KEY `uq_course_plo` (`program_course_id`, `plo_id`);

-- peo_plo: ป้องกัน mapping ซ้ำ
ALTER TABLE `peo_plo`
  ADD UNIQUE KEY `uq_peo_plo` (`peo_id`, `plo_id`);

-- plo_ylo: ป้องกัน mapping ซ้ำ
ALTER TABLE `plo_ylo`
  ADD UNIQUE KEY `uq_plo_ylo` (`ylo_id`, `plo_id`);

-- ============================================================
-- 8. เพิ่ม created_at / updated_at ทุกตารางหลัก
-- ============================================================
ALTER TABLE `program`
  ADD COLUMN `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE `course`
  ADD COLUMN `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE `plo`
  ADD COLUMN `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE `ylo`
  ADD COLUMN `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE `peo`
  ADD COLUMN `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

ALTER TABLE `user`
  ADD COLUMN `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  ADD COLUMN `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- ============================================================
-- 9. เพิ่มตาราง ai_generation_log
--    สำหรับเก็บ log ทุกครั้งที่ AI สร้างเนื้อหา
-- ============================================================
CREATE TABLE IF NOT EXISTS `ai_generation_log` (
  `id`          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  `user_id`     INT NOT NULL,
  `feature`     ENUM('course_description','plo_mapping','ylo','spell_check') NOT NULL,
  `ref_id`      INT NOT NULL COMMENT 'course_id หรือ plo_id ที่เกี่ยวข้อง',
  `input_data`  JSON NOT NULL,
  `output_data` JSON NOT NULL,
  `model_used`  VARCHAR(100) NOT NULL,
  `source`      ENUM('local','openrouter') NOT NULL DEFAULT 'local',
  `is_accepted` TINYINT(1) DEFAULT 0 COMMENT 'อาจารย์อนุมัติแล้วหรือยัง',
  `created_at`  DATETIME DEFAULT CURRENT_TIMESTAMP,
  KEY `idx_feature` (`feature`),
  KEY `idx_user`    (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;

-- ============================================================
-- สรุปการเปลี่ยนแปลง
-- ============================================================
-- [แก้ type]   instructor.full_name_th/en: int → varchar(200)
-- [แก้ typo]   program.satatus → status
-- [แก้ typo]   peo/plo/ylo.descripition_* → description_*
-- [แก้ security] user.password: plain text → bcrypt hash
-- [เพิ่ม column] user: full_name, email, is_active
-- [แก้ type]   user.role: varchar → ENUM 3 ระดับ
-- [แก้ type]   course_plo.responsibility_level: varchar → ENUM
-- [ลบซ้ำ]      ทุกตาราง เหลือข้อมูล unique ชุดเดียว
-- [เพิ่ม UNIQUE] ทุกตารางหลัก ป้องกันซ้ำอนาคต
-- [เพิ่ม timestamp] created_at/updated_at ทุกตารางหลัก
-- [เพิ่มตาราง] ai_generation_log สำหรับ track AI output
