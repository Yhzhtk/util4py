
CREATE TABLE `key_statist` (   
	`id` int(64) NOT NULL AUTO_INCREMENT,     
	`host` varchar(24) DEFAULT NULL,          
	`keyword` varchar(100) NOT NULL,          
	`count` int(32) DEFAULT NULL,
	`date` date DEFAULT NULL,    
	PRIMARY KEY (`id`),          
	KEY `KEYINDEX` (`keyword`)   
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

CREATE TABLE `position_statist` (            
	`id` int(64) NOT NULL AUTO_INCREMENT,      
	`host` varchar(24) DEFAULT NULL,           
	`pid` int(32) DEFAULT NULL,   
	`adword` int(8) DEFAULT NULL, 
	`count` int(32) DEFAULT NULL, 
	`date` date DEFAULT NULL,     
	PRIMARY KEY (`id`),           
	KEY `PIDINDEX` (`pid`),       
	KEY `ADWORDINDEX` (`adword`)  
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

