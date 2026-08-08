-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: mariadb:3306
-- Generation Time: Aug 08, 2026 at 11:43 AM
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
  `credit_selfstudy` int(11) DEFAULT NULL
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
  `sort_order` int(11) DEFAULT 0
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
  `sort_order` int(11) DEFAULT 0
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
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `program`
--

INSERT INTO `program` (`id`, `created_by`, `program_code`, `name_th`, `name_en`, `degree_name_th`, `degree_abbr_th`, `degree_name_en`, `degree_abbr_en`, `major`, `program_format`, `duration_years`, `program_category`, `language`, `admission_req`, `degree_granting`, `program_type`, `open_year`, `approval_details`, `status`, `philosophy`, `importance`, `objectives`, `uniqueness`, `careers`, `total_credits`, `created_at`, `updated_at`) VALUES
(2, NULL, '8900', 'asdf', 'jk', 'asdf', 'a', 'asdf', 'a', 'no', 'หลักสูตรระดับปริญญาตรี', 4.0, 'asdft', 'asdfy', 'asdfg', 'ให้ปริญญาเพียงสาขาวิชาเดียว', 'หลักสูตรใหม่', 'fg6678', 'asdfashafhadfhafh', 'draft', NULL, NULL, NULL, NULL, NULL, NULL, '2026-07-18 13:38:29', '2026-07-18 13:38:29'),
(3, 1, '', '', '', '', '', '', '', '', 'หลักสูตรระดับปริญญาตรี', NULL, '', '', '', 'ให้ปริญญาเพียงสาขาวิชาเดียว', 'หลักสูตรใหม่', '', '', 'draft', NULL, NULL, NULL, NULL, NULL, NULL, '2026-07-19 02:14:10', '2026-07-19 02:14:10');

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
-- Table structure for table `program_course`
--

CREATE TABLE `program_course` (
  `id` int(10) UNSIGNED NOT NULL,
  `semester_id` int(10) UNSIGNED NOT NULL,
  `course_id` varchar(20) NOT NULL,
  `sort_order` int(11) DEFAULT 0
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
  `graduation_criteria` text DEFAULT NULL
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
  `description` text DEFAULT NULL
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
  `description` text DEFAULT NULL
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
-- Indexes for table `plo`
--
ALTER TABLE `plo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_plo_program_id` (`program_id`);

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
-- Indexes for table `program_course`
--
ALTER TABLE `program_course`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_program_course` (`semester_id`,`course_id`),
  ADD KEY `idx_program_course_semester_id` (`semester_id`),
  ADD KEY `idx_program_course_course_id` (`course_id`);

--
-- Indexes for table `program_evaluation`
--
ALTER TABLE `program_evaluation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `program_id` (`program_id`);

--
-- Indexes for table `program_learning_process`
--
ALTER TABLE `program_learning_process`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `program_id` (`program_id`);

--
-- Indexes for table `program_review`
--
ALTER TABLE `program_review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_review_program` (`program_id`),
  ADD KEY `fk_review_reviewer` (`reviewer_id`);

--
-- Indexes for table `program_semester`
--
ALTER TABLE `program_semester`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_program_semester` (`program_id`,`year`,`term`),
  ADD KEY `idx_program_semester_program_id` (`program_id`);

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
  ADD KEY `idx_ylo_program_id` (`program_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `course_category`
--
ALTER TABLE `course_category`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plo`
--
ALTER TABLE `plo`
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
-- AUTO_INCREMENT for table `program_course`
--
ALTER TABLE `program_course`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_evaluation`
--
ALTER TABLE `program_evaluation`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_learning_process`
--
ALTER TABLE `program_learning_process`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_review`
--
ALTER TABLE `program_review`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_semester`
--
ALTER TABLE `program_semester`
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
-- Constraints for table `plo`
--
ALTER TABLE `plo`
  ADD CONSTRAINT `fk_plo_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

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
-- Constraints for table `program_course`
--
ALTER TABLE `program_course`
  ADD CONSTRAINT `fk_program_course_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`),
  ADD CONSTRAINT `fk_program_course_semester` FOREIGN KEY (`semester_id`) REFERENCES `program_semester` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_evaluation`
--
ALTER TABLE `program_evaluation`
  ADD CONSTRAINT `fk_evaluation_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_learning_process`
--
ALTER TABLE `program_learning_process`
  ADD CONSTRAINT `fk_learning_process_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_review`
--
ALTER TABLE `program_review`
  ADD CONSTRAINT `fk_review_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_review_reviewer` FOREIGN KEY (`reviewer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `program_semester`
--
ALTER TABLE `program_semester`
  ADD CONSTRAINT `fk_program_semester_program` FOREIGN KEY (`program_id`) REFERENCES `program` (`id`) ON DELETE CASCADE;

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
