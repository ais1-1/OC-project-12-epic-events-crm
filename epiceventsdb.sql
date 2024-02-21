-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 21, 2024 at 11:05 AM
-- Server version: 10.11.5-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `epiceventsdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `authentication_user`
--

CREATE TABLE `authentication_user` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `joined_date` date DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `role_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `authentication_user`
--

INSERT INTO `authentication_user` (`id`, `password`, `last_login`, `is_superuser`, `email`, `first_name`, `last_name`, `is_active`, `is_staff`, `joined_date`, `created_date`, `role_id`) VALUES
(1, 'pbkdf2_sha256$720000$7oRkTpNVok5d9NWrmDg5mh$HXyScqZY+8i/JJO0LqFHIRh42538QDQXhROrezYdeXY=', '2024-02-12 10:51:43.679685', 1, 'epic@management.com', 'Epic', 'MANAGER', 1, 1, '2020-01-02', '2024-01-31 10:32:04.488644', 1),
(3, 'pbkdf2_sha256$720000$KCI4SS9iSDeeDxi5qUb2Qo$sdXjxIBYUhsbkI5yiUD9YPYd+pgUm4/xXH536T6HPf0=', NULL, 0, 'john@smith.com', 'John', 'SMITH', 1, 1, NULL, '2024-01-31 13:03:19.884189', 2),
(6, 'pbkdf2_sha256$720000$5Qq6GQ7HlPF1cOmjxMZ0ze$imKFj2TZOIO8C0F8lSWuOKOOHtC+9DQACUdKfba1xi4=', NULL, 0, 'konqui@test.com', 'Konqui', 'KIKI', 1, 1, '2024-01-02', '2024-02-02 15:23:11.779725', 3),
(8, 'pbkdf2_sha256$720000$IknK7DYBnCW1MFhyjDVcyg$c2GH/X4o43DSWT/YT8RGFEKAvyrOAFRAitrIhcVuJsU=', NULL, 0, 'marie@sales.com', 'Marie', 'LEELU', 1, 1, NULL, '2024-02-07 08:40:40.766679', 2),
(17, 'pbkdf2_sha256$720000$04ZiEGEdyIz2slLyIzMWPi$EIOyRV2atic6SyFNo9kdnQpNQu+J4zzMaq5+iJrFfco=', NULL, 0, 'test@create.com', 'Test', 'TESTEUR', 1, 1, NULL, '2024-02-12 19:50:55.825458', 3),
(20, 'pbkdf2_sha256$720000$qvJzzGQWWGAExLeEd91iq3$c8GOQb+Q9PTKGlHGE/Z6OmCMjJlWCfJmxlsNgV+43pc=', '2024-02-14 21:05:42.490186', 1, 'staff@management.com', 'Epic', 'Admin', 1, 1, NULL, '2024-02-14 21:04:58.733827', 1),
(22, 'pbkdf2_sha256$720000$1B65m3pzguHGY7BrOlYk1Z$lHXKLQLJoqlx91blPv93Wm+6sgZk5pscsswUGRlfBJs=', NULL, 0, 'staff@support.com', 'Rick', 'MORTY', 1, 1, NULL, '2024-02-15 14:33:17.970914', 3);

-- --------------------------------------------------------

--
-- Table structure for table `authentication_user_groups`
--

CREATE TABLE `authentication_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `authentication_user_user_permissions`
--

CREATE TABLE `authentication_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `authtoken_token`
--

INSERT INTO `authtoken_token` (`key`, `created`, `user_id`) VALUES
('3f85b1e684ec15ea1377aeadd71b995894100eab', '2024-02-21 09:41:03.595755', 8),
('637e5be67b5269b81363384d89beaf14ecdd937d', '2024-02-20 19:45:54.427749', 1),
('9f2ca32a1da39d95fe7a13263604a85bb0dba244', '2024-02-15 10:22:31.257394', 6),
('a0628758179faaded8abb66886f3b1eeb8469e68', '2024-02-12 20:26:45.896493', 17),
('a81793a08325ba22af31fff9d8504c83b6f83dbe', '2024-02-19 15:33:40.928126', 3),
('b1859efeda57cc153832e7ff7ad187ec3d99c9a5', '2024-02-21 10:32:19.319645', 22);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Team', 6, 'add_team'),
(22, 'Can change Team', 6, 'change_team'),
(23, 'Can delete Team', 6, 'delete_team'),
(24, 'Can view Team', 6, 'view_team'),
(25, 'Can add user', 7, 'add_user'),
(26, 'Can change user', 7, 'change_user'),
(27, 'Can delete user', 7, 'delete_user'),
(28, 'Can view user', 7, 'view_user'),
(29, 'Can add Client', 8, 'add_client'),
(30, 'Can change Client', 8, 'change_client'),
(31, 'Can delete Client', 8, 'delete_client'),
(32, 'Can view Client', 8, 'view_client'),
(33, 'Can add Contract', 9, 'add_contract'),
(34, 'Can change Contract', 9, 'change_contract'),
(35, 'Can delete Contract', 9, 'delete_contract'),
(36, 'Can view Contract', 9, 'view_contract'),
(37, 'Can add Event', 10, 'add_event'),
(38, 'Can change Event', 10, 'change_event'),
(39, 'Can delete Event', 10, 'delete_event'),
(40, 'Can view Event', 10, 'view_event'),
(41, 'Can add Token', 11, 'add_token'),
(42, 'Can change Token', 11, 'change_token'),
(43, 'Can delete Token', 11, 'delete_token'),
(44, 'Can view Token', 11, 'view_token'),
(45, 'Can add token', 12, 'add_tokenproxy'),
(46, 'Can change token', 12, 'change_tokenproxy'),
(47, 'Can delete token', 12, 'delete_tokenproxy'),
(48, 'Can view token', 12, 'view_tokenproxy');

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE `client` (
  `id` bigint(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `phone` varchar(25) DEFAULT NULL,
  `company` varchar(128) NOT NULL,
  `note` longtext NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `sales_contact_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`id`, `email`, `first_name`, `last_name`, `phone`, `company`, `note`, `created_date`, `updated_date`, `sales_contact_id`) VALUES
(1, 'toto@example.com', 'Toto', 'TATA', '+33678912345', '', '', '2024-01-31 12:40:54.707797', '2024-02-15 09:57:09.227228', 3),
(6, 'client@create.com', 'John', 'PIERRE', NULL, '', '', '2024-02-06 15:31:32.321343', '2024-02-06 15:32:38.584082', 3),
(7, 'vedan@example.com', 'Vedan', 'ML', '+33 621475388', 'MuZika', '', '2024-02-06 21:11:11.011253', '2024-02-13 20:51:47.046463', 3),
(10, 'suzan@blender.com', 'Suzan', 'BLEND', '+33657894522', 'Blender foundation', '', '2024-02-13 20:26:06.994765', '2024-02-13 20:26:06.994919', 8);

-- --------------------------------------------------------

--
-- Table structure for table `contract`
--

CREATE TABLE `contract` (
  `id` uuid NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `amount_due` decimal(12,2) DEFAULT NULL,
  `signed` tinyint(1) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `client_id` bigint(20) DEFAULT NULL,
  `sales_contact_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `contract`
--

INSERT INTO `contract` (`id`, `total_amount`, `amount_due`, `signed`, `created_date`, `updated_date`, `client_id`, `sales_contact_id`) VALUES
('b62be181-4bb3-4dca-b9ea-24ef48fe9200', 1800.00, 500.00, 1, '2024-02-06 20:43:28.909473', '2024-02-15 10:06:30.432212', 6, 3),
('8b4f8cb0-6276-4958-bc6f-9d3b3666148f', 150000.00, 0.00, 1, '2024-01-31 13:53:40.048061', '2024-02-21 10:15:00.849783', 1, 3),
('05140107-4e13-46c7-a5a7-b64de1aabffd', 1200.00, 500.00, 0, '2024-02-07 08:23:22.862380', '2024-02-14 11:42:43.927965', 7, 3),
('85a7965e-5ac7-460f-bc1a-d0637a69f11d', 1244.00, 120.00, 1, '2024-02-19 19:57:16.272608', '2024-02-19 19:57:16.272640', 6, 3),
('9d6c7a4c-28c1-4241-8ec2-df42bdfd8fce', 1800.00, 100.00, 0, '2024-02-21 10:09:00.742177', '2024-02-21 10:12:07.525308', 10, 8),
('e80694fc-0c93-4dbc-8877-f49a0db7db01', 1000.00, 0.00, 1, '2024-02-06 21:12:14.526028', '2024-02-06 21:12:14.526071', 7, 3),
('7a45b445-85ee-41cf-bda9-f94f90370472', 1000.26, 0.00, 1, '2024-02-14 11:11:34.958666', '2024-02-15 16:12:01.778670', 10, 8);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2024-01-31 10:33:25.993028', '2', '2: TOTO test (test@example.com)', 1, '[{\"added\": {}}]', 7, 1),
(2, '2024-01-31 12:40:54.709138', '1', '1: TITI Toto; contact: 2: TOTO test (test@example.com) ', 1, '[{\"added\": {}}]', 8, 1),
(3, '2024-01-31 12:42:44.301187', 'c91db70b-80c3-418e-9d77-c6ac29ca2631', 'c91db70b-80c3-418e-9d77-c6ac29ca2631: Contract not signed - Client info is unavailable', 1, '[{\"added\": {}}]', 9, 1),
(4, '2024-01-31 12:42:57.755465', 'c91db70b-80c3-418e-9d77-c6ac29ca2631', 'c91db70b-80c3-418e-9d77-c6ac29ca2631: Contract not signed - TITI Toto', 2, '[{\"changed\": {\"fields\": [\"Client\"]}}]', 9, 1),
(5, '2024-01-31 12:43:41.300214', '0eef5941-ae3a-4bb7-8bbb-2348b2dce730', '0eef5941-ae3a-4bb7-8bbb-2348b2dce730: Contract not signed - TITI Toto', 1, '[{\"added\": {}}]', 9, 1),
(6, '2024-01-31 12:43:56.784054', '0eef5941-ae3a-4bb7-8bbb-2348b2dce730', '0eef5941-ae3a-4bb7-8bbb-2348b2dce730: Contract not signed - TITI Toto', 3, '', 9, 1),
(7, '2024-01-31 12:45:38.538736', 'c91db70b-80c3-418e-9d77-c6ac29ca2631', 'c91db70b-80c3-418e-9d77-c6ac29ca2631: Contract not signed - TITI Toto', 2, '[{\"changed\": {\"fields\": [\"Total amount\"]}}]', 9, 1),
(8, '2024-01-31 12:45:52.274201', '2727f173-c41e-4d91-8c9b-16a5ff5457c2', '2727f173-c41e-4d91-8c9b-16a5ff5457c2: Contract not signed - TITI Toto', 1, '[{\"added\": {}}]', 9, 1),
(9, '2024-01-31 12:46:35.759218', 'c91db70b-80c3-418e-9d77-c6ac29ca2631', 'c91db70b-80c3-418e-9d77-c6ac29ca2631: Contract not signed - TITI Toto', 3, '', 9, 1),
(10, '2024-01-31 12:46:35.766079', '2727f173-c41e-4d91-8c9b-16a5ff5457c2', '2727f173-c41e-4d91-8c9b-16a5ff5457c2: Contract not signed - TITI Toto', 3, '', 9, 1),
(11, '2024-01-31 12:50:52.194275', '1', '1: TITI Toto; Sales contact: TOTO test ', 2, '[{\"changed\": {\"fields\": [\"Email\", \"Phone\"]}}]', 8, 1),
(12, '2024-01-31 12:51:22.288982', '2', '2: SMITH John (test@example.com)', 2, '[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]', 7, 1),
(13, '2024-01-31 13:01:23.887519', '2', '2: SMITH John (test@example.com)', 3, '', 7, 1),
(14, '2024-01-31 13:03:19.885450', '3', '3: SMITH John (john@smith.com)', 1, '[{\"added\": {}}]', 7, 1),
(15, '2024-01-31 13:03:31.749270', '1', '1: TITI Toto; Sales contact: SMITH John ', 2, '[{\"changed\": {\"fields\": [\"Sales contact\"]}}]', 8, 1),
(16, '2024-01-31 13:53:40.049687', '8b4f8cb0-6276-4958-bc6f-9d3b3666148f', '8b4f8cb0-6276-4958-bc6f-9d3b3666148f: Contract not signed - TITI Toto', 1, '[{\"added\": {}}]', 9, 1),
(17, '2024-01-31 13:53:59.706882', '8b4f8cb0-6276-4958-bc6f-9d3b3666148f', '8b4f8cb0-6276-4958-bc6f-9d3b3666148f: Contract signed - TITI Toto', 2, '[{\"changed\": {\"fields\": [\"Signed\"]}}]', 9, 1),
(18, '2024-02-02 13:01:00.681905', '4', '4: TITI Toto (toto@example.com)', 1, '[{\"added\": {}}]', 7, 1),
(19, '2024-02-02 15:15:11.669891', '5', '5: KIKI Konqui (konqui@test.com)', 3, '', 7, 1),
(20, '2024-02-05 13:41:02.263498', '6', 'a536d5039dfd12e23b583b16cca23cbed142825a', 3, '', 12, 1),
(21, '2024-02-05 13:44:31.043784', '3', '55ed874ed3b3bd8c1dfdd2e1a403fb3e3c1a1b94', 3, '', 12, 1),
(22, '2024-02-05 13:56:12.343134', '1', '73cb00d95b49296883d4615aa423ef346b4a1e1b', 3, '', 12, 1),
(23, '2024-02-05 15:01:01.130888', '7', '7: KIKI Konqui (konqui@test.com1)', 3, '', 7, 1),
(24, '2024-02-05 16:41:04.710852', '3', '3: TODO test; No sales contact yet...', 1, '[{\"added\": {}}]', 8, 1),
(25, '2024-02-05 16:41:15.195995', '3', '3: TODO test; No sales contact yet...', 3, '', 8, 1),
(26, '2024-02-05 16:49:21.611670', '5', '5: eiue uei; No sales contact yet...', 1, '[{\"added\": {}}]', 8, 1),
(27, '2024-02-05 16:49:30.861257', '5', '5: eiue uei; No sales contact yet...', 3, '', 8, 1),
(28, '2024-02-06 20:43:28.911365', 'b62be181-4bb3-4dca-b9ea-24ef48fe9200', 'b62be181-4bb3-4dca-b9ea-24ef48fe9200: Contract not signed - PIERRE John', 1, '[{\"added\": {}}]', 9, 1),
(29, '2024-02-06 21:09:03.894106', '8b4f8cb0-6276-4958-bc6f-9d3b3666148f', '8b4f8cb0-6276-4958-bc6f-9d3b3666148f: Contract signed - TITI Toto', 2, '[{\"changed\": {\"fields\": [\"Amount due\"]}}]', 9, 1),
(30, '2024-02-06 21:11:11.013134', '7', '7: ML Vedan; contact: SMITH John ', 1, '[{\"added\": {}}]', 8, 1),
(31, '2024-02-06 21:12:14.528659', 'e80694fc-0c93-4dbc-8877-f49a0db7db01', 'e80694fc-0c93-4dbc-8877-f49a0db7db01: Contract signed - ML Vedan', 1, '[{\"added\": {}}]', 9, 1),
(32, '2024-02-07 08:24:31.580251', '8db46a53-fca3-4905-a982-ec703dfba072', '8db46a53-fca3-4905-a982-ec703dfba072: Contract not signed - ML Vedan', 3, '', 9, 1),
(33, '2024-02-07 08:40:40.768421', '8', '8: LEELU Marie (marie@sales.com)', 1, '[{\"added\": {}}]', 7, 1),
(34, '2024-02-07 12:57:25.602228', '1', '1: Birthday - PLANNED', 1, '[{\"added\": {}}]', 10, 1),
(35, '2024-02-07 14:58:24.744325', '2', '2: Concert - PLANNED', 3, '', 10, 1),
(36, '2024-02-07 14:59:41.985104', '3', '3: Concert - PLANNED', 3, '', 10, 1),
(37, '2024-02-07 15:05:43.552285', '4', '4: Concert - PLANNED', 3, '', 10, 1),
(38, '2024-02-07 15:06:39.152021', '5', '5: Concert - PLANNED', 3, '', 10, 1),
(39, '2024-02-07 15:47:54.833714', '9', '9: 1 Konqui (konqui@test.in)', 3, '', 7, 1),
(40, '2024-02-07 15:48:55.250539', '10', '10: WAITING Godot (godot@test.in)', 3, '', 7, 1),
(41, '2024-02-12 09:52:47.852824', '1', '4701862099567f34a861f09f396eb81353c71fbc', 1, '[{\"added\": {}}]', 12, 1),
(42, '2024-02-12 11:10:32.618287', '6', '6: KIKI Konqui (konqui@test.com)', 2, '[{\"changed\": {\"fields\": [\"Joined date\"]}}]', 7, 1),
(43, '2024-02-12 15:58:00.954221', '12', '12: last firt (test2@creat.con)', 3, '', 7, 1),
(44, '2024-02-12 15:59:12.442235', '13', '13: role Rte (role@test.com)', 3, '', 7, 1),
(45, '2024-02-12 16:01:51.828230', '11', '11: create test (test@createc.om)', 3, '', 7, 1),
(46, '2024-02-12 20:26:22.795760', '17', '17: TEST Test (etest@create.com)', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 7, 1),
(47, '2024-02-14 14:37:29.176428', '1', '1: Birthday - PLANNED', 2, '[{\"changed\": {\"fields\": [\"Location\"]}}]', 10, 1),
(48, '2024-02-14 21:06:16.280977', '1', '1: MANAGER Epic (epic@management.com)', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 7, 20),
(49, '2024-02-14 21:10:06.730792', '1', '1: Birthday - PLANNED', 3, '', 10, 20),
(50, '2024-02-15 10:22:17.852272', '6', '6: KIKI Konqui (konqui@test.com)', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 7, 20),
(51, '2024-02-15 16:12:01.779957', '7a45b445-85ee-41cf-bda9-f94f90370472', '7a45b445-85ee-41cf-bda9-f94f90370472: Contract signed - BLEND Suzan', 2, '[{\"changed\": {\"fields\": [\"Signed\"]}}]', 9, 20),
(52, '2024-02-21 09:41:03.596868', '8', '3f85b1e684ec15ea1377aeadd71b995894100eab', 1, '[{\"added\": {}}]', 12, 20),
(53, '2024-02-21 10:32:19.324373', '22', 'b1859efeda57cc153832e7ff7ad187ec3d99c9a5', 1, '[{\"added\": {}}]', 12, 20),
(54, '2024-02-21 10:36:06.949631', '12', '12: Farewell - HELD', 3, '', 10, 20);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(7, 'authentication', 'user'),
(11, 'authtoken', 'token'),
(12, 'authtoken', 'tokenproxy'),
(8, 'clients', 'client'),
(4, 'contenttypes', 'contenttype'),
(9, 'contracts', 'contract'),
(10, 'events', 'event'),
(5, 'sessions', 'session'),
(6, 'teams', 'team');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-01-31 10:31:45.561131'),
(2, 'teams', '0001_initial', '2024-01-31 10:31:45.581632'),
(3, 'contenttypes', '0002_remove_content_type_name', '2024-01-31 10:31:45.655016'),
(4, 'auth', '0001_initial', '2024-01-31 10:31:45.917561'),
(5, 'auth', '0002_alter_permission_name_max_length', '2024-01-31 10:31:45.972062'),
(6, 'auth', '0003_alter_user_email_max_length', '2024-01-31 10:31:45.979742'),
(7, 'auth', '0004_alter_user_username_opts', '2024-01-31 10:31:45.988222'),
(8, 'auth', '0005_alter_user_last_login_null', '2024-01-31 10:31:45.999355'),
(9, 'auth', '0006_require_contenttypes_0002', '2024-01-31 10:31:46.003741'),
(10, 'auth', '0007_alter_validators_add_error_messages', '2024-01-31 10:31:46.012640'),
(11, 'auth', '0008_alter_user_username_max_length', '2024-01-31 10:31:46.027380'),
(12, 'auth', '0009_alter_user_last_name_max_length', '2024-01-31 10:31:46.040231'),
(13, 'auth', '0010_alter_group_name_max_length', '2024-01-31 10:31:46.080660'),
(14, 'auth', '0011_update_proxy_permissions', '2024-01-31 10:31:46.095996'),
(15, 'auth', '0012_alter_user_first_name_max_length', '2024-01-31 10:31:46.114047'),
(16, 'authentication', '0001_initial', '2024-01-31 10:31:46.497864'),
(17, 'admin', '0001_initial', '2024-01-31 10:31:46.617491'),
(18, 'admin', '0002_logentry_remove_auto_add', '2024-01-31 10:31:46.669125'),
(19, 'admin', '0003_logentry_add_action_flag_choices', '2024-01-31 10:31:46.707143'),
(20, 'clients', '0001_initial', '2024-01-31 10:31:46.804761'),
(21, 'sessions', '0001_initial', '2024-01-31 10:31:46.840079'),
(22, 'teams', '0002_auto_20240131_1031', '2024-01-31 10:31:46.871168'),
(23, 'contracts', '0001_initial', '2024-01-31 12:39:17.483064'),
(24, 'events', '0001_initial', '2024-01-31 13:52:24.996589'),
(25, 'authtoken', '0001_initial', '2024-02-01 14:24:32.444932'),
(26, 'authtoken', '0002_auto_20160226_1747', '2024-02-01 14:24:32.499202'),
(27, 'authtoken', '0003_tokenproxy', '2024-02-01 14:24:32.504054'),
(28, 'teams', '0002_auto_20240215_2245', '2024-02-15 22:46:10.699221');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('88nlyvuco5eb1vhl4qcwab7750tbsl4o', '.eJxVjMsOwiAQRf-FtSEzyKO4dO83kGGgUjWQlHZl_HfbpAvd3nPOfYtA61LC2vMcpiQuQoE4_Y6R-JnrTtKD6r1JbnWZpyh3RR60y1tL-XU93L-DQr1stVcWEIbsEM_JMaMGBtLWAhEDUkQYjYcxszYpKiCDPse0OYMDpZz4fAHpmTeZ:1raYsj:wf8CxnaRZePkdmx8hd346I3zw6WsX9pPLVZUa0il79w', '2024-02-29 10:22:17.864133'),
('achpvzymdxp9v3u2smoegik7ia9lb00r', '.eJxVjEEOwiAQRe_C2hCgQAeX7j0DmYEZWzVtUtqV8e7apAvd_vfef6mM2zrkrfGSx6rOyqrT70ZYHjztoN5xus26zNO6jKR3RR-06etc-Xk53L-DAdvwrU2IwYJ445hEUKCn2llxHoEABLj4PiRgIo62c8YB-mI4Jamx58jq_QHr4ThN:1rVZhU:VXeN-cyS2QWOwBpvO-NPQwFKyQG2YwvtqqUncD2Lkdo', '2024-02-15 16:14:04.676393'),
('d9dkpnvmqy0ycna11pmdcblx8r5fjcc7', '.eJxVjEEOwiAQRe_C2hCgQAeX7j0DmYEZWzVtUtqV8e7apAvd_vfef6mM2zrkrfGSx6rOyqrT70ZYHjztoN5xus26zNO6jKR3RR-06etc-Xk53L-DAdvwrU2IwYJ445hEUKCn2llxHoEABLj4PiRgIo62c8YB-mI4Jamx58jq_QHr4ThN:1rVsSg:v5crXmUJ0nW4S6aoCASivQxy0Ng-TAZjwgugH19V63U', '2024-02-16 12:16:02.455938');

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `location` longtext NOT NULL,
  `number_of_attendees` int(10) UNSIGNED NOT NULL CHECK (`number_of_attendees` >= 0),
  `notes` longtext NOT NULL,
  `status` varchar(64) DEFAULT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) NOT NULL,
  `contract_id` uuid NOT NULL,
  `support_contact_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`id`, `name`, `start_date`, `end_date`, `location`, `number_of_attendees`, `notes`, `status`, `created_date`, `updated_date`, `contract_id`, `support_contact_id`) VALUES
(6, 'Concert', '2024-05-12 00:00:00.000000', '2024-05-15 00:00:00.000000', '', 0, '', 'PLANNED', '2024-02-07 15:19:08.661636', '2024-02-07 15:19:08.661669', 'e80694fc-0c93-4dbc-8877-f49a0db7db01', NULL),
(9, 'Dance festival', '2024-01-01 00:00:00.000000', '2024-01-04 00:00:00.000000', 'Dinard', 452, 'Need more info on location', 'PLANNED', '2024-02-14 21:10:32.607084', '2024-02-15 11:07:08.104780', '8b4f8cb0-6276-4958-bc6f-9d3b3666148f', 6),
(10, 'John Pierre\'s birthday', '2025-01-02 00:00:00.000000', '2025-01-02 00:00:00.000000', 'Somewhere', 1, 'lonely birthday', 'PLANNED', '2024-02-15 10:19:28.842693', '2024-02-15 12:53:47.095432', 'b62be181-4bb3-4dca-b9ea-24ef48fe9200', 6),
(11, 'Blender Conf', '2024-05-05 04:01:00.000000', '2024-05-10 00:00:00.000000', 'Amsterdam', 300, '', 'PLANNED', '2024-02-15 16:15:57.624359', '2024-02-15 16:15:57.624408', '7a45b445-85ee-41cf-bda9-f94f90370472', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `team`
--

CREATE TABLE `team` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `created_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

--
-- Dumping data for table `team`
--

INSERT INTO `team` (`id`, `name`, `created_date`) VALUES
(1, 'MANAGEMENT', '2024-01-31 10:31:46.862827'),
(2, 'SALES', '2024-01-31 10:31:46.865815'),
(3, 'SUPPORT', '2024-01-31 10:31:46.868235');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authentication_user`
--
ALTER TABLE `authentication_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `authentication_user_role_id_24664e00_fk_team_id` (`role_id`);

--
-- Indexes for table `authentication_user_groups`
--
ALTER TABLE `authentication_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `authentication_user_groups_user_id_group_id_8af031ac_uniq` (`user_id`,`group_id`),
  ADD KEY `authentication_user_groups_group_id_6b5c44b7_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `authentication_user_user_permissions`
--
ALTER TABLE `authentication_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `authentication_user_user_user_id_permission_id_ec51b09f_uniq` (`user_id`,`permission_id`),
  ADD KEY `authentication_user__permission_id_ea6be19a_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD KEY `client_sales_contact_id_1bbb9a66_fk_authentication_user_id` (`sales_contact_id`);

--
-- Indexes for table `contract`
--
ALTER TABLE `contract`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contract_client_id_afea8eeb_fk_client_id` (`client_id`),
  ADD KEY `contract_sales_contact_id_9b0e50ee_fk_authentication_user_id` (`sales_contact_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_authentication_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `contract_id` (`contract_id`),
  ADD KEY `event_support_contact_id_a1ef69aa_fk_authentication_user_id` (`support_contact_id`);

--
-- Indexes for table `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `authentication_user`
--
ALTER TABLE `authentication_user`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `authentication_user_groups`
--
ALTER TABLE `authentication_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `authentication_user_user_permissions`
--
ALTER TABLE `authentication_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `client`
--
ALTER TABLE `client`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `team`
--
ALTER TABLE `team`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `authentication_user`
--
ALTER TABLE `authentication_user`
  ADD CONSTRAINT `authentication_user_role_id_24664e00_fk_team_id` FOREIGN KEY (`role_id`) REFERENCES `team` (`id`);

--
-- Constraints for table `authentication_user_groups`
--
ALTER TABLE `authentication_user_groups`
  ADD CONSTRAINT `authentication_user__user_id_30868577_fk_authentic` FOREIGN KEY (`user_id`) REFERENCES `authentication_user` (`id`),
  ADD CONSTRAINT `authentication_user_groups_group_id_6b5c44b7_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `authentication_user_user_permissions`
--
ALTER TABLE `authentication_user_user_permissions`
  ADD CONSTRAINT `authentication_user__permission_id_ea6be19a_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `authentication_user__user_id_736ebf7e_fk_authentic` FOREIGN KEY (`user_id`) REFERENCES `authentication_user` (`id`);

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_authentication_user_id` FOREIGN KEY (`user_id`) REFERENCES `authentication_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `client`
--
ALTER TABLE `client`
  ADD CONSTRAINT `client_sales_contact_id_1bbb9a66_fk_authentication_user_id` FOREIGN KEY (`sales_contact_id`) REFERENCES `authentication_user` (`id`);

--
-- Constraints for table `contract`
--
ALTER TABLE `contract`
  ADD CONSTRAINT `contract_client_id_afea8eeb_fk_client_id` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  ADD CONSTRAINT `contract_sales_contact_id_9b0e50ee_fk_authentication_user_id` FOREIGN KEY (`sales_contact_id`) REFERENCES `authentication_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_authentication_user_id` FOREIGN KEY (`user_id`) REFERENCES `authentication_user` (`id`);

--
-- Constraints for table `event`
--
ALTER TABLE `event`
  ADD CONSTRAINT `event_contract_id_b365512a_fk_contract_id` FOREIGN KEY (`contract_id`) REFERENCES `contract` (`id`),
  ADD CONSTRAINT `event_support_contact_id_a1ef69aa_fk_authentication_user_id` FOREIGN KEY (`support_contact_id`) REFERENCES `authentication_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
