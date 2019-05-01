 ______________________
|___DATABASE 'ghbpmn'__|
--------------------------------------------------------
-- -----------------------------------------------------
-- Table 'ghbpmn'.'all_gh_users'
-- -----------------------------------------------------
CREATE TABLE ghbpmn.all_gh_users(
 id INTEGER PRIMARY KEY,
 login TEXT NOT NULL,
 country_code TEXT
 );

-- -----------------------------------------------------
-- Table 'ghbpmn'.'all_gh_projects'
-- -----------------------------------------------------
CREATE TABLE ghbpmn.all_gh_projects(
 id INTEGER PRIMARY KEY,
 login TEXT NOT NULL,
 name TEXT NOT NULL
 );

-- -----------------------------------------------------
-- Table 'ghbpmn'.'to_query_projects'
-- -----------------------------------------------------
CREATE TABLE ghbpmn.to_query_projects(
 id INTEGER PRIMARY KEY,
 login TEXT NOT NULL,
 name TEXT NOT NULL,
 status TYNYINT NOT NULL DEFAULT 0
 );

-- -----------------------------------------------------
-- Table 'ghbpmn'.'result_projects'
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS gh.result_projects(
  login TEXT NOT NULL,
  name TEXT NOT NULL,
  language TEXT,
  created_at TEXT,
  last_commit_at TEXT,
  location_country TEXT,
  PRIMARY KEY(login, name)
);

-- -----------------------------------------------------
-- Table 'ghbpmn'.'result_files'
-- -----------------------------------------------------
CREATE TABLE ghbpmn.result_files(
  login TEXT NOT NULL,
  name TEXT NOT NULL,
  link_file TEXT PRIMARY KEY,
  path_file TEXT NOT NULL,
  n_authors INT,
  n_revs INT,
  age_months INT
);

-- -----------------------------------------------------
-- Table 'ghbpmn'.'copy_result_files'
-- -----------------------------------------------------
CREATE TABLE ghbpmn.copy_result_files(
  path_file TEXT PRIMARY KEY,
  path_copy_file TEXT NOT NULL,
  duplicate INT
);

-- -----------------------------------------------------
-- Table 'ghbpmn'.'result_bpmn'
-- -----------------------------------------------------
CREATE TABLE ghbpmn.result_bpmn(
  path_file TEXT PRIMARY KEY,
  valid INT,
  constraints_list TEXT
);


--------------------------------------------------------
 _____________________
|___DATABASE 'part1'__|
-- -----------------------------------------------------
-- Table 'part1'.'to_query_projects1'
-- -----------------------------------------------------
CREATE TABLE part1.to_query_projects1(
 id INTEGER PRIMARY KEY,
 login TEXT NOT NULL,
 name TEXT NOT NULL,
 status TYNYINT NOT NULL DEFAULT 0
 );

CREATE TABLE part1.result_links1(
 login TEXT NOT NULL,
 name TEXT NOT NULL,
 link_file TEXT PRIMARY KEY
 );

--------------------------------------------------------
 _____________________
|___DATABASE 'part2'__|
-- -----------------------------------------------------
-- Table 'part2'.'to_query_projects2'
-- -----------------------------------------------------
CREATE TABLE part2.to_query_projects2(
 id INTEGER PRIMARY KEY,
 login TEXT NOT NULL,
 name TEXT NOT NULL,
 status TYNYINT NOT NULL DEFAULT 0
 );

CREATE TABLE part2.result_links2(
 login TEXT NOT NULL,
 name TEXT NOT NULL,
 link_file TEXT PRIMARY KEY
 );
--------------------------------------------------------
 _____________________
|___DATABASE 'part3'__|
-- -----------------------------------------------------
-- Table 'part3'.'to_query_projects3'
-- -----------------------------------------------------
CREATE TABLE part3.to_query_projects3(
 id INTEGER PRIMARY KEY,
 login TEXT NOT NULL,
 name TEXT NOT NULL,
 status TYNYINT NOT NULL DEFAULT 0
 );

CREATE TABLE part3.result_links3(
 login TEXT NOT NULL,
 name TEXT NOT NULL,
 link_file TEXT PRIMARY KEY
 );
--------------------------------------------------------
 _____________________
|___DATABASE 'part4'__|
-- -----------------------------------------------------
-- Table 'part4'.'to_query_projects4'
-- -----------------------------------------------------
CREATE TABLE part4.to_query_projects4(
 id INTEGER PRIMARY KEY,
 login TEXT NOT NULL,
 name TEXT NOT NULL,
 status TYNYINT NOT NULL DEFAULT 0
 );

CREATE TABLE part4.result_links4(
 login TEXT NOT NULL,
 name TEXT NOT NULL,
 link_file TEXT PRIMARY KEY
 );