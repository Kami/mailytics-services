BEGIN;

CREATE TABLE IF NOT EXISTS refresh_tokens (
  account_uuid TEXT PRIMARY KEY,
  refresh_token TEXT NOT NULL,

  UNIQUE(account_uuid),
  UNIQUE(refresh_token)
);

CREATE INDEX IF NOT EXISTS refresh_token_idx ON refresh_tokens (refresh_token);
COMMIT;
