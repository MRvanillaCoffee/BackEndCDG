-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: mariadb:3306
-- Generation Time: Aug 08, 2026 at 05:05 PM
-- Server version: 11.7.2-MariaDB-ubu2404
-- PHP Version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `new_Curriculum_DB`
--

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `id` varchar(20) NOT NULL,
  `name_th` varchar(255) DEFAULT NULL,
  `name_en` varchar(255) DEFAULT NULL,
  `credits` varchar(20) DEFAULT NULL,
  `credit_lecture` int(11) DEFAULT NULL,
  `credit_lab` int(11) DEFAULT NULL,
  `credit_selfstudy` int(11) DEFAULT NULL,
  `description_th` text DEFAULT NULL,
  `description_en` text DEFAULT NULL,
  `prereq` text DEFAULT NULL,
  `note` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `course_category`
--

CREATE TABLE `course_category` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `name_th` varchar(255) DEFAULT NULL,
  `required_credits` int(11) DEFAULT NULL,
  `sort_order` int(11) DEFAULT 0,
  `branch` varchar(100) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `course_instructor`
--

CREATE TABLE `course_instructor` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `course_id` varchar(20) NOT NULL,
  `instructor_id` int(10) UNSIGNED DEFAULT NULL,
  `instructor_name` varchar(255) DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plo`
--

CREATE TABLE `plo` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `plo_code` varchar(20) DEFAULT NULL,
  `domain` varchar(100) DEFAULT NULL,
  `description_th` text DEFAULT NULL,
  `sort_order` int(11) DEFAULT 0,
  `outcome_type` varchar(20) DEFAULT NULL,
  `branch` varchar(100) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plo_course_mapping`
--

CREATE TABLE `plo_course_mapping` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `plo_id` int(10) UNSIGNED NOT NULL,
  `course_id` varchar(20) NOT NULL,
  `mapping_level` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plo_tqf_mapping`
--

CREATE TABLE `plo_tqf_mapping` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `plo_id` int(10) UNSIGNED DEFAULT NULL,
  `plo_code` varchar(20) DEFAULT NULL,
  `d1` tinyint(1) NOT NULL DEFAULT 0,
  `d2` tinyint(1) NOT NULL DEFAULT 0,
  `d3` tinyint(1) NOT NULL DEFAULT 0,
  `d4` tinyint(1) NOT NULL DEFAULT 0,
  `d5` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program`
--

CREATE TABLE `program` (
  `id` int(10) UNSIGNED NOT NULL,
  `created_by` int(10) UNSIGNED DEFAULT NULL,
  `program_code` varchar(50) DEFAULT NULL,
  `name_th` varchar(255) DEFAULT NULL,
  `name_en` varchar(255) DEFAULT NULL,
  `degree_name_th` varchar(255) DEFAULT NULL,
  `degree_abbr_th` varchar(50) DEFAULT NULL,
  `degree_name_en` varchar(255) DEFAULT NULL,
  `degree_abbr_en` varchar(50) DEFAULT NULL,
  `major` varchar(255) DEFAULT NULL,
  `program_format` varchar(100) DEFAULT NULL,
  `duration_years` decimal(3,1) DEFAULT NULL,
  `program_category` varchar(255) DEFAULT NULL,
  `language` varchar(255) DEFAULT NULL,
  `admission_req` text DEFAULT NULL,
  `degree_granting` varchar(255) DEFAULT NULL,
  `program_type` varchar(100) DEFAULT NULL,
  `open_year` varchar(100) DEFAULT NULL,
  `approval_details` text DEFAULT NULL,
  `status` enum('draft','submitted','under_review','approved','rejected') NOT NULL DEFAULT 'draft',
  `philosophy` text DEFAULT NULL,
  `importance` text DEFAULT NULL,
  `objectives` text DEFAULT NULL,
  `uniqueness` text DEFAULT NULL,
  `careers` text DEFAULT NULL,
  `total_credits` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `university_name` varchar(255) DEFAULT NULL,
  `campus` varchar(255) DEFAULT NULL,
  `cooperation` text DEFAULT NULL,
  `readiness` text DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `economic_situation` text DEFAULT NULL,
  `social_situation` text DEFAULT NULL,
  `development_plan` text DEFAULT NULL,
  `university_mission` text DEFAULT NULL,
  `other_courses_in` text DEFAULT NULL,
  `other_courses_out` text DEFAULT NULL,
  `administration` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `program`
--

INSERT INTO `program` (`id`, `created_by`, `program_code`, `name_th`, `name_en`, `degree_name_th`, `degree_abbr_th`, `degree_name_en`, `degree_abbr_en`, `major`, `program_format`, `duration_years`, `program_category`, `language`, `admission_req`, `degree_granting`, `program_type`, `open_year`, `approval_details`, `status`, `philosophy`, `importance`, `objectives`, `uniqueness`, `careers`, `total_credits`, `created_at`, `updated_at`, `university_name`, `campus`, `cooperation`, `readiness`, `location`, `economic_situation`, `social_situation`, `development_plan`, `university_mission`, `other_courses_in`, `other_courses_out`, `administration`) VALUES
(2, NULL, '8900', 'asdf', 'jk', 'asdf', 'a', 'asdf', 'a', 'no', 'หลักสูตรระดับปริญญาตรี', 4.0, 'asdft', 'asdfy', 'asdfg', 'ให้ปริญญาเพียงสาขาวิชาเดียว', 'หลักสูตรใหม่', 'fg6678', 'asdfashafhadfhafh', 'draft', NULL, NULL, NULL, NULL, NULL, NULL, '2026-07-18 13:38:29', '2026-07-18 13:38:29', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(3, 1, '', '', '', '', '', '', '', '', 'หลักสูตรระดับปริญญาตรี', NULL, '', '', '', 'ให้ปริญญาเพียงสาขาวิชาเดียว', 'หลักสูตรใหม่', '', '', 'draft', NULL, NULL, NULL, NULL, NULL, NULL, '2026-07-19 02:14:10', '2026-07-19 02:14:10', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `program_admission`
--

CREATE TABLE `program_admission` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `qualifications` text DEFAULT NULL,
  `selection_criteria` text DEFAULT NULL,
  `other_conditions` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_approval`
--

CREATE TABLE `program_approval` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `committee` varchar(255) DEFAULT NULL,
  `approval_date` date DEFAULT NULL,
  `note` text DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_budget_expense`
--

CREATE TABLE `program_budget_expense` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `category` varchar(255) DEFAULT NULL,
  `year_label` varchar(20) NOT NULL,
  `amount` decimal(15,2) DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_budget_income`
--

CREATE TABLE `program_budget_income` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `detail` varchar(255) DEFAULT NULL,
  `year_label` varchar(20) NOT NULL,
  `amount` decimal(15,2) DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_career`
--

CREATE TABLE `program_career` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `career_name` varchar(255) NOT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_course`
--

CREATE TABLE `program_course` (
  `id` int(10) UNSIGNED NOT NULL,
  `semester_id` int(10) UNSIGNED NOT NULL,
  `course_id` varchar(20) NOT NULL,
  `sort_order` int(11) DEFAULT 0,
  `category_id` int(10) UNSIGNED DEFAULT NULL,
  `branch` varchar(100) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_development_plan`
--

CREATE TABLE `program_development_plan` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `plan` text DEFAULT NULL,
  `strategy` text DEFAULT NULL,
  `indicator` text DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_elo_framework`
--

CREATE TABLE `program_elo_framework` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `framework` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_evaluation`
--

CREATE TABLE `program_evaluation` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `grading_rules` text DEFAULT NULL,
  `achievement_verify` text DEFAULT NULL,
  `graduation_criteria` text DEFAULT NULL,
  `achievement_verify_during` text DEFAULT NULL,
  `achievement_verify_after` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_evaluation_process`
--

CREATE TABLE `program_evaluation_process` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `section_no` varchar(20) NOT NULL,
  `content` text DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_faculty_development`
--

CREATE TABLE `program_faculty_development` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `section_no` varchar(20) NOT NULL,
  `activity` text DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_graduation_criteria`
--

CREATE TABLE `program_graduation_criteria` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `criterion` text NOT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_instructor`
--

CREATE TABLE `program_instructor` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `position` varchar(255) DEFAULT NULL,
  `degree` varchar(255) DEFAULT NULL,
  `branch` varchar(100) DEFAULT NULL,
  `research` text DEFAULT NULL,
  `load_now` decimal(8,2) DEFAULT NULL,
  `load_new` decimal(8,2) DEFAULT NULL,
  `instructor_type` enum('responsible','teaching','both') NOT NULL DEFAULT 'responsible',
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_learning_attribute`
--

CREATE TABLE `program_learning_attribute` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `category` varchar(50) NOT NULL,
  `outcomes` text DEFAULT NULL,
  `strategy` text DEFAULT NULL,
  `assessment` text DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_learning_dimension`
--

CREATE TABLE `program_learning_dimension` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `d1` text DEFAULT NULL,
  `d2` text DEFAULT NULL,
  `d3` text DEFAULT NULL,
  `d4` text DEFAULT NULL,
  `d5` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_learning_process`
--

CREATE TABLE `program_learning_process` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `edu_system` varchar(255) DEFAULT NULL,
  `summer_edu` text DEFAULT NULL,
  `credit_transfer` text DEFAULT NULL,
  `schedule` varchar(255) DEFAULT NULL,
  `freshman_issues` text DEFAULT NULL,
  `strategies` text DEFAULT NULL,
  `fieldwork` text DEFAULT NULL,
  `research_req` text DEFAULT NULL,
  `growth_mindset` text DEFAULT NULL,
  `real_world_learning` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_learning_topic`
--

CREATE TABLE `program_learning_topic` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `topic_no` varchar(20) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_major`
--

CREATE TABLE `program_major` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `major_name` varchar(255) NOT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_quality_section`
--

CREATE TABLE `program_quality_section` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `section_no` varchar(20) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_review`
--

CREATE TABLE `program_review` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `reviewer_id` int(10) UNSIGNED NOT NULL,
  `decision` enum('approved','rejected','comment') NOT NULL,
  `comment` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_schedule`
--

CREATE TABLE `program_schedule` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `semester_type` enum('semester1','semester2','summer') NOT NULL,
  `schedule_text` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_semester`
--

CREATE TABLE `program_semester` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `year` int(11) NOT NULL,
  `term` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `program_student_plan`
--

CREATE TABLE `program_student_plan` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `year_label` varchar(20) NOT NULL,
  `student_count` int(11) DEFAULT NULL,
  `graduate_count` int(11) DEFAULT NULL,
  `sort_order` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `quality_assurance`
--

CREATE TABLE `quality_assurance` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `std_grad` text DEFAULT NULL,
  `std_student` text DEFAULT NULL,
  `std_faculty` text DEFAULT NULL,
  `teaching_quality` text DEFAULT NULL,
  `learning_support` text DEFAULT NULL,
  `quality_plan` text DEFAULT NULL,
  `risk_mgmt` text DEFAULT NULL,
  `complaints` text DEFAULT NULL,
  `data_review` text DEFAULT NULL,
  `communication` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `quality_kpi`
--

CREATE TABLE `quality_kpi` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `kpi_name` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `y1` tinyint(1) NOT NULL DEFAULT 0,
  `y2` tinyint(1) NOT NULL DEFAULT 0,
  `y3` tinyint(1) NOT NULL DEFAULT 0,
  `y4` tinyint(1) NOT NULL DEFAULT 0,
  `y5` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(10) UNSIGNED NOT NULL,
  `email` varchar(255) NOT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `role` enum('admin','coordinator','reviewer') NOT NULL DEFAULT 'coordinator',
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `hashed_password`, `full_name`, `role`, `is_active`, `created_at`) VALUES
(1, 'th@th.com', '$2b$12$x9BPGJBSB/c9Vepy4ytMruNPty1r0a8xgwkAk4sJ/fIe1sorydGkq', 'thanakorn sertsai', 'admin', 1, '2026-07-18 17:38:35');

-- --------------------------------------------------------

--
-- Table structure for table `ylo`
--

CREATE TABLE `ylo` (
  `id` int(10) UNSIGNED NOT NULL,
  `program_id` int(10) UNSIGNED NOT NULL,
  `year` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `branch` varchar(100) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `course_category`
--
ALTER TABLE `course_category`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_course_category_program_id` (`program_id`);

--
-- Indexes for table `course_instructor`
--
ALTER TABLE `course_instructor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_course_instructor_program_id` (`program_id`),
  ADD KEY `idx_course_instructor_course_id` (`course_id`),
  ADD KEY `idx_course_instructor_instructor_id` (`instructor_id`);

--
-- Indexes for table `plo`
--
ALTER TABLE `plo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_plo_program_id` (`program_id`),
  ADD KEY `idx_plo_program_branch` (`program_id`,`branch`);

--
-- Indexes for table `plo_course_mapping`
--
ALTER TABLE `plo_course_mapping`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_plo_course_mapping` (`plo_id`,`course_id`),
  ADD KEY `idx_plo_course_mapping_program_id` (`program_id`),
  ADD KEY `idx_plo_course_mapping_course_id` (`course_id`);

--
-- Indexes for table `plo_tqf_mapping`
--
ALTER TABLE `plo_tqf_mapping`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_plo_tqf_mapping_program_id` (`program_id`),
  ADD KEY `idx_plo_tqf_mapping_plo_id` (`plo_id`);

--
-- Indexes for table `program`
--
ALTER TABLE `program`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_program_created_by` (`created_by`);

--
-- Indexes for table `program_admission`
--
ALTER TABLE `program_admission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `program_id` (`program_id`);

--
-- Indexes for table `program_approval`
--
ALTER TABLE `program_approval`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_approval_program_id` (`program_id`);

--
-- Indexes for table `program_budget_expense`
--
ALTER TABLE `program_budget_expense`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_budget_expense_program_id` (`program_id`);

--
-- Indexes for table `program_budget_income`
--
ALTER TABLE `program_budget_income`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_budget_income_program_id` (`program_id`);

--
-- Indexes for table `program_career`
--
ALTER TABLE `program_career`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_career_program_id` (`program_id`);

--
-- Indexes for table `program_course`
--
ALTER TABLE `program_course`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_program_course_branch` (`semester_id`,`course_id`,`branch`),
  ADD KEY `idx_program_course_semester_id` (`semester_id`),
  ADD KEY `idx_program_course_course_id` (`course_id`),
  ADD KEY `idx_program_course_category_id` (`category_id`);

--
-- Indexes for table `program_development_plan`
--
ALTER TABLE `program_development_plan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_development_plan_program_id` (`program_id`);

--
-- Indexes for table `program_elo_framework`
--
ALTER TABLE `program_elo_framework`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_program_elo_framework_program` (`program_id`);

--
-- Indexes for table `program_evaluation`
--
ALTER TABLE `program_evaluation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `program_id` (`program_id`);

--
-- Indexes for table `program_evaluation_process`
--
ALTER TABLE `program_evaluation_process`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_evaluation_process_program_id` (`program_id`);

--
-- Indexes for table `program_faculty_development`
--
ALTER TABLE `program_faculty_development`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_faculty_development_program_id` (`program_id`);

--
-- Indexes for table `program_graduation_criteria`
--
ALTER TABLE `program_graduation_criteria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_graduation_criteria_program_id` (`program_id`);

--
-- Indexes for table `program_instructor`
--
ALTER TABLE `program_instructor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_instructor_program_id` (`program_id`);

--
-- Indexes for table `program_learning_attribute`
--
ALTER TABLE `program_learning_attribute`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_learning_attribute_program_id` (`program_id`);

--
-- Indexes for table `program_learning_dimension`
--
ALTER TABLE `program_learning_dimension`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_program_learning_dimension_program` (`program_id`);

--
-- Indexes for table `program_learning_process`
--
ALTER TABLE `program_learning_process`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `program_id` (`program_id`);

--
-- Indexes for table `program_learning_topic`
--
ALTER TABLE `program_learning_topic`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_learning_topic_program_id` (`program_id`);

--
-- Indexes for table `program_major`
--
ALTER TABLE `program_major`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_major_program_id` (`program_id`);

--
-- Indexes for table `program_quality_section`
--
ALTER TABLE `program_quality_section`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_quality_section_program_id` (`program_id`);

--
-- Indexes for table `program_review`
--
ALTER TABLE `program_review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_review_program` (`program_id`),
  ADD KEY `fk_review_reviewer` (`reviewer_id`);

--
-- Indexes for table `program_schedule`
--
ALTER TABLE `program_schedule`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_program_schedule` (`program_id`,`semester_type`);

--
-- Indexes for table `program_semester`
--
ALTER TABLE `program_semester`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_program_semester` (`program_id`,`year`,`term`),
  ADD KEY `idx_program_semester_program_id` (`program_id`);

--
-- Indexes for table `program_student_plan`
--
ALTER TABLE `program_student_plan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_program_student_plan_program_id` (`program_id`);

--
-- Indexes for table `quality_assurance`
--
ALTER TABLE `quality_assurance`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `program_id` (`program_id`);

--
-- Indexes for table `quality_kpi`
--
ALTER TABLE `quality_kpi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_quality_kpi_program_id` (`program_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `ylo`
--
ALTER TABLE `ylo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_ylo_program_id` (`program_id`),
  ADD KEY `idx_ylo_program_branch_year` (`program_id`,`branch`,`year`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `course_category`
--
ALTER TABLE `course_category`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `course_instructor`
--
ALTER TABLE `course_instructor`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plo`
--
ALTER TABLE `plo`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plo_course_mapping`
--
ALTER TABLE `plo_course_mapping`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plo_tqf_mapping`
--
ALTER TABLE `plo_tqf_mapping`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program`
--
ALTER TABLE `program`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `program_admission`
--
ALTER TABLE `program_admission`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_approval`
--
ALTER TABLE `program_approval`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_budget_expense`
--
ALTER TABLE `program_budget_expense`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_budget_income`
--
ALTER TABLE `program_budget_income`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_career`
--
ALTER TABLE `program_career`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_course`
--
ALTER TABLE `program_course`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_development_plan`
--
ALTER TABLE `program_development_plan`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_elo_framework`
--
ALTER TABLE `program_elo_framework`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_evaluation`
--
ALTER TABLE `program_evaluation`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_evaluation_process`
--
ALTER TABLE `program_evaluation_process`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_faculty_development`
--
ALTER TABLE `program_faculty_development`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_graduation_criteria`
--
ALTER TABLE `program_graduation_criteria`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_instructor`
--
ALTER TABLE `program_instructor`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_learning_attribute`
--
ALTER TABLE `program_learning_attribute`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_learning_dimension`
--
ALTER TABLE `program_learning_dimension`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_learning_process`
--
ALTER TABLE `program_learning_process`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_learning_topic`
--
ALTER TABLE `program_learning_topic`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_major`
--
ALTER TABLE `program_major`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_quality_section`
--
ALTER TABLE `program_quality_section`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_review`
--
ALTER TABLE `program_review`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_schedule`
--
ALTER TABLE `program_schedule`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_semester`
--
ALTER TABLE `program_semester`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_student_plan`
--
ALTER TABLE `program_student_plan`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `quality_assurance`
--
ALTER TABLE `quality_assurance`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `quality_kpi`
--
ALTER TABLE `quality_kpi`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `ylo`
--
ALTER TABLE `ylo`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `course_category`
--
ALTER TABLE `course_category`
  ADD CONSTRAINT `fk_course_category_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `course_instructor`
--
ALTER TABLE `course_instructor`
  ADD CONSTRAINT `fk_course_instructor_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_course_instructor_instructor` FOREIGN KEY (`instructor_id`) REFERENCES `program_instructor` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_course_instructor_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `plo`
--
ALTER TABLE `plo`
  ADD CONSTRAINT `fk_plo_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `plo_course_mapping`
--
ALTER TABLE `plo_course_mapping`
  ADD CONSTRAINT `fk_plo_course_mapping_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_plo_course_mapping_plo` FOREIGN KEY (`plo_id`) REFERENCES `plo` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_plo_course_mapping_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `plo_tqf_mapping`
--
ALTER TABLE `plo_tqf_mapping`
  ADD CONSTRAINT `fk_plo_tqf_mapping_plo` FOREIGN KEY (`plo_id`) REFERENCES `plo` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_plo_tqf_mapping_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program`
--
ALTER TABLE `program`
  ADD CONSTRAINT `fk_program_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `program_admission`
--
ALTER TABLE `program_admission`
  ADD CONSTRAINT `fk_admission_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_approval`
--
ALTER TABLE `program_approval`
  ADD CONSTRAINT `fk_program_approval_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_budget_expense`
--
ALTER TABLE `program_budget_expense`
  ADD CONSTRAINT `fk_program_budget_expense_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_budget_income`
--
ALTER TABLE `program_budget_income`
  ADD CONSTRAINT `fk_program_budget_income_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_career`
--
ALTER TABLE `program_career`
  ADD CONSTRAINT `fk_program_career_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_course`
--
ALTER TABLE `program_course`
  ADD CONSTRAINT `fk_program_course_category` FOREIGN KEY (`category_id`) REFERENCES `course_category` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_program_course_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  ADD CONSTRAINT `fk_program_course_semester` FOREIGN KEY (`semester_id`) REFERENCES `program_semester` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_development_plan`
--
ALTER TABLE `program_development_plan`
  ADD CONSTRAINT `fk_program_development_plan_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_elo_framework`
--
ALTER TABLE `program_elo_framework`
  ADD CONSTRAINT `fk_program_elo_framework_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_evaluation`
--
ALTER TABLE `program_evaluation`
  ADD CONSTRAINT `fk_evaluation_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_evaluation_process`
--
ALTER TABLE `program_evaluation_process`
  ADD CONSTRAINT `fk_program_evaluation_process_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_faculty_development`
--
ALTER TABLE `program_faculty_development`
  ADD CONSTRAINT `fk_program_faculty_development_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_graduation_criteria`
--
ALTER TABLE `program_graduation_criteria`
  ADD CONSTRAINT `fk_program_graduation_criteria_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_instructor`
--
ALTER TABLE `program_instructor`
  ADD CONSTRAINT `fk_program_instructor_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_learning_attribute`
--
ALTER TABLE `program_learning_attribute`
  ADD CONSTRAINT `fk_program_learning_attribute_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_learning_dimension`
--
ALTER TABLE `program_learning_dimension`
  ADD CONSTRAINT `fk_program_learning_dimension_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_learning_process`
--
ALTER TABLE `program_learning_process`
  ADD CONSTRAINT `fk_learning_process_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_learning_topic`
--
ALTER TABLE `program_learning_topic`
  ADD CONSTRAINT `fk_program_learning_topic_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_major`
--
ALTER TABLE `program_major`
  ADD CONSTRAINT `fk_program_major_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_quality_section`
--
ALTER TABLE `program_quality_section`
  ADD CONSTRAINT `fk_program_quality_section_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_review`
--
ALTER TABLE `program_review`
  ADD CONSTRAINT `fk_review_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_review_reviewer` FOREIGN KEY (`reviewer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_schedule`
--
ALTER TABLE `program_schedule`
  ADD CONSTRAINT `fk_program_schedule_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_semester`
--
ALTER TABLE `program_semester`
  ADD CONSTRAINT `fk_program_semester_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_student_plan`
--
ALTER TABLE `program_student_plan`
  ADD CONSTRAINT `fk_program_student_plan_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `quality_assurance`
--
ALTER TABLE `quality_assurance`
  ADD CONSTRAINT `fk_quality_assurance_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `quality_kpi`
--
ALTER TABLE `quality_kpi`
  ADD CONSTRAINT `fk_quality_kpi_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `ylo`
--
ALTER TABLE `ylo`
  ADD CONSTRAINT `fk_ylo_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
