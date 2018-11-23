### Create table users
CREATE TABLE IF NOT EXISTS `ghtorrent_restore`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
  `login` VARCHAR(255) NOT NULL COMMENT '',
  `company` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `type` VARCHAR(255) NOT NULL DEFAULT 'USR' COMMENT '',
  `fake` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '',
  `deleted` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '',
  `long` DECIMAL(11,8) COMMENT '',
  `lat` DECIMAL(10,8) COMMENT '',
  `country_code` CHAR(3) COMMENT '',
  `state` VARCHAR(255) COMMENT '',
  `city` VARCHAR(255) COMMENT '',
  `location` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '')
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;



### Create table projects
CREATE TABLE IF NOT EXISTS `ghtorrent_restore`.`projects` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '',
  `url` VARCHAR(255) NULL DEFAULT NULL COMMENT '',
  `owner_id` INT(11) NULL DEFAULT NULL COMMENT '',
  `name` VARCHAR(255) NOT NULL COMMENT '',
  `forked_from` INT(11) NULL DEFAULT NULL COMMENT '',
  `deleted` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '',
  PRIMARY KEY (`id`)  COMMENT '');
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

### Load data from csv files into tables in database
LOAD DATA LOCAL INFILE 'C:/Users/viktor/Documents/education/bachelorarbeit/data_dump_GHTorrent/extracted_files/users.csv' INTO TABLE ghtorrent_restore.users FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n';
LOAD DATA LOCAL INFILE 'C:/Users/viktor/Documents/education/bachelorarbeit/data_dump_GHTorrent/extracted_files/projects.csv' INTO TABLE ghtorrent_restore.projects FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n' (id, url, owner_id, name, @dummy, @dummy, @dummy, forked_from, deleted, @dummy);

### Create login_and_proj_name table with two culumns: login and project's name
CREATE TABLE projects_not_forked AS SELECT * FROM projects WHERE projects.forked_from IS NULL;
CREATE TABLE login_and_proj_name AS SELECT users.login, projects_not_forked.name FROM projects_not_forked, users WHERE projects_not_forked.owner_id=users.id;


# show tables;
# show table status;
# describe login_and_proj_name;