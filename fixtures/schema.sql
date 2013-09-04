BEGIN;

CREATE TABLE IF NOT EXISTS refresh_tokens (
  user_id TEXT PRIMARY KEY,
  refresh_token TEXT NOT NULL,

  UNIQUE(user_id),
  UNIQUE(refresh_token)
);

CREATE INDEX refresh_token_idx ON refresh_tokens (refresh_token);
COMMIT;
