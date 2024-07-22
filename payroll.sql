-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 24, 2022 at 01:39 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.4.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `payroll`
--

-- --------------------------------------------------------

--
-- Table structure for table `company`
--

CREATE TABLE `company` (
  `sno` int(11) NOT NULL,
  `username` varchar(300) NOT NULL,
  `password` varchar(255) NOT NULL,
  `Name` varchar(300) NOT NULL,
  `contact` varchar(50) NOT NULL,
  `status` varchar(20) NOT NULL,
  `datetime` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `company`
--

INSERT INTO `company` (`sno`, `username`, `password`, `Name`, `contact`, `status`, `datetime`) VALUES
(3, 'satvik2001', '123', 'insrow', 'satvik017@gmail.com', 'active', '2022-05-22 09:06:36');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `sno` int(100) NOT NULL,
  `username` varchar(300) NOT NULL,
  `password` varchar(400) NOT NULL,
  `name` varchar(300) NOT NULL,
  `companyID` int(100) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(20) NOT NULL,
  `profile` varchar(200) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `email` varchar(300) NOT NULL,
  `status` varchar(20) NOT NULL,
  `datetime` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`sno`, `username`, `password`, `name`, `companyID`, `dob`, `gender`, `profile`, `phone`, `email`, `status`, `datetime`) VALUES
(2, 'satvik111', '123', 'satvik sharma', 3, '1989-06-21', 'male', 'a', '', 'satvik2711@gmail.com', 'active', '2022-05-23 06:06:50');

-- --------------------------------------------------------

--
-- Table structure for table `salary`
--

CREATE TABLE `salary` (
  `sno` int(100) NOT NULL,
  `companyID` int(100) NOT NULL,
  `designation` varchar(100) NOT NULL,
  `basic_pay` decimal(10,2) NOT NULL,
  `hra` decimal(10,2) NOT NULL,
  `food` decimal(10,2) NOT NULL,
  `overtime` decimal(10,2) NOT NULL,
  `pf` decimal(10,2) NOT NULL,
  `datetime` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `salary`
--

INSERT INTO `salary` (`sno`, `companyID`, `designation`, `basic_pay`, `hra`, `food`, `overtime`, `pf`, `datetime`) VALUES
(2, 3, 'assistant software engineer', '0.00', '0.00', '0.00', '0.00', '0.00', '2022-05-24 03:41:31'),
(3, 3, 'software engineer', '0.00', '0.00', '0.00', '0.00', '0.00', '2022-05-24 03:41:32'),
(4, 3, 'project manager', '0.00', '0.00', '0.00', '0.00', '0.00', '2022-05-24 03:41:33'),
(5, 3, 'manager', '0.00', '0.00', '0.00', '0.00', '0.00', '2022-05-24 03:41:33'),
(6, 3, 'fresher', '1000.00', '0.00', '0.00', '0.00', '0.00', '2022-05-24 03:54:22');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `company`
--
ALTER TABLE `company`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `salary`
--
ALTER TABLE `salary`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `company`
--
ALTER TABLE `company`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `sno` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `salary`
--
ALTER TABLE `salary`
  MODIFY `sno` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
