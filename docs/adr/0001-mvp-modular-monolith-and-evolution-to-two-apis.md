# ADR 0001 — MVP modular monolith and evolution to two APIs

- **Date:** 2026-04-16
- **Status:** Accepted
- **Deciders:** Team / mentor guidance incorporated
- **Technical story:** [`docs/architecture.md`](../architecture.md)

## Context

SmartTicket needs to ingest tickets (including ML classification), persist state, and let attendants work through a UI. A single service doing everything creates **operational coupling**: deploys and failures on the ingestion/ML path can affect attendant-facing reads if they share one process and are not carefully isolated.

The team also discussed **load balancers and multiple replicas**: they improve instance-level availability but do not replace **logical** separation between intake/orchestration and query/UI traffic.

## Decision

1. **MVP:** Ship a **modular monolith** — one FastAPI application and one primary deployable, with **explicit modules** for:
   - **Ingestion & processing** (webhooks, pipeline, ML, writes).
   - **Query & attendant workflows** (reads and manual updates backed by the database).

   Internal boundaries (routers, services) should make a future split a **structural** change (new entrypoints / containers), not a domain rewrite.

2. **Post-MVP evolution:** Move to **two APIs** (two deployables):
   - **Ingestion API** — receives tickets, orchestrates preprocessing and ML (or async workers), persists authoritative data.
   - **Query API** — serves the attendant/UI layer with read-optimized access to the database (and optional cache), **without** requiring the inference stack on the hot path.

3. **When to split:** Revisit when **blast radius**, **independent scaling**, **deploy frequency**, or **team ownership** clearly favor separate services; until then, the modular monolith is the default.

## Consequences

- **Positive:** Faster MVP delivery, simpler CI/CD and observability, clear documented path to microservices.
- **Positive:** Code organized for **ingest vs query** mirrors the future two-API topology.
- **Trade-off:** A single process still shares fate on **catastrophic** failures (OOM, bad deploy) until the split; mitigate with careful ML isolation, health checks, and multi-replica rollouts when available.
- **Documentation:** Architectural narrative lives in `docs/architecture.md`; future ADRs should capture concrete choices (queues, auth split, DB read replicas).

## Branch workflow note (2026-04-16)

Architecture documentation that was expanded locally on `main` was **restored on `main`** to match `origin/main`, and the **consolidated** document (including this decision) was committed on **`develop`**, which is ahead of `main` and is the integration branch for ongoing work.
