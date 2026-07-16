-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 13, 2026 at 03:50 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `curriculum`
--

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `course_id` int(11) NOT NULL,
  `course_code` varchar(20) NOT NULL,
  `name_th` varchar(200) NOT NULL,
  `name_en` varchar(200) NOT NULL,
  `total_credits` int(11) NOT NULL,
  `lecture_hours` int(11) NOT NULL,
  `lab_hours` int(11) NOT NULL,
  `self_study_hours` int(11) NOT NULL,
  `taugh_in_eng` tinyint(1) NOT NULL,
  `description_th` text NOT NULL,
  `description_en` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`course_id`, `course_code`, `name_th`, `name_en`, `total_credits`, `lecture_hours`, `lab_hours`, `self_study_hours`, `taugh_in_eng`, `description_th`, `description_en`) VALUES
(1, '010203101', 'การเขียนโปรแกรมสำหรับระบบสมองกลฝังตัว', 'Programming for Embedded Systems', 3, 2, 3, 6, 1, 'ศึกษาการเขียนโปรแกรมระบบสมองกลฝังตัว', 'Study embedded systems programming'),
(2, '010203102', 'การออกแบบวงจรดิจิทัล', 'Digital Circuit Design', 3, 2, 3, 6, 1, 'ศึกษาการออกแบบวงจรดิจิทัล', 'Study digital circuit design'),
(3, '010203103', 'ไมโครคอนโทรลเลอร์', 'Microcontroller', 3, 2, 3, 6, 1, 'ศึกษาการใช้งานไมโครคอนโทรลเลอร์', 'Study microcontroller applications'),
(4, '010203101', 'การเขียนโปรแกรมสำหรับระบบสมองกลฝังตัว', 'Programming for Embedded Systems', 3, 2, 3, 6, 1, 'ศึกษาการเขียนโปรแกรมระบบสมองกลฝังตัว', 'Study embedded systems programming'),
(5, '010203102', 'การออกแบบวงจรดิจิทัล', 'Digital Circuit Design', 3, 2, 3, 6, 1, 'ศึกษาการออกแบบวงจรดิจิทัล', 'Study digital circuit design'),
(6, '010203103', 'ไมโครคอนโทรลเลอร์', 'Microcontroller', 3, 2, 3, 6, 1, 'ศึกษาการใช้งานไมโครคอนโทรลเลอร์', 'Study microcontroller applications');

-- --------------------------------------------------------

--
-- Table structure for table `course_category`
--

CREATE TABLE `course_category` (
  `category_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `parent_category_id` int(11) NOT NULL,
  `name_th` varchar(200) NOT NULL,
  `name_en` varchar(200) NOT NULL,
  `require_credits` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course_category`
--

INSERT INTO `course_category` (`category_id`, `program_id`, `parent_category_id`, `name_th`, `name_en`, `require_credits`) VALUES
(1, 1, 0, 'หมวดศึกษาทั่วไป', 'General Education', 30),
(2, 1, 0, 'หมวดวิชาเฉพาะ', 'Core Courses', 84),
(3, 1, 0, 'หมวดวิชาเลือกเสรี', 'Free Elective', 6),
(4, 1, 0, 'หมวดศึกษาทั่วไป', 'General Education', 30),
(5, 1, 0, 'หมวดวิชาเฉพาะ', 'Core Courses', 84),
(6, 1, 0, 'หมวดวิชาเลือกเสรี', 'Free Elective', 6),
(7, 1, 0, 'หมวดศึกษาทั่วไป', 'General Education', 30),
(8, 1, 0, 'หมวดวิชาเฉพาะ', 'Core Courses', 84),
(9, 1, 0, 'หมวดวิชาเลือกเสรี', 'Free Elective', 6);

-- --------------------------------------------------------

--
-- Table structure for table `course_instructor`
--

CREATE TABLE `course_instructor` (
  `id` int(11) NOT NULL,
  `program_course_id` int(11) NOT NULL,
  `instructor_id` int(11) NOT NULL,
  `academic_year` varchar(2) NOT NULL,
  `semester` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `course_plo`
--

CREATE TABLE `course_plo` (
  `id` int(11) NOT NULL,
  `program_course_id` int(11) NOT NULL,
  `plo_id` int(11) NOT NULL,
  `responsibility_level` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course_plo`
--

INSERT INTO `course_plo` (`id`, `program_course_id`, `plo_id`, `responsibility_level`) VALUES
(1, 1, 1, 'High'),
(2, 1, 3, 'Medium'),
(3, 2, 2, 'High'),
(4, 3, 3, 'High'),
(5, 1, 1, 'High'),
(6, 1, 3, 'Medium'),
(7, 2, 2, 'High'),
(8, 3, 3, 'High');

-- --------------------------------------------------------

--
-- Table structure for table `instructor`
--

CREATE TABLE `instructor` (
  `instructor_id` int(11) NOT NULL,
  `employee_id` varchar(20) NOT NULL,
  `full_name_th` int(200) NOT NULL,
  `full_name_en` int(200) NOT NULL,
  `position` varchar(100) NOT NULL,
  `academic_rank` text NOT NULL,
  `highest_degree` text NOT NULL,
  `degree_field` text NOT NULL,
  `email` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`instructor_id`, `employee_id`, `full_name_th`, `full_name_en`, `position`, `academic_rank`, `highest_degree`, `degree_field`, `email`) VALUES
(1, 'EMP001', 0, 0, 'Lecturer', 'Assistant Professor', 'Ph.D.', 'Embedded Systems Engineering', 'somchai@kmutnb.ac.th'),
(2, 'EMP001', 0, 0, 'Lecturer', 'Assistant Professor', 'Ph.D.', 'Embedded Systems Engineering', 'somchai@kmutnb.ac.th');

-- --------------------------------------------------------

--
-- Table structure for table `peo`
--

CREATE TABLE `peo` (
  `peo_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `peo_code` varchar(20) NOT NULL,
  `description_th` text NOT NULL,
  `descripition_en` text NOT NULL,
  `sequence_no` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `peo`
--

INSERT INTO `peo` (`peo_id`, `program_id`, `peo_code`, `description_th`, `descripition_en`, `sequence_no`) VALUES
(1, 1, 'PEO1', 'สามารถประยุกต์ใช้ความรู้ด้านระบบสมองกลฝังตัวและการออกแบบอิเล็กทรอนิกส์ในงานวิชาชีพ', 'Apply embedded systems and electronics design knowledge professionally', 1),
(2, 1, 'PEO2', 'มีความเชี่ยวชาญด้านการออกแบบวงจรอิเล็กทรอนิกส์', 'Expertise in electronic circuit design', 2),
(3, 1, 'PEO3', 'สามารถวิเคราะห์และแก้ปัญหาระบบสมองกลฝังตัวได้', 'Analyze and solve embedded system problems', 3),
(4, 1, 'PEO1', 'สามารถประยุกต์ใช้ความรู้ด้านระบบสมองกลฝังตัวและการออกแบบอิเล็กทรอนิกส์ในงานวิชาชีพ', 'Apply embedded systems and electronics design knowledge professionally', 1),
(5, 1, 'PEO2', 'มีความเชี่ยวชาญด้านการออกแบบวงจรอิเล็กทรอนิกส์', 'Expertise in electronic circuit design', 2),
(6, 1, 'PEO3', 'สามารถวิเคราะห์และแก้ปัญหาระบบสมองกลฝังตัวได้', 'Analyze and solve embedded system problems', 3),
(7, 1, 'PEO1', 'สามารถประยุกต์ใช้ความรู้ด้านระบบสมองกลฝังตัวและการออกแบบอิเล็กทรอนิกส์ในงานวิชาชีพ', 'Apply embedded systems and electronics design knowledge professionally', 1),
(8, 1, 'PEO2', 'มีความเชี่ยวชาญด้านการออกแบบวงจรอิเล็กทรอนิกส์', 'Expertise in electronic circuit design', 2),
(9, 1, 'PEO3', 'สามารถวิเคราะห์และแก้ปัญหาระบบสมองกลฝังตัวได้', 'Analyze and solve embedded system problems', 3),
(10, 1, 'PEO1', 'สามารถประยุกต์ใช้ความรู้ด้านระบบสมองกลฝังตัวและการออกแบบอิเล็กทรอนิกส์ในงานวิชาชีพ', 'Apply embedded systems and electronics design knowledge professionally', 1),
(11, 1, 'PEO2', 'มีความเชี่ยวชาญด้านการออกแบบวงจรอิเล็กทรอนิกส์', 'Expertise in electronic circuit design', 2),
(12, 1, 'PEO3', 'สามารถวิเคราะห์และแก้ปัญหาระบบสมองกลฝังตัวได้', 'Analyze and solve embedded system problems', 3);

-- --------------------------------------------------------

--
-- Table structure for table `peo_plo`
--

CREATE TABLE `peo_plo` (
  `id` int(11) NOT NULL,
  `peo_id` int(11) NOT NULL,
  `plo_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `peo_plo`
--

INSERT INTO `peo_plo` (`id`, `peo_id`, `plo_id`) VALUES
(1, 1, 1),
(2, 1, 3),
(3, 2, 2),
(4, 3, 4),
(5, 1, 1),
(6, 1, 3),
(7, 2, 2),
(8, 3, 4);

-- --------------------------------------------------------

--
-- Table structure for table `plo`
--

CREATE TABLE `plo` (
  `plo_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `plo_code` varchar(20) NOT NULL,
  `plo_type` varchar(20) NOT NULL,
  `descripition_en` text NOT NULL,
  `descripition_th` text NOT NULL,
  `sequence_no` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `plo`
--

INSERT INTO `plo` (`plo_id`, `program_id`, `plo_code`, `plo_type`, `descripition_en`, `descripition_th`, `sequence_no`) VALUES
(1, 1, 'PLO1', 'S', 'Solve engineering problems using mathematics and engineering knowledge', 'แก้ปัญหาทางวิศวกรรมโดยใช้คณิตศาสตร์และวิศวกรรม', 1),
(2, 1, 'PLO2', 'S', 'Design analog and digital electronic circuits', 'ออกแบบวงจรอิเล็กทรอนิกส์แบบแอนะล็อกและดิจิทัล', 2),
(3, 1, 'PLO3', 'S', 'Develop embedded system software', 'พัฒนาซอฟต์แวร์ระบบสมองกลฝังตัว', 3),
(4, 1, 'PLO4', 'G', 'Communicate effectively in Thai and English', 'สื่อสารได้อย่างมีประสิทธิภาพทั้งภาษาไทยและอังกฤษ', 4),
(5, 1, 'PLO1', 'S', 'Solve engineering problems using mathematics and engineering knowledge', 'แก้ปัญหาทางวิศวกรรมโดยใช้คณิตศาสตร์และวิศวกรรม', 1),
(6, 1, 'PLO2', 'S', 'Design analog and digital electronic circuits', 'ออกแบบวงจรอิเล็กทรอนิกส์แบบแอนะล็อกและดิจิทัล', 2),
(7, 1, 'PLO3', 'S', 'Develop embedded system software', 'พัฒนาซอฟต์แวร์ระบบสมองกลฝังตัว', 3),
(8, 1, 'PLO4', 'G', 'Communicate effectively in Thai and English', 'สื่อสารได้อย่างมีประสิทธิภาพทั้งภาษาไทยและอังกฤษ', 4),
(9, 1, 'PLO1', 'S', 'Solve engineering problems using mathematics and engineering knowledge', 'แก้ปัญหาทางวิศวกรรมโดยใช้คณิตศาสตร์และวิศวกรรม', 1),
(10, 1, 'PLO2', 'S', 'Design analog and digital electronic circuits', 'ออกแบบวงจรอิเล็กทรอนิกส์แบบแอนะล็อกและดิจิทัล', 2),
(11, 1, 'PLO3', 'S', 'Develop embedded system software', 'พัฒนาซอฟต์แวร์ระบบสมองกลฝังตัว', 3),
(12, 1, 'PLO4', 'G', 'Communicate effectively in Thai and English', 'สื่อสารได้อย่างมีประสิทธิภาพทั้งภาษาไทยและอังกฤษ', 4),
(13, 1, 'PLO1', 'S', 'Solve engineering problems using mathematics and engineering knowledge', 'แก้ปัญหาทางวิศวกรรมโดยใช้คณิตศาสตร์และวิศวกรรม', 1),
(14, 1, 'PLO2', 'S', 'Design analog and digital electronic circuits', 'ออกแบบวงจรอิเล็กทรอนิกส์แบบแอนะล็อกและดิจิทัล', 2),
(15, 1, 'PLO3', 'S', 'Develop embedded system software', 'พัฒนาซอฟต์แวร์ระบบสมองกลฝังตัว', 3),
(16, 1, 'PLO4', 'G', 'Communicate effectively in Thai and English', 'สื่อสารได้อย่างมีประสิทธิภาพทั้งภาษาไทยและอังกฤษ', 4);

-- --------------------------------------------------------

--
-- Table structure for table `plo_ylo`
--

CREATE TABLE `plo_ylo` (
  `id` int(11) NOT NULL,
  `ylo_id` int(11) NOT NULL,
  `plo_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `plo_ylo`
--

INSERT INTO `plo_ylo` (`id`, `ylo_id`, `plo_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 1, 1),
(5, 2, 2),
(6, 3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `prerequisite`
--

CREATE TABLE `prerequisite` (
  `prereq_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `prereq_course_id` int(11) NOT NULL,
  `condition_type` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prerequisite`
--

INSERT INTO `prerequisite` (`prereq_id`, `course_id`, `prereq_course_id`, `condition_type`) VALUES
(1, 2, 1, 'PASS'),
(2, 3, 1, 'PASS');

-- --------------------------------------------------------

--
-- Table structure for table `program`
--

CREATE TABLE `program` (
  `program_id` int(11) NOT NULL,
  `program_code` varchar(20) NOT NULL,
  `name_th` varchar(200) NOT NULL,
  `name_en` varchar(200) NOT NULL,
  `degree_name_th` varchar(100) NOT NULL,
  `degree_name_en` varchar(100) NOT NULL,
  `faculty` varchar(100) NOT NULL,
  `department` varchar(100) NOT NULL,
  `total_credits` int(11) NOT NULL,
  `duration_years` varchar(20) NOT NULL,
  `satatus` varchar(20) NOT NULL,
  `Approved_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `program`
--

INSERT INTO `program` (`program_id`, `program_code`, `name_th`, `name_en`, `degree_name_th`, `degree_name_en`, `faculty`, `department`, `total_credits`, `duration_years`, `satatus`, `Approved_date`) VALUES
(1, 'ESED2568', 'ระบบสมองกลฝังตัวและการออกแบบอิเล็กทรอนิกส์', 'Embedded System and Electronics Design', 'วิศวกรรมศาสตรบัณฑิต', 'Bachelor of Engineering', 'College of Industrial Technology', 'Department of Electronic Engineering Technology', 132, '4 Years', 'ACTIVE', '2025-02-26'),
(2, 'ESED2568', 'ระบบสมองกลฝังตัวและการออกแบบอิเล็กทรอนิกส์', 'Embedded System and Electronics Design', 'วิศวกรรมศาสตรบัณฑิต', 'Bachelor of Engineering', 'College of Industrial Technology', 'Department of Electronic Engineering Technology', 132, '4 Years', 'ACTIVE', '2025-02-26'),
(3, 'ESED2568', 'ระบบสมองกลฝังตัวและการออกแบบอิเล็กทรอนิกส์', 'Embedded System and Electronics Design', 'วิศวกรรมศาสตรบัณฑิต', 'Bachelor of Engineering', 'College of Industrial Technology', 'Department of Electronic Engineering Technology', 132, '4 Years', 'ACTIVE', '2025-02-26'),
(4, 'ESED2568', 'ระบบสมองกลฝังตัวและการออกแบบอิเล็กทรอนิกส์', 'Embedded System and Electronics Design', 'วิศวกรรมศาสตรบัณฑิต', 'Bachelor of Engineering', 'College of Industrial Technology', 'Department of Electronic Engineering Technology', 132, '4 Years', 'ACTIVE', '2025-02-26');

-- --------------------------------------------------------

--
-- Table structure for table `program_course`
--

CREATE TABLE `program_course` (
  `program_course_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `is_required` int(11) NOT NULL,
  `year_offered` int(11) NOT NULL,
  `semester_offered` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `program_course`
--

INSERT INTO `program_course` (`program_course_id`, `program_id`, `course_id`, `category_id`, `is_required`, `year_offered`, `semester_offered`) VALUES
(1, 1, 1, 2, 1, 1, 1),
(2, 1, 2, 2, 1, 1, 2),
(3, 1, 3, 2, 1, 2, 1),
(4, 1, 1, 2, 1, 1, 1),
(5, 1, 2, 2, 1, 1, 2),
(6, 1, 3, 2, 1, 2, 1);

-- --------------------------------------------------------

--
-- Table structure for table `program_instructor`
--

CREATE TABLE `program_instructor` (
  `id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `instructor_id` int(11) NOT NULL,
  `role` varchar(30) NOT NULL,
  `is_coordinator` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `program_instructor`
--

INSERT INTO `program_instructor` (`id`, `program_id`, `instructor_id`, `role`, `is_coordinator`) VALUES
(1, 1, 1, 'Program Committee', 1),
(2, 1, 1, 'Program Committee', 1);

-- --------------------------------------------------------

--
-- Table structure for table `quality_kpi`
--

CREATE TABLE `quality_kpi` (
  `kpi_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `kpi_code` varchar(50) NOT NULL,
  `kpi_name` varchar(100) NOT NULL,
  `kpi_category` varchar(50) NOT NULL,
  `taget_value` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `quality_kpi`
--

INSERT INTO `quality_kpi` (`kpi_id`, `program_id`, `kpi_code`, `kpi_name`, `kpi_category`, `taget_value`) VALUES
(1, 1, 'KPI001', 'Graduate Employment Rate', 'Employment', '80%'),
(2, 1, 'KPI002', 'Student Satisfaction', 'Education Quality', '85%');

-- --------------------------------------------------------

--
-- Table structure for table `student_intake`
--

CREATE TABLE `student_intake` (
  `intake_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `academic_year` int(11) NOT NULL,
  `planned_intake` int(11) NOT NULL,
  `actual_intake` int(11) NOT NULL,
  `planned_graduate` int(11) NOT NULL,
  `actual_graduate` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_intake`
--

INSERT INTO `student_intake` (`intake_id`, `program_id`, `academic_year`, `planned_intake`, `actual_intake`, `planned_graduate`, `actual_graduate`) VALUES
(1, 1, 2025, 60, 55, 50, 48),
(2, 1, 2025, 60, 55, 50, 48);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `uid` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`uid`, `username`, `password`, `role`) VALUES
(1, 'admin', '1234', 'editor'),
(2, 'admin2', '1235', 'coeditor');

-- --------------------------------------------------------

--
-- Table structure for table `ylo`
--

CREATE TABLE `ylo` (
  `ylo_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `ylo_code` varchar(20) NOT NULL,
  `year_level` int(11) NOT NULL,
  `descripition_en` text NOT NULL,
  `descripition_th` text NOT NULL,
  `sequence_no` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ylo`
--

INSERT INTO `ylo` (`ylo_id`, `program_id`, `ylo_code`, `year_level`, `descripition_en`, `descripition_th`, `sequence_no`) VALUES
(1, 1, 'YLO1', 1, 'Basic programming and electronics knowledge', 'มีพื้นฐานการเขียนโปรแกรมและอิเล็กทรอนิกส์', 1),
(2, 1, 'YLO2', 2, 'Design embedded and electronic systems', 'สามารถออกแบบระบบสมองกลฝังตัวได้', 2),
(3, 1, 'YLO3', 3, 'Develop IoT systems', 'สามารถพัฒนาระบบ IoT ได้', 3),
(4, 1, 'YLO1', 1, 'Basic programming and electronics knowledge', 'มีพื้นฐานการเขียนโปรแกรมและอิเล็กทรอนิกส์', 1),
(5, 1, 'YLO2', 2, 'Design embedded and electronic systems', 'สามารถออกแบบระบบสมองกลฝังตัวได้', 2),
(6, 1, 'YLO3', 3, 'Develop IoT systems', 'สามารถพัฒนาระบบ IoT ได้', 3),
(7, 1, 'YLO1', 1, 'Basic programming and electronics knowledge', 'มีพื้นฐานการเขียนโปรแกรมและอิเล็กทรอนิกส์', 1),
(8, 1, 'YLO2', 2, 'Design embedded and electronic systems', 'สามารถออกแบบระบบสมองกลฝังตัวได้', 2),
(9, 1, 'YLO3', 3, 'Develop IoT systems', 'สามารถพัฒนาระบบ IoT ได้', 3),
(10, 1, 'YLO1', 1, 'Basic programming and electronics knowledge', 'มีพื้นฐานการเขียนโปรแกรมและอิเล็กทรอนิกส์', 1),
(11, 1, 'YLO2', 2, 'Design embedded and electronic systems', 'สามารถออกแบบระบบสมองกลฝังตัวได้', 2),
(12, 1, 'YLO3', 3, 'Develop IoT systems', 'สามารถพัฒนาระบบ IoT ได้', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`course_id`);

--
-- Indexes for table `course_category`
--
ALTER TABLE `course_category`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `course_instructor`
--
ALTER TABLE `course_instructor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fkpc` (`program_course_id`),
  ADD KEY `fin` (`instructor_id`);

--
-- Indexes for table `course_plo`
--
ALTER TABLE `course_plo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk13` (`program_course_id`),
  ADD KEY `fk14` (`plo_id`);

--
-- Indexes for table `instructor`
--
ALTER TABLE `instructor`
  ADD PRIMARY KEY (`instructor_id`);

--
-- Indexes for table `peo`
--
ALTER TABLE `peo`
  ADD PRIMARY KEY (`peo_id`),
  ADD KEY `fk` (`program_id`);

--
-- Indexes for table `peo_plo`
--
ALTER TABLE `peo_plo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk2` (`plo_id`),
  ADD KEY `fk3` (`peo_id`);

--
-- Indexes for table `plo`
--
ALTER TABLE `plo`
  ADD PRIMARY KEY (`plo_id`),
  ADD KEY `fk4` (`program_id`);

--
-- Indexes for table `plo_ylo`
--
ALTER TABLE `plo_ylo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk6` (`plo_id`),
  ADD KEY `fk7` (`ylo_id`);

--
-- Indexes for table `prerequisite`
--
ALTER TABLE `prerequisite`
  ADD PRIMARY KEY (`prereq_id`),
  ADD KEY `fk9` (`course_id`);

--
-- Indexes for table `program`
--
ALTER TABLE `program`
  ADD PRIMARY KEY (`program_id`);

--
-- Indexes for table `program_course`
--
ALTER TABLE `program_course`
  ADD PRIMARY KEY (`program_course_id`),
  ADD KEY `fk10` (`program_id`),
  ADD KEY `fk11` (`course_id`),
  ADD KEY `fk12` (`category_id`);

--
-- Indexes for table `program_instructor`
--
ALTER TABLE `program_instructor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fkp` (`program_id`),
  ADD KEY `fki` (`instructor_id`);

--
-- Indexes for table `quality_kpi`
--
ALTER TABLE `quality_kpi`
  ADD PRIMARY KEY (`kpi_id`),
  ADD KEY `fk8` (`program_id`);

--
-- Indexes for table `student_intake`
--
ALTER TABLE `student_intake`
  ADD PRIMARY KEY (`intake_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`uid`);

--
-- Indexes for table `ylo`
--
ALTER TABLE `ylo`
  ADD PRIMARY KEY (`ylo_id`),
  ADD KEY `fk5` (`program_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `course`
--
ALTER TABLE `course`
  MODIFY `course_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `course_category`
--
ALTER TABLE `course_category`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `course_instructor`
--
ALTER TABLE `course_instructor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `course_plo`
--
ALTER TABLE `course_plo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `instructor`
--
ALTER TABLE `instructor`
  MODIFY `instructor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `peo`
--
ALTER TABLE `peo`
  MODIFY `peo_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `peo_plo`
--
ALTER TABLE `peo_plo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `plo`
--
ALTER TABLE `plo`
  MODIFY `plo_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `plo_ylo`
--
ALTER TABLE `plo_ylo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `prerequisite`
--
ALTER TABLE `prerequisite`
  MODIFY `prereq_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `program`
--
ALTER TABLE `program`
  MODIFY `program_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `program_course`
--
ALTER TABLE `program_course`
  MODIFY `program_course_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `program_instructor`
--
ALTER TABLE `program_instructor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `quality_kpi`
--
ALTER TABLE `quality_kpi`
  MODIFY `kpi_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `student_intake`
--
ALTER TABLE `student_intake`
  MODIFY `intake_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `ylo`
--
ALTER TABLE `ylo`
  MODIFY `ylo_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `course_instructor`
--
ALTER TABLE `course_instructor`
  ADD CONSTRAINT `fin` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`instructor_id`),
  ADD CONSTRAINT `fkpc` FOREIGN KEY (`program_course_id`) REFERENCES `program_course` (`program_course_id`);

--
-- Constraints for table `course_plo`
--
ALTER TABLE `course_plo`
  ADD CONSTRAINT `fk13` FOREIGN KEY (`program_course_id`) REFERENCES `program_course` (`program_course_id`),
  ADD CONSTRAINT `fk14` FOREIGN KEY (`plo_id`) REFERENCES `plo` (`plo_id`);

--
-- Constraints for table `peo`
--
ALTER TABLE `peo`
  ADD CONSTRAINT `fk` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`);

--
-- Constraints for table `peo_plo`
--
ALTER TABLE `peo_plo`
  ADD CONSTRAINT `fk2` FOREIGN KEY (`plo_id`) REFERENCES `plo` (`plo_id`),
  ADD CONSTRAINT `fk3` FOREIGN KEY (`peo_id`) REFERENCES `peo` (`peo_id`);

--
-- Constraints for table `plo`
--
ALTER TABLE `plo`
  ADD CONSTRAINT `fk4` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`);

--
-- Constraints for table `plo_ylo`
--
ALTER TABLE `plo_ylo`
  ADD CONSTRAINT `fk6` FOREIGN KEY (`plo_id`) REFERENCES `plo` (`plo_id`),
  ADD CONSTRAINT `fk7` FOREIGN KEY (`ylo_id`) REFERENCES `ylo` (`ylo_id`);

--
-- Constraints for table `prerequisite`
--
ALTER TABLE `prerequisite`
  ADD CONSTRAINT `fk9` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`);

--
-- Constraints for table `program_course`
--
ALTER TABLE `program_course`
  ADD CONSTRAINT `fk10` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`),
  ADD CONSTRAINT `fk11` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`),
  ADD CONSTRAINT `fk12` FOREIGN KEY (`category_id`) REFERENCES `course_category` (`category_id`);

--
-- Constraints for table `program_instructor`
--
ALTER TABLE `program_instructor`
  ADD CONSTRAINT `fki` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`instructor_id`),
  ADD CONSTRAINT `fkp` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`);

--
-- Constraints for table `quality_kpi`
--
ALTER TABLE `quality_kpi`
  ADD CONSTRAINT `fk8` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`);

--
-- Constraints for table `ylo`
--
ALTER TABLE `ylo`
  ADD CONSTRAINT `fk5` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
