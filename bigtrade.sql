-- phpMyAdmin SQL Dump
-- version 4.5.5.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2016-11-29 01:47:49
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
-- 表的结构 `bigtrade`
--

CREATE TABLE `bigtrade` (
  `date` date DEFAULT NULL COMMENT AS `大宗交易日期`,
  `num` varchar(8) DEFAULT NULL COMMENT AS `股票代码`,
  `name` varchar(255) DEFAULT NULL COMMENT AS `股票名称`,
  `dealprice` double DEFAULT NULL COMMENT AS `成交价`,
  `closeprice` double DEFAULT NULL COMMENT AS `收盘价`,
  `islimited` tinyint(1) DEFAULT NULL COMMENT AS `是否涨停`,
  `discount` double DEFAULT NULL COMMENT AS `溢价率`,
  `volume` double DEFAULT NULL COMMENT AS `成交量`,
  `volumemoney` double DEFAULT NULL COMMENT AS `成交金额`,
  `dealrate` double DEFAULT NULL COMMENT AS `成交比例`,
  `buy` varchar(255) DEFAULT NULL COMMENT AS `买方营业部`,
  `sell` varchar(255) DEFAULT NULL COMMENT AS `卖方营业部`,
  `sameplace` tinyint(1) DEFAULT NULL COMMENT AS `是否为同一家营业部买卖`,
  `increaseone` varchar(32) DEFAULT NULL,
  `increasetwo` varchar(32) DEFAULT NULL COMMENT AS `2日涨幅`,
  `increasefive` varchar(32) DEFAULT NULL COMMENT AS `5日涨幅`,
  `increaseten` varchar(32) DEFAULT NULL COMMENT AS `10日涨幅`,
  `increasefifteen` varchar(32) DEFAULT NULL COMMENT AS `15日涨幅`,
  `increasetwenty` varchar(32) DEFAULT NULL COMMENT AS `20日涨幅`,
  `ontop` tinyint(1) DEFAULT NULL,
  `toptype` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `bigtrade`
--

INSERT INTO `bigtrade` (`date`, `num`, `name`, `dealprice`, `closeprice`, `islimited`, `discount`, `volume`, `volumemoney`, `dealrate`, `buy`, `sell`, `sameplace`, `increaseone`, `increasetwo`, `increasefive`, `increaseten`, `increasefifteen`, `increasetwenty`, `ontop`, `toptype`) VALUES
('2016-11-15', '600393', 'ÔÁÌ©¹É·Ý', 11.66, 13.12, 0, -11.13, 1465.62, 17089.1, 4.5, '¶«·½Ö¤È¯¹É·ÝÓÐÏÞ¹«Ë¾ÉÏº£ÆÖ¶«ÐÂÇøÕÅÑîÂ·Ö¤È¯ÓªÒµ²¿', '»ªÈÚÖ¤È¯¹É·ÝÓÐÏÞ¹«Ë¾×Ü²¿', 0, '5.67,7.13,0.00', '8.35,9.58,0.00', '11.26,13.87,0.00', '', '', '', 0, '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bigtrade`
--
ALTER TABLE `bigtrade`
  ADD UNIQUE KEY `date` (`date`,`num`,`dealprice`,`buy`,`sell`) USING BTREE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
