-- SmartTicket: add urgency tier + LLM/human queue routing columns.
-- Apply against PostgreSQL (e.g. Railway). SQLite tests use SQLAlchemy metadata instead.

ALTER TABLE tickets
  ADD COLUMN IF NOT EXISTS urgency VARCHAR(32) NOT NULL DEFAULT 'MEDIUM';

ALTER TABLE tickets
  ADD COLUMN IF NOT EXISTS queue_target VARCHAR(32) NOT NULL DEFAULT 'human';

COMMENT ON COLUMN tickets.urgency IS 'HIGH | MEDIUM | LOW — tiered queue ordering';
COMMENT ON COLUMN tickets.queue_target IS 'human | llm — routing from classification score vs SMARTTICKET_LLM_MIN_SCORE';
