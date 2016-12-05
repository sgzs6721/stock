-- phpMyAdmin SQL Dump
-- version 4.5.5.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2016-12-06 01:04:32
-- 服务器版本： 5.7.11
-- PHP Version: 5.5.36

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stock`
--

-- --------------------------------------------------------

--
-- 表的结构 `ten`
--

CREATE TABLE `ten` (
  `id` int(32) NOT NULL,
  `person` varchar(32) NOT NULL,
  `prediction` varchar(16) NOT NULL,
  `num` varchar(8) NOT NULL,
  `predict_time` datetime NOT NULL,
  `success_date` varchar(64) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `success` int(8) DEFAULT NULL,
  `increaseone` varchar(32) DEFAULT NULL,
  `increasetwo` varchar(32) DEFAULT NULL,
  `increasefive` varchar(32) DEFAULT NULL,
  `increaseten` varchar(32) DEFAULT NULL,
  `increasefifteen` varchar(32) DEFAULT NULL,
  `increasetwenty` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `ten`
--

INSERT INTO `ten` (`id`, `person`, `prediction`, `num`, `predict_time`, `success_date`, `price`, `success`, `increaseone`, `increasetwo`, `increasefive`, `increaseten`, `increasefifteen`, `increasetwenty`) VALUES
(1, 'jsjs123', '银润投资', '000526', '2015-09-01 01:17:00', '', 40.28, 0, '-18.74,0.00,-20.77', '-16.12,0.00,-20.77', '-10.88,0.00,-23.18', '-19.86,0.00,-26.43', '-3.86,0.00,-26.43', '-0.72,2.42,-26.43');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ten`
--
ALTER TABLE `ten`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `ten`
--
ALTER TABLE `ten`
  MODIFY `id` int(32) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
