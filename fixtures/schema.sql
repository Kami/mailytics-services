BEGIN;

CREATE TABLE IF NOT EXISTS refresh_tokens (
  user_id TEXT PRIMARY KEY,
  refresh_token TEXT NOT NULL,

  UNIQUE(user_id),
  UNIQUE(refresh_token)
);

CREATE INDEX refresh_token_idx ON refresh_tokens (refresh_token);
COMMIT;

BEGIN;
CREATE TABLE IF NOT EXISTS access_tokens_cache (
  user_id TEXT PRIMARY KEY,
  access_token TEXT NOT NULL,
  expires_at INTEGER NOT NULL,

  UNIQUE(user_id)
);

COMMIT;
