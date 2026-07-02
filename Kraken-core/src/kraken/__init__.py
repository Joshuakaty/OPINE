"""KRAKEN — internal engineering foundation for building OPINE.

KRAKEN is not the product itself. It is the engineering scaffolding
(configuration, logging, CLI, tooling) that OPINE (Opportunity Intelligence
Engine) and future internal systems are built on top of.

This package intentionally contains no product/domain logic in Sprint 1.
See ROADMAP.md and DECISIONS.md at the repository root for scope details.
"""

from .__version__ import __version__

__all__ = ["__version__"]
