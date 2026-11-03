-- ============================================================
-- Migration 001: course catalog relationships, category tree,
--                program favorites, curriculum type
--
-- Apply on top of new_Curriculum_DB.sql.
-- Safe to run more than once (IF NOT EXISTS everywhere).
-- Column types match the existing schema exactly
-- (ids are INT UNSIGNED, course.id is VARCHAR(20)) —
-- MariaDB rejects foreign keys whose types differ.
-- ============================================================

-- ------------------------------------------------------------
-- 1) program.curriculum_type  (new curriculum vs revision)
-- ------------------------------------------------------------
ALTER TABLE `program`
  ADD COLUMN IF NOT EXISTS `curriculum_type` ENUM('new','revision') NOT NULL DEFAULT 'new';

-- ------------------------------------------------------------
-- 2) course: total credits + who created it
-- ------------------------------------------------------------
ALTER TABLE `course`
  ADD COLUMN IF NOT EXISTS `credit_total` INT(11) DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS `created_by` INT(10) UNSIGNED DEFAULT NULL,
  ADD KEY IF NOT EXISTS `idx_course_created_by` (`created_by`),
  ADD CONSTRAINT `fk_course_created_by`
    FOREIGN KEY IF NOT EXISTS (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

-- ------------------------------------------------------------
-- 3) course_category: nesting, credit/hour type, note
--    parent_id NULL = top-level category
-- ------------------------------------------------------------
ALTER TABLE `course_category`
  ADD COLUMN IF NOT EXISTS `parent_id` INT(10) UNSIGNED DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS `credit_type` ENUM('credit','hour') NOT NULL DEFAULT 'credit',
  ADD COLUMN IF NOT EXISTS `note` TEXT DEFAULT NULL,
  ADD KEY IF NOT EXISTS `idx_course_category_parent_id` (`parent_id`),
  ADD CONSTRAINT `fk_course_category_parent`
    FOREIGN KEY IF NOT EXISTS (`parent_id`) REFERENCES `course_category` (`id`) ON DELETE CASCADE;

-- ------------------------------------------------------------
-- 4) course_prerequisite
--    A course cannot require itself; a pair can only appear once.
--    Deleting the *required* course is blocked (RESTRICT) rather than
--    silently rewriting other courses' rules.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `course_prerequisite` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `course_id` VARCHAR(20) NOT NULL,
  `prerequisite_course_id` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_course_prerequisite` (`course_id`, `prerequisite_course_id`),
  KEY `idx_course_prerequisite_target` (`prerequisite_course_id`),
  CONSTRAINT `chk_course_prerequisite_not_self` CHECK (`course_id` <> `prerequisite_course_id`),
  CONSTRAINT `fk_course_prerequisite_course`
    FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_course_prerequisite_target`
    FOREIGN KEY (`prerequisite_course_id`) REFERENCES `course` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 5) course_corequisite  (same rules as prerequisites)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `course_corequisite` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `course_id` VARCHAR(20) NOT NULL,
  `corequisite_course_id` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_course_corequisite` (`course_id`, `corequisite_course_id`),
  KEY `idx_course_corequisite_target` (`corequisite_course_id`),
  CONSTRAINT `chk_course_corequisite_not_self` CHECK (`course_id` <> `corequisite_course_id`),
  CONSTRAINT `fk_course_corequisite_course`
    FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_course_corequisite_target`
    FOREIGN KEY (`corequisite_course_id`) REFERENCES `course` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 6) course_category_assignment
--    Puts a course into a category-tree node with NO semester.
--    (program_course stays as-is for semester-based study plans.)
--    A course can sit in a category only once per program.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `course_category_assignment` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `program_id` INT(10) UNSIGNED NOT NULL,
  `category_id` INT(10) UNSIGNED NOT NULL,
  `course_id` VARCHAR(20) NOT NULL,
  `sort_order` INT(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_category_assignment` (`program_id`, `category_id`, `course_id`),
  KEY `idx_category_assignment_category` (`category_id`),
  KEY `idx_category_assignment_course` (`course_id`),
  CONSTRAINT `fk_category_assignment_program`
    FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_category_assignment_category`
    FOREIGN KEY (`category_id`) REFERENCES `course_category` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_category_assignment_course`
    FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- 7) program_favorite  (per-user star on a program)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `program_favorite` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `program_id` INT(10) UNSIGNED NOT NULL,
  `user_id` INT(10) UNSIGNED NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_program_favorite` (`program_id`, `user_id`),
  KEY `idx_program_favorite_user` (`user_id`),
  CONSTRAINT `fk_program_favorite_program`
    FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_program_favorite_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
