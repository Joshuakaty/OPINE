"""Tests for collection commands."""

from kraken.console.collect import collect_jobs


def test_collect_jobs(capsys) -> None:
    collect_jobs()

    output = capsys.readouterr().out

    assert "Collected 2 opportunities" in output
    assert "Software Engineer" in output
    assert "Backend Python Developer" in output