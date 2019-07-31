CREATE TABLE "users" (
  "id" INTEGER PRIMARY KEY,
  "login" TEXT UNIQUE NOT NULL,
  "country_code" TEXT
);

CREATE TABLE "projects" (
  "id" INTEGER PRIMARY KEY,
  "name" TEXT UNIQUE NOT NULL,
  "owner_id" INTEGER UNIQUE NOT NULL,
  "forked_from" INTEGER,
  "deleted" TYNYINT
);

CREATE TABLE "to_query_projects" (
  "id" INTEGER PRIMARY KEY,
  "login" TEXT,
  "name" TEXT,
  "status" TYNYINT
);

CREATE TABLE "result_files" (
  "login" TEXT,
  "name" TEXT,
  "link_file" TEXT PRIMARY KEY,
  "path_file" TEXT,
  "n_authors" INTEGER,
  "n_revs" INTEGER,
  "age_months" INTEGER,
  "duplicate" INTEGER,
  "is_xml" INTEGER
);

CREATE TABLE "result_projects" (
  "login" TEXT PRIMARY KEY,
  "name" TEXT PRIMARY KEY,
  "language" TEXT,
  "created_at" TEXT,
  "last_commit_at" TEXT,
  "n_commits" INTEGER,
  "location_country" TEXT
);

CREATE TABLE "copy_result_files" (
  "path_file" TEXT PRIMARY KEY,
  "path_copy_file" TEXT
);

CREATE TABLE "result_xml_original" (
  "path_file" TEXT PRIMARY KEY,
  "path_copy_file" TEXT,
  "has_copy" INTEGER,
  "n_xml_elements" INTEGER,
  "valid" INTEGER,
  "valid_after_repairing" INTEGER,
  "constraints_list" TEXT,
  "constraints_list_after_repairing" TEXT,
  "BPMNDiagram" INTEGER
);

ALTER TABLE "users" ADD FOREIGN KEY ("id") REFERENCES "projects" ("owner_id");

ALTER TABLE "users" ADD FOREIGN KEY ("login") REFERENCES "to_query_projects" ("login");

ALTER TABLE "projects" ADD FOREIGN KEY ("name") REFERENCES "to_query_projects" ("name");

ALTER TABLE "projects" ADD FOREIGN KEY ("id") REFERENCES "projects" ("forked_from");

ALTER TABLE "to_query_projects" ADD FOREIGN KEY ("login") REFERENCES "result_files" ("login");

ALTER TABLE "to_query_projects" ADD FOREIGN KEY ("name") REFERENCES "result_files" ("name");

ALTER TABLE "result_files" ADD FOREIGN KEY ("path_file") REFERENCES "result_xml_original" ("path_file");

ALTER TABLE "copy_result_files" ADD FOREIGN KEY ("path_copy_file") REFERENCES "result_xml_original" ("path_copy_file");

ALTER TABLE "result_files" ADD FOREIGN KEY ("login") REFERENCES "result_projects" ("login");

ALTER TABLE "result_files" ADD FOREIGN KEY ("name") REFERENCES "result_projects" ("name");

ALTER TABLE "result_files" ADD FOREIGN KEY ("path_file") REFERENCES "copy_result_files" ("path_file");