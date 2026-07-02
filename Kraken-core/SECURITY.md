# SECURITY

## Scope

This document defines the security posture for KRAKEN as of Sprint 1. It
covers secret handling, environment configuration, and reporting practices.
It will grow as later sprints introduce networking, authentication, and
external integrations.

---

## Core Principles

1. **No hardcoded secrets.** No API keys, tokens, passwords, or credentials
   may ever be committed to source control, in code, tests, or
   documentation.
2. **Environment variables only.** All sensitive or environment-specific
   configuration is supplied via environment variables, loaded locally from
   a `.env` file that is **never** committed (see `.gitignore`).
3. **Fail closed on misconfiguration.** `config.py` validates required
   settings at startup using Pydantic. Missing or malformed configuration
   raises a clear error rather than silently defaulting to an insecure
   state.
4. **`.env.example` is the contract.** `.env.example` documents every
   supported environment variable with a placeholder, non-functional value.
   Real values live only in each developer's local, untracked `.env`.
5. **Least surface area.** Sprint 1 intentionally excludes networking,
   authentication, and any external API surface, minimizing the attack
   surface until those layers are deliberately designed.

---

## Secret Handling Rules

- Never log secret values. `logging_config.py` must not be configured to
  dump raw environment variables or full settings objects at anything above
  `DEBUG`, and even then, secret fields should be masked.
- Never print secret values to the console, including in error messages or
  stack traces.
- Never include secret values in exceptions raised from `config.py`.
- Treat every value sourced from `.env` as sensitive by default unless it is
  explicitly documented as non-sensitive in `.env.example`.

---

## Dependency Hygiene

- Dependencies are pinned in `requirements.txt` and declared in
  `pyproject.toml`.
- Only well-maintained, widely used libraries are introduced (Typer, Rich,
  Loguru, Pydantic, python-dotenv, pytest, Black, Ruff for Sprint 1).
- New dependencies must be justified in `DECISIONS.md` before being added in
  future sprints.

---

## Local Development

- Copy `.env.example` to `.env` and fill in local values only.
- `.env` is excluded from version control via `.gitignore`.
- Never share a populated `.env` file over chat, email, or tickets.

---

## Reporting a Security Issue

Since KRAKEN is an internal engineering system, security concerns should be
reported directly to the engineering lead responsible for the repository
rather than through a public issue tracker. Do not include actual secret
values in any report.

---

## Out of Scope for Sprint 1

The following security-relevant areas do not exist yet and therefore have
no controls defined yet. They will be addressed in dedicated future sprints
with their own ADRs in `DECISIONS.md`:

- Authentication and authorization
- Network transport security (TLS configuration, outbound request policy)
- Database access control and encryption at rest
- API surface hardening (rate limiting, input validation at the boundary)
- Automation / scraping legal and ethical guardrails
