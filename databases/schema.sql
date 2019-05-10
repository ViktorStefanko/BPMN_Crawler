CREATE TABLE "users" (
  "id" INTEGER PRIMARY KEY,
  "login" TEXT,
  "country_code" TEXT
);

CREATE TABLE "projects" (
  "id" INTEGER PRIMARY KEY,
  "name" TEXT,
  "owner_id" INTEGER,
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
  "duplicate" INTEGER
);

CREATE TABLE "result_projects" (
  "login" TEXT,
  "name" TEXT,
  "language" TEXT,
  "created_at" TEXT,
  "last_commit_at" TEXT,
  "location_country" TEXT
);

CREATE TABLE "copy_result_files" (
  "path_file" TEXT PRIMARY KEY,
  "path_copy_file" TEXT
);

CREATE TABLE "result_bpmn" (
  "path_file" TEXT PRIMARY KEY,
  "valid" TYNYINT,
  "constraints_list" TEXT
);

ALTER TABLE "projects" ADD FOREIGN KEY ("owner_id") REFERENCES "users" ("id");

ALTER TABLE "to_query_projects" ADD FOREIGN KEY ("login") REFERENCES "users" ("login");

ALTER TABLE "to_query_projects" ADD FOREIGN KEY ("name") REFERENCES "projects" ("name");

ALTER TABLE "projects" ADD FOREIGN KEY ("forked_from") REFERENCES "projects" ("id");

ALTER TABLE "result_files" ADD FOREIGN KEY ("login") REFERENCES "to_query_projects" ("login");

ALTER TABLE "result_files" ADD FOREIGN KEY ("name") REFERENCES "to_query_projects" ("name");

ALTER TABLE "result_projects" ADD FOREIGN KEY ("login") REFERENCES "result_files" ("login");

ALTER TABLE "result_projects" ADD FOREIGN KEY ("name") REFERENCES "result_files" ("name");

ALTER TABLE "copy_result_files" ADD FOREIGN KEY ("path_file") REFERENCES "result_files" ("path_file");

ALTER TABLE "result_bpmn" ADD FOREIGN KEY ("path_file") REFERENCES "result_files" ("path_file");