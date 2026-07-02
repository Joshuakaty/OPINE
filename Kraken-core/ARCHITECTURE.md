# ARCHITECTURE

## Purpose

KRAKEN is the engineering foundation used to build OPINE. This document
describes the architectural principles and structure established in
Sprint 1. It will be extended as later sprints add layers.

---

## Guiding Principles

1. **Clean Architecture.** Dependencies point inward. Low-level details
   (I/O, frameworks, CLI) depend on abstractions, not the other way around.
   Core logic must never import from outer layers.
2. **Modularity.** Every concern lives in its own module with a single,
   well-defined responsibility. Modules are small and composable.
3. **Security-first.** No secrets in source control. All sensitive
   configuration comes from environment variables. See `SECURITY.md`.
4. **Explicit configuration.** Configuration is validated at startup using
   Pydantic models, failing fast and loudly on misconfiguration.
5. **Observability by default.** Logging is centralized and configured once,
   at the composition root, and used consistently throughout the codebase.
6. **Typed and documented.** All public functions carry type hints and
   docstrings. Code should be self-explanatory to a new engineer.

---

## Layering (Sprint 1 scope)

Sprint 1 only establishes the outermost, framework-facing layers. There is
no domain or use-case layer yet — that arrives in a future sprint once there
is actual business logic to model.

```
┌─────────────────────────────────────────────┐
│              Entry Points                    │
│   src/kraken/main.py   (composition root)     │
│   src/kraken/cli.py    (Typer CLI)            │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│           Cross-Cutting Infrastructure        │
│  src/kraken/config.py            (settings)   │
│  src/kraken/logging_config.py    (logging)    │
│  src/kraken/diagnostics.py       (doctor)     │
│  src/kraken/info.py              (info)       │
│  src/kraken/devtools.py          (test/fmt/   │
│                                    lint)       │
│  src/kraken/console/welcome.py   (UI/output)  │
│  src/kraken/console/doctor.py    (UI/output)  │
│  src/kraken/console/info.py      (UI/output)  │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│                 Foundation                    │
│  src/kraken/constants.py                      │
│  src/kraken/__version__.py                    │
└─────────────────────────────────────────────┘
```

- **Entry points** (`main.py`, `cli.py`) are the only modules allowed to
  wire concrete implementations together (the "composition root" pattern).
- **Infrastructure** modules (`config.py`, `logging_config.py`) provide
  cross-cutting services consumed by entry points and, later, by domain
  and application layers.
- **Foundation** modules hold static values with no behavior and no
  dependencies on the rest of the application.

As OPINE's domain logic is introduced in future sprints, this document will
be updated to describe the `domain/`, `application/`, and `infrastructure/`
layers in full Clean Architecture form (entities, use cases, interface
adapters, frameworks/drivers).

---

## Module Responsibilities

| Module | Responsibility |
|---|---|
| `kraken/__version__.py` | Single source of truth for the package version. |
| `kraken/constants.py` | Static, non-secret project-wide constants. |
| `kraken/config.py` | Loads and validates environment-based settings. |
| `kraken/logging_config.py` | Configures Loguru sinks, format, and level. |
| `kraken/diagnostics.py` | Runs environment/config checks for `kraken doctor`. |
| `kraken/info.py` | Gathers the version/environment snapshot for `kraken info`. |
| `kraken/devtools.py` | Subprocess wrappers around pytest/black/ruff for `kraken test`/`format`/`lint`. |
| `kraken/console/welcome.py` | Renders the Rich welcome screen. |
| `kraken/console/doctor.py` | Renders the `kraken doctor` diagnostic report. |
| `kraken/console/info.py` | Renders the `kraken info` summary panel. |
| `kraken/cli.py` | Defines the Typer CLI surface (commands, options). |
| `kraken/main.py` | Composition root / application entry point. |

---

## Data Flow (Sprint 2)

1. `main.py` (or the `kraken` console script) is invoked.
2. `cli.py` builds the Typer application and parses arguments.
3. On any command invocation, `config.py` loads and validates settings from
   the environment (via `.env` in local development).
4. `logging_config.py` configures Loguru sinks based on those settings.
5. The requested command executes:
   - No subcommand / `version` — as in Sprint 1
     (`console/welcome.py`, `__version__.py`).
   - `doctor` — `diagnostics.py` runs the checks, `console/doctor.py`
     renders the pass/fail report.
   - `info` — `info.py` gathers the snapshot, `console/info.py` renders it.
   - `test` / `format` / `lint` — `devtools.py` shells out to pytest,
     black, or ruff and returns their exit code.

---

## Testing Strategy

- Unit tests live in `tests/`, mirroring the `src/kraken/` package layout.
- `pytest` is the test runner; fixtures are centralized in
  `tests/conftest.py`.
- Sprint 1 tests cover configuration loading and version metadata.
- Sprint 2 tests cover diagnostic checks (`test_diagnostics.py`), the info
  snapshot (`test_info.py`), the pytest/black/ruff subprocess wrappers with
  `subprocess.run` monkeypatched (`test_devtools.py`), and CLI wiring via
  Typer's `CliRunner` (`test_cli.py`).

---

## Future Evolution

As sprints progress, this document will be extended — not rewritten — to
add:

- `domain/` — entities and business rules for OPINE
- `application/` — use cases orchestrating domain logic
- `infrastructure/` — persistence, networking, external integrations
- `interfaces/` — adapters exposing the application (CLI, API, UI)

Each addition will be recorded as an ADR in `DECISIONS.md`.
