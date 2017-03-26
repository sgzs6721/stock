-- phpMyAdmin SQL Dump
-- version 4.5.5.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 2017-03-26 16:08:56
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
  `date` date NOT NULL COMMENT '大宗交易日期',
  `num` varchar(8) NOT NULL COMMENT '股票代码',
  `name` varchar(255) NOT NULL COMMENT '股票名称',
  `dealprice` double NOT NULL COMMENT '成交价',
  `closeprice` double NOT NULL COMMENT '收盘价',
  `islimited` tinyint(1) DEFAULT NULL COMMENT AS `是否涨停`,
  `discount` double DEFAULT NULL COMMENT AS `溢价率`,
  `volume` double DEFAULT NULL COMMENT AS `成交量`,
  `volumemoney` double DEFAULT NULL COMMENT AS `成交金额`,
  `dealrate` double DEFAULT NULL COMMENT AS `成交比例`,
  `buy` varchar(255) NOT NULL COMMENT '买方营业部',
  `sell` varchar(255) NOT NULL COMMENT '卖方营业部',
  `sameplace` tinyint(1) DEFAULT NULL COMMENT AS `是否为同一家营业部买卖`,
  `increaseone` varchar(32) DEFAULT NULL COMMENT AS `1 日涨幅`,
  `increasetwo` varchar(32) DEFAULT NULL COMMENT AS `2日涨幅`,
  `increasefive` varchar(32) DEFAULT NULL COMMENT AS `5日涨幅`,
  `increaseten` varchar(32) DEFAULT NULL COMMENT AS `10日涨幅`,
  `increasefifteen` varchar(32) DEFAULT NULL COMMENT AS `15日涨幅`,
  `increasetwenty` varchar(32) DEFAULT NULL COMMENT AS `20日涨幅`,
  `ontop` tinyint(1) DEFAULT NULL COMMENT AS `是否上龙虎榜`,
  `toptype` varchar(255) DEFAULT NULL COMMENT AS `上榜类型`
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `statistics`
--

CREATE TABLE `statistics` (
  `id` int(11) NOT NULL,
  `person` varchar(32) NOT NULL,
  `num` int(8) DEFAULT '1',
  `success` int(8) NOT NULL DEFAULT '0',
  `rate` int(4) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `ten`
--

CREATE TABLE `ten` (
  `id` int(32) NOT NULL,
  `person` varchar(32) NOT NULL,
  `name` varchar(16) NOT NULL,
  `code` varchar(8) NOT NULL,
  `time` datetime NOT NULL,
  `price` double DEFAULT NULL,
  `date` date DEFAULT NULL COMMENT AS `成功日期`,
  `success` int(4) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bigtrade`
--
ALTER TABLE `bigtrade`
  ADD UNIQUE KEY `date` (`date`,`num`,`dealprice`,`buy`,`sell`,`volume`) USING BTREE;

--
-- Indexes for table `statistics`
--
ALTER TABLE `statistics`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ten`
--
ALTER TABLE `ten`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `update` (`person`,`code`,`time`,`price`) USING BTREE;

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `statistics`
--
ALTER TABLE `statistics`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- 使用表AUTO_INCREMENT `ten`
--
ALTER TABLE `ten`
  MODIFY `id` int(32) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
