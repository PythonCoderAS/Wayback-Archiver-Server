-- upgrade --
CREATE TABLE IF NOT EXISTS "host" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "hostname" VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS "session" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_on" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "host_id" INT NOT NULL REFERENCES "host" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_session_host_id_566edc" ON "session" ("host_id");
CREATE TABLE IF NOT EXISTS "sessionitem" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_on" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "url" TEXT NOT NULL,
    "session_id" INT NOT NULL REFERENCES "session" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_sessionitem_session_2dd848" ON "sessionitem" ("session_id");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
