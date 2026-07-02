# ROADMAP

This document tracks the high-level, sprint-based evolution of KRAKEN as the
foundation for OPINE (Opportunity Intelligence Engine). It exists so that
scope is always explicit: what is built now, and what is deliberately
deferred.

Sprints are additive. Each sprint must be complete, tested, and documented
before the next begins.

---

## Sprint 1 — Foundation (Current)

**Goal:** Establish a production-quality engineering skeleton.

- Professional project structure (Clean Architecture layout)
- Governance docs: README, ARCHITECTURE, SECURITY, DECISIONS, CHANGELOG
- MIT license, `.gitignore`, `.env.example`
- Dependency and tooling configuration (`requirements.txt`, `pyproject.toml`)
- Version module and project constants
- Environment-based configuration loader (Pydantic + python-dotenv)
- Centralized logging configuration (Loguru)
- CLI entry point (Typer) with a Rich welcome screen
- Starter unit test suite (pytest)

**Explicitly out of scope for Sprint 1:** database layer, AI integration,
memory/persistence, prompt generation, code review tooling, automation,
networking, authentication, any API layer, desktop UI, mouse/keyboard
control, the Opportunity Engine itself, and scrapers.

---

## Sprint 2 — Developer Productivity (Complete)

**Goal:** Give contributors a single, discoverable entry point for common
developer workflows, built entirely on top of Sprint 1's foundation.

- `kraken doctor` — environment diagnostic checks (Python version, required
  dependencies, configuration, log directory)
- `kraken info` — version/environment/configuration summary
- `kraken test` — thin CLI wrapper around `pytest`
- `kraken format` — thin CLI wrapper around `black` (with `--check`)
- `kraken lint` — thin CLI wrapper around `ruff` (with `--fix`)

**Explicitly out of scope for Sprint 2:** the core domain layer for OPINE,
database layer, AI integration, memory/persistence, prompt generation, code
review tooling, automation, networking, authentication, any API layer,
desktop UI, mouse/keyboard control, the Opportunity Engine itself, and
scrapers — same boundaries as Sprint 1.

---

## Sprint 3 — Planned (Not Started)

Tentative focus: core domain layer for OPINE — domain models and use-case
interfaces only, still without persistence or external I/O.

---

## Sprint 4+ — Future (Not Scoped)

Later sprints will introduce, in an order to be decided closer to the time:

- Persistence / database layer
- Authentication and access control
- Networking and external API integrations
- AI/LLM integration and prompt generation
- Memory and context management
- Automation and scraping capabilities
- The Opportunity Intelligence Engine itself
- Desktop UI and input control (mouse/keyboard)
- Code review tooling

No implementation work for these areas exists yet. Their design will be
addressed in dedicated future sprints and recorded in this roadmap and in
`DECISIONS.md` when scoped.
