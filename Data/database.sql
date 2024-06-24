CREATE TABLE "posts" (
  "id_post" integer PRIMARY KEY,
  "title" varchar,
  "body" text,
  "has_image" boolean,
  "status" varchar(3),
  "publishing_date" timestamp
);

CREATE TABLE "images" (
  "id_image" integer PRIMARY KEY,
  "added_at" timestamp,
  "url" varchar,
  "caption" varchar
);

CREATE TABLE "tags" (
  "id_tag" integer PRIMARY KEY,
  "title" varchar,
  "status" varchar(3)
);

CREATE TABLE "post_tags" (
  "added_at" datetime,
  "id_post" int,
  "id_tag" int
);

CREATE TABLE "post_images" (
  "added_at" datetime,
  "id_post" int,
  "id_image" int
);

COMMENT ON COLUMN "posts"."body" IS 'Content of the post';

ALTER TABLE "post_tags" ADD FOREIGN KEY ("id_post") REFERENCES "posts" ("id_post");

ALTER TABLE "post_tags" ADD FOREIGN KEY ("id_tag") REFERENCES "tags" ("id_tag");

ALTER TABLE "post_images" ADD FOREIGN KEY ("id_post") REFERENCES "posts" ("id_post");

ALTER TABLE "post_images" ADD FOREIGN KEY ("id_image") REFERENCES "images" ("id_image");