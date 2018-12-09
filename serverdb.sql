-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 14, 2018 at 07:45 AM
-- Server version: 10.1.28-MariaDB
-- PHP Version: 7.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `serverdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `clienta`
--

CREATE TABLE `clienta` (
  `id` int(10) NOT NULL,
  `NearestNode` int(10) NOT NULL,
  `Description` varchar(250) NOT NULL,
  `address` varchar(500) NOT NULL,
  `contact` int(10) NOT NULL,
  `isProhibited` tinyint(1) NOT NULL,
  `Latitude` float(10,7) NOT NULL,
  `Longitude` float(10,7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `clienta`
--



-- --------------------------------------------------------

--
-- Table structure for table `clientb`
--

CREATE TABLE `clientb` (
  `id` int(10) NOT NULL,
  `address` varchar(250) NOT NULL,
  `contact` int(10) NOT NULL,
  `description` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `clientb`
--


-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `SourceID` int(10) NOT NULL,
  `DestinationID` int(10) NOT NULL,
  `Time` datetime(6) NOT NULL,
  `location_description` varchar(250) NOT NULL,
  `Activity_Recognized` varchar(250) NOT NULL,
  `location_address` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `messages`
--


--
-- Indexes for dumped tables
--

--
-- Indexes for table `clienta`
--
ALTER TABLE `clienta`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `clientb`
--
ALTER TABLE `clientb`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
