-- ============================================================
-- Migration 002: widen program_learning_topic.content
--
-- Pages 3 and 4 store whole lists as JSON in this column (course lists,
-- study plans, course descriptions, the curriculum-mapping matrix).
-- TEXT holds at most 65,535 BYTES, and Thai characters take 3 bytes each,
-- so a normal curriculum (e.g. 80 course descriptions ≈ 224 KB) did not fit
-- and the save failed with a server error.
-- MEDIUMTEXT holds up to 16,777,215 bytes.
--
-- Safe to run more than once. Existing data is untouched.
-- Apply after 001_course_catalog_and_favorites.sql.
-- ============================================================

ALTER TABLE `program_learning_topic`
  MODIFY COLUMN `content` MEDIUMTEXT DEFAULT NULL;
