-- upgrade --
ALTER TABLE "host" ADD "created_on" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
-- downgrade --
ALTER TABLE "host" DROP COLUMN "created_on";
