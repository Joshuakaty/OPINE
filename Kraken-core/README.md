# KRAKEN

**KRAKEN** is the internal engineering foundation used to build **OPINE**
(Opportunity Intelligence Engine).

KRAKEN is **not** the product. It is the scaffolding, tooling, and
architectural backbone that OPINE and future internal systems are built on
top of. It exists to guarantee that every system built afterward starts from
a consistent, secure, well-tested, and well-documented foundation.

---

## Status

**Sprint 2 — Developer Productivity.**

Sprint 1 delivered the engineering skeleton:

- Project structure following Clean Architecture principles
- Configuration and environment handling
- Logging infrastructure
- CLI entry point with a Rich-rendered welcome screen
- Test scaffolding
- Governance documents (roadmap, architecture, security, decisions)

Sprint 2 adds developer-productivity tooling on top of that foundation:

- `kraken doctor` — environment diagnostic checks
- `kraken info` — version/environment/configuration summary
- `kraken test` — thin wrapper around `pytest`
- `kraken format` — thin wrapper around `black`
- `kraken lint` — thin wrapper around `ruff`

No product features (database, AI, scraping, automation, UI control, etc.)
exist yet. See [ROADMAP.md](ROADMAP.md) for what comes later and
[DO NOT GENERATE list in DECISIONS.md](DECISIONS.md) for explicit
out-of-scope items for this sprint.

---

## Requirements

- Python 3.13+
- pip

---

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd kraken

# Create a virtual environment
python3.13 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .

# Create your local environment file
cp .env.example .env
```

---

## Usage

Run the CLI entry point:

```bash
kraken
```

Or, without installing the console script:

```bash
python -m kraken.main
```

Show CLI help:

```bash
kraken --help
```

Show version:

```bash
kraken version
```

Check your environment is set up correctly:

```bash
kraken doctor
```

Show version, environment, and configuration at a glance:

```bash
kraken info
```

Run the test suite:

```bash
kraken test
```

Format the codebase (add `--check` to verify without modifying files):

```bash
kraken format
kraken format --check
```

Lint the codebase (add `--fix` to auto-fix fixable issues):

```bash
kraken lint
kraken lint --fix
```

---

## Project Structure

```
kraken/
├── README.md
├── ROADMAP.md
├── ARCHITECTURE.md
├── SECURITY.md
├── DECISIONS.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
├── pyproject.toml
├── src/
│   └── kraken/
│       ├── __init__.py
│       ├── __version__.py
│       ├── constants.py
│       ├── config.py
│       ├── logging_config.py
│       ├── diagnostics.py
│       ├── info.py
│       ├── devtools.py
│       ├── main.py
│       ├── cli.py
│       └── console/
│           ├── __init__.py
│           ├── welcome.py
│           ├── doctor.py
│           └── info.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_version.py
    ├── test_config.py
    ├── test_diagnostics.py
    ├── test_info.py
    ├── test_devtools.py
    └── test_cli.py
```

---

## Configuration

All configuration is provided via environment variables, loaded from a
local `.env` file (never committed) using `python-dotenv`. See
[.env.example](.env.example) for the full list of supported variables and
[SECURITY.md](SECURITY.md) for the rules around secrets handling.

---

## Development

```bash
# Run tests
pytest
# ...or via the CLI:
kraken test

# Format code
black src tests
# ...or via the CLI:
kraken format

# Lint code
ruff check src tests
# ...or via the CLI:
kraken lint

# Check your environment is set up correctly
kraken doctor
```

---

## Documentation

| Document | Purpose |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design and architectural principles |
| [SECURITY.md](SECURITY.md) | Security posture and secret handling rules |
| [DECISIONS.md](DECISIONS.md) | Architecture Decision Records (ADRs) |
| [ROADMAP.md](ROADMAP.md) | Planned sprints and future scope |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

## License

MIT — see [LICENSE](LICENSE).
