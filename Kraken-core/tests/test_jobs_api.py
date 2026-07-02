"""Tests for the jobs API endpoint."""

from fastapi.testclient import TestClient

from kraken.api.main import app

client = TestClient(app)


def test_get_jobs() -> None:
    response = client.get("/jobs")

    assert response.status_code == 200

    jobs = response.json()

    assert len(jobs) == 2
    assert jobs[0]["title"] == "Software Engineer"
    assert jobs[0]["score"] == 100
    assert jobs[1]["title"] == "Backend Python Developer"
    assert jobs[1]["score"] == 80