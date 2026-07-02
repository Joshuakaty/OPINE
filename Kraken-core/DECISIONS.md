# DECISIONS

Architecture Decision Records (ADRs) for KRAKEN. Each record captures a
significant decision, its context, and its consequences. Records are never
deleted or rewritten after the fact — superseding decisions get their own
new entry that references the old one.

---

## ADR-001: KRAKEN is infrastructure, not the product

**Status:** Accepted (Sprint 1)

**Context:** The eventual product is OPINE (Opportunity Intelligence
Engine). Without a clear boundary, engineering scaffolding tends to blend
with product code, making both harder to reason about.

**Decision:** KRAKEN is scoped strictly as the internal engineering
foundation — tooling, architecture, configuration, logging, CLI — that
OPINE and future systems are built on top of. Product-specific logic
(the Opportunity Engine, scrapers, AI features) will live in separate,
clearly bounded modules or packages introduced in later sprints, never
merged into KRAKEN's foundational layer.

**Consequences:** Sprint boundaries stay clean. Future contributors can
reason about "is this KRAKEN or is this OPINE" unambiguously.

---

## ADR-002: Clean Architecture as the structural baseline

**Status:** Accepted (Sprint 1)

**Context:** OPINE will eventually have real domain logic, external
integrations, and multiple interfaces (CLI, possibly API/UI later).
Coupling business logic to frameworks early creates expensive rework.

**Decision:** Adopt Clean Architecture principles from Sprint 1 onward,
even though Sprint 1 only contains the outer layers (entry points and
infrastructure). Dependencies point inward; entry points act as the sole
composition roots.

**Consequences:** Slightly more structure than a minimal script would need
up front, in exchange for a codebase that can absorb a domain layer later
without a rewrite.

---

## ADR-003: Environment-variable-only configuration

**Status:** Accepted (Sprint 1)

**Context:** Secrets and environment-specific values must never be
committed to source control.

**Decision:** All configuration is sourced from environment variables,
loaded via `python-dotenv` in local development and validated with a
Pydantic settings model (`kraken/config.py`). `.env.example` documents every
supported variable; `.env` is gitignored.

**Consequences:** Onboarding requires copying `.env.example` to `.env`.
Misconfiguration fails fast with a validation error instead of silently
running with bad defaults.

---

## ADR-004: Loguru for logging

**Status:** Accepted (Sprint 1)

**Context:** The standard library `logging` module requires significant
boilerplate to get sensible formatting, rotation, and structured output.

**Decision:** Use Loguru, configured once in `kraken/logging_config.py` and
imported wherever logging is needed.

**Consequences:** Simpler, more consistent logging setup at the cost of an
additional dependency. Log level and sink behavior are driven by
`config.py` settings, not hardcoded.

---

## ADR-005: Typer + Rich for the CLI surface

**Status:** Accepted (Sprint 1)

**Context:** Sprint 1 needs a real, usable entry point to prove the
foundation works end-to-end, without building product features.

**Decision:** Use Typer for CLI command definition and argument parsing,
and Rich for terminal output (the welcome screen). No other user interface
is introduced in Sprint 1.

**Consequences:** Establishes the CLI as the primary interface for now.
Any future API or desktop UI (explicitly out of scope for Sprint 1) will be
introduced as a separate interface adapter, not a replacement of the CLI.

---

## ADR-006: Sprint-scoped, additive delivery

**Status:** Accepted (Sprint 1)

**Context:** Large, ambiguous scope ("build OPINE") invites scope creep and
half-finished modules.

**Decision:** Work is delivered in explicit, self-contained sprints.
Sprint 1 delivers only the foundation listed in `ROADMAP.md`. No
placeholder implementations for future modules (database, AI, scrapers,
etc.) are created ahead of their sprint.

**Consequences:** Some familiar project files (e.g. a `domain/` package)
will simply not exist until the sprint that needs them. This is
intentional, not an oversight.

---

## ADR-007: Developer-productivity commands wrap existing tools, not reimplement them

**Status:** Accepted (Sprint 2)

**Context:** Sprint 2 needed `kraken test`, `kraken format`, and
`kraken lint` commands. KRAKEN already depends on `pytest`, `black`, and
`ruff` (see `pyproject.toml`'s `dev` extra). Reimplementing test running,
formatting, or linting would duplicate mature, well-maintained tools for no
benefit.

**Decision:** `kraken/devtools.py` shells out to the existing `pytest`,
`black`, and `ruff` executables via `subprocess.run`, streaming their
output directly and propagating their exit codes. `kraken doctor` and
`kraken info` follow the same split used elsewhere in the codebase: a
plain-data module (`diagnostics.py`, `info.py`) with no console I/O, and a
`console/` module (`doctor.py`, `info.py`) responsible only for rendering,
mirroring the existing `console/welcome.py` pattern.

**Consequences:** `kraken test`/`format`/`lint` behave identically to
running the underlying tools directly — same output, same exit codes — so
there is no second implementation to keep in sync. This does mean those
three commands require `pytest`, `black`, and `ruff` to be installed
(already true for any Sprint 1 checkout that installed the `dev` extra).
