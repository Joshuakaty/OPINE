"""FastAPI application for OPINE."""

from fastapi import FastAPI

app = FastAPI(
    title="OPINE API",
    version="0.4.0",
    description="Opportunity Intelligence Engine API",
)


@app.get("/")
def root() -> dict[str, str]:
    """Health endpoint."""
    return {
        "name": "OPINE API",
        "status": "running",
        "engine": "Kraken",
    }