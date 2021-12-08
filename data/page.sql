CREATE TABLE IF NOT EXISTS "clip"(
  "id" TEXT,
  "created" TEXT,
  "modified" TEXT,
  "name" TEXT,
  "description" TEXT,
  "source_id" TEXT,
  "icon" TEXT,
  "season_number" TEXT,
  "disc_number" TEXT,
  "credit_id" TEXT,
  "embed_id" TEXT
);
CREATE TABLE IF NOT EXISTS "clipsegment"(
  "id" TEXT,
  "start_hours" TEXT,
  "start_minutes" TEXT,
  "start_seconds" TEXT,
  "end_hours" TEXT,
  "end_minutes" TEXT,
  "end_seconds" TEXT
);
CREATE TABLE IF NOT EXISTS "cliptag"(
  "id" TEXT,
  "name" TEXT,
  "slug" TEXT,
  "description" TEXT
);
CREATE TABLE IF NOT EXISTS "taggedclip"(
  "id" TEXT,
  "object_id" TEXT,
  "content_type_id" TEXT,
  "tag_id" TEXT
);
CREATE TABLE IF NOT EXISTS "clip_segments"(
  "id" TEXT,
  "clip_id" TEXT,
  "clipsegment_id" TEXT
);
CREATE TABLE IF NOT EXISTS "clipsource"(
  "id" TEXT,
  "title" TEXT,
  "slug" TEXT,
  "description" TEXT,
  "source_type" TEXT
);
CREATE TABLE IF NOT EXISTS "contributor"(
  "id" TEXT,
  "first_name" TEXT,
  "last_name" TEXT,
  "institution" TEXT
);
