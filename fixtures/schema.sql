BEGIN;

CREATE TABLE IF NOT EXISTS refesh_tokens (
  user_id TEXT PRIMARY KEY,
  refresh_token TEXT NOT NULL,

  UNIQUE(user_id, refresh_token)
);

CREATE INDEX refresh_token_idx ON refesh_tokens (refresh_token);
COMMIT;
