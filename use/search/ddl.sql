
CREATE TABLE `key_statist` (
	`id` int(64) NOT NULL AUTO_INCREMENT COMMENT 'id,自增',
	`host` varchar(24) DEFAULT NULL COMMENT '统计的主机',
	`keyword` varchar(100) NOT NULL COMMENT '关键字',
	`count` int(32) DEFAULT NULL COMMENT '搜索次数',
	`date` date DEFAULT NULL COMMENT '统计日期',
	PRIMARY KEY (`id`),
	KEY `KEYINDEX` (`keyword`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `position_statist` (
	`id` int(64) NOT NULL AUTO_INCREMENT COMMENT 'id,自增',
	`host` varchar(24) DEFAULT NULL COMMENT '统计的主机',
	`pid` int(32) DEFAULT NULL COMMENT '职位ID',
	`adword` int(8) DEFAULT NULL COMMENT '职位推广属性',
	`count` int(32) DEFAULT NULL COMMENT '展示次数',
	`date` date DEFAULT NULL COMMENT '统计日期',
	PRIMARY KEY (`id`),
	KEY `PIDINDEX` (`pid`),
	KEY `ADWORDINDEX` (`adword`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

