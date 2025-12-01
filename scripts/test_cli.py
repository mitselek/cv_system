#!/usr/bin/env python3
"""Tests for job_monitor CLI commands."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from click.testing import CliRunner
from pydantic import HttpUrl

from job_monitor import cli
from schemas import JobPosting, JobStatus, ScoredJob
from state_manager import StateManager


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def test_config(tmp_path: Path) -> Path:
    """Create a test configuration file."""
    config_content = """sources:
  - name: duunitori.fi
    enabled: true
    queries:
      - keywords: python developer
        location: helsinki
        limit: 5

scoring:
  positive_keywords:
    - python
    - django
  negative_keywords:
    - java
  required_keywords: []
  preferred_companies: []
  blocked_companies: []
  preferred_locations:
    - remote
  remote_bonus: 15
  days_threshold_fresh: 7
  days_threshold_old: 30

state_file: {state_file}
candidates_dir: {candidates_dir}
scan_interval_hours: 24
auto_archive_days: 60
"""
    config_path = tmp_path / "test_config.yaml"
    state_file = tmp_path / "state.json"
    candidates_dir = tmp_path / "candidates"
    
    config_content = config_content.format(
        state_file=state_file,
        candidates_dir=candidates_dir
    )
    config_path.write_text(config_content)
    return config_path


@pytest.fixture
def test_candidates(tmp_path: Path) -> Path:
    """Create test candidate files."""
    candidates_dir = tmp_path / "candidates"
    today = datetime.now().strftime("%Y-%m-%d")
    day_dir = candidates_dir / today
    
    # Create high priority candidate
    high_dir = day_dir / "high_priority"
    high_dir.mkdir(parents=True, exist_ok=True)
    
    job1 = JobPosting(
        title="Senior Python Developer",
        company="Tech Corp",
        location="Remote",
        url=HttpUrl("https://example.com/job1"),
        source="duunitori.fi",
        discovered_date=datetime.now(timezone.utc)
    )
    sj1 = ScoredJob(job=job1, score=85.0)
    
    with open(high_dir / f"{job1.id}.json", "w") as f:
        json.dump(sj1.model_dump(mode="json"), f, indent=2)
    
    # Create review candidate
    review_dir = day_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    
    job2 = JobPosting(
        title="Python Developer",
        company="Startup Inc",
        location="Helsinki",
        url=HttpUrl("https://example.com/job2"),
        source="duunitori.fi",
        discovered_date=datetime.now(timezone.utc)
    )
    sj2 = ScoredJob(job=job2, score=55.0)
    
    with open(review_dir / f"{job2.id}.json", "w") as f:
        json.dump(sj2.model_dump(mode="json"), f, indent=2)
    
    return candidates_dir


def test_cli_help(runner: CliRunner) -> None:
    """Test CLI main help output."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Job monitoring and application management system" in result.output
    assert "scan" in result.output
    assert "review" in result.output
    assert "stats" in result.output
    assert "mark" in result.output
    assert "cleanup" in result.output
    assert "init" in result.output


def test_cli_version(runner: CliRunner) -> None:
    """Test CLI version output."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.output


def test_scan_help(runner: CliRunner) -> None:
    """Test scan command help."""
    result = runner.invoke(cli, ["scan", "--help"])
    assert result.exit_code == 0
    assert "Scan enabled job sources" in result.output
    assert "--config" in result.output
    assert "--dry-run" in result.output
    assert "--force" in result.output


def test_scan_dry_run(runner: CliRunner, test_config: Path) -> None:
    """Test scan command with --dry-run."""
    result = runner.invoke(cli, ["scan", "--config", str(test_config), "--dry-run"])
    assert "Dry-run: not saving state or candidates" in result.output


def test_review_help(runner: CliRunner) -> None:
    """Test review command help."""
    result = runner.invoke(cli, ["review", "--help"])
    assert result.exit_code == 0
    assert "Review candidate jobs" in result.output
    assert "--category" in result.output
    assert "--min-score" in result.output
    assert "--source" in result.output
    assert "--date" in result.output


def test_review_no_candidates(runner: CliRunner, test_config: Path) -> None:
    """Test review command with no candidates."""
    result = runner.invoke(cli, ["review", "--config", str(test_config)])
    assert "No candidates found" in result.output or "No candidates match" in result.output


def test_review_with_candidates(runner: CliRunner, tmp_path: Path, test_candidates: Path) -> None:
    """Test review command with actual candidates."""
    config_path = tmp_path / "test_config.yaml"
    config_content = f"""sources:
  - name: duunitori.fi
    enabled: true
    queries:
      - keywords: python
        limit: 5

scoring:
  positive_keywords: [python]
  negative_keywords: []
  required_keywords: []
  preferred_companies: []
  blocked_companies: []
  preferred_locations: [remote]
  remote_bonus: 15
  days_threshold_fresh: 7
  days_threshold_old: 30

state_file: {tmp_path / "state.json"}
candidates_dir: {test_candidates}
scan_interval_hours: 24
auto_archive_days: 60
"""
    config_path.write_text(config_content)
    
    result = runner.invoke(cli, ["review", "--config", str(config_path), "--category", "all"])
    assert result.exit_code == 0
    assert "Senior Python Developer" in result.output or "Python Developer" in result.output


def test_stats_help(runner: CliRunner) -> None:
    """Test stats command help."""
    result = runner.invoke(cli, ["stats", "--help"])
    assert result.exit_code == 0
    assert "Show monitoring statistics" in result.output
    assert "--config" in result.output


def test_stats_empty_state(runner: CliRunner, test_config: Path) -> None:
    """Test stats command with empty state."""
    result = runner.invoke(cli, ["stats", "--config", str(test_config)])
    assert result.exit_code == 0
    assert "Job Monitoring Statistics" in result.output
    assert "Last Scan: Never" in result.output
    assert "Total Jobs Seen: 0" in result.output


def test_stats_with_data(runner: CliRunner, tmp_path: Path) -> None:
    """Test stats command with state data."""
    state_file = tmp_path / "state.json"
    config_path = tmp_path / "test_config.yaml"
    
    # Create state with data
    sm = StateManager(state_file)
    job = JobPosting(
        title="Test Job",
        company="Test Co",
        location="Test City",
        url=HttpUrl("https://example.com/test"),
        source="duunitori.fi",
        discovered_date=datetime.now(timezone.utc)
    )
    sm.add_job(job)
    sm.touch_scan_time()
    sm.save_state()
    
    # Create config
    config_content = f"""sources:
  - name: duunitori.fi
    enabled: true
    queries:
      - keywords: python
        limit: 5

scoring:
  positive_keywords: [python]
  negative_keywords: []
  required_keywords: []
  preferred_companies: []
  blocked_companies: []
  preferred_locations: [remote]
  remote_bonus: 15
  days_threshold_fresh: 7
  days_threshold_old: 30

state_file: {state_file}
candidates_dir: {tmp_path / "candidates"}
scan_interval_hours: 24
auto_archive_days: 60
"""
    config_path.write_text(config_content)
    
    result = runner.invoke(cli, ["stats", "--config", str(config_path)])
    assert result.exit_code == 0
    assert "Job Monitoring Statistics" in result.output
    assert "Total Jobs Seen: 1" in result.output


def test_mark_help(runner: CliRunner) -> None:
    """Test mark command help."""
    result = runner.invoke(cli, ["mark", "--help"])
    assert result.exit_code == 0
    assert "Mark a job with a new status" in result.output
    assert "--config" in result.output


def test_mark_job_not_found(runner: CliRunner, test_config: Path) -> None:
    """Test mark command with non-existent job."""
    result = runner.invoke(cli, ["mark", "nonexistent", "candidate", "--config", str(test_config)])
    assert result.exit_code == 1
    assert "not found" in result.output


def test_mark_job_candidate(runner: CliRunner, tmp_path: Path) -> None:
    """Test marking a job as candidate."""
    state_file = tmp_path / "state.json"
    config_path = tmp_path / "test_config.yaml"
    
    # Create state with a job
    sm = StateManager(state_file)
    job = JobPosting(
        title="Test Job",
        company="Test Co",
        location="Test City",
        url=HttpUrl("https://example.com/test"),
        source="duunitori.fi",
        discovered_date=datetime.now(timezone.utc)
    )
    sm.add_job(job)
    sm.save_state()
    
    # Create config
    config_content = f"""sources:
  - name: duunitori.fi
    enabled: true
    queries:
      - keywords: python
        limit: 5

scoring:
  positive_keywords: [python]
  negative_keywords: []
  required_keywords: []
  preferred_companies: []
  blocked_companies: []
  preferred_locations: [remote]
  remote_bonus: 15
  days_threshold_fresh: 7
  days_threshold_old: 30

state_file: {state_file}
candidates_dir: {tmp_path / "candidates"}
scan_interval_hours: 24
auto_archive_days: 60
"""
    config_path.write_text(config_content)
    
    result = runner.invoke(cli, ["mark", job.id, "candidate", "--config", str(config_path)])
    assert result.exit_code == 0
    assert "Marked job" in result.output
    assert "candidate" in result.output


def test_cleanup_help(runner: CliRunner) -> None:
    """Test cleanup command help."""
    result = runner.invoke(cli, ["cleanup", "--help"])
    assert result.exit_code == 0
    assert "Archive old jobs" in result.output
    assert "--days" in result.output
    assert "--dry-run" in result.output


def test_cleanup_dry_run(runner: CliRunner, test_config: Path) -> None:
    """Test cleanup command with --dry-run."""
    result = runner.invoke(cli, ["cleanup", "--config", str(test_config), "--dry-run", "--days", "30"])
    assert result.exit_code == 0
    assert "Would archive" in result.output


def test_cleanup_archive_jobs(runner: CliRunner, tmp_path: Path) -> None:
    """Test cleanup command actually archives old jobs."""
    state_file = tmp_path / "state.json"
    config_path = tmp_path / "test_config.yaml"
    
    # Create state with old job
    sm = StateManager(state_file)
    old_date = datetime(2020, 1, 1, tzinfo=timezone.utc)
    job = JobPosting(
        title="Old Job",
        company="Test Co",
        location="Test City",
        url=HttpUrl("https://example.com/old"),
        source="duunitori.fi",
        discovered_date=old_date
    )
    sm.add_job(job)
    sm.save_state()
    
    # Create config
    config_content = f"""sources:
  - name: duunitori.fi
    enabled: true
    queries:
      - keywords: python
        limit: 5

scoring:
  positive_keywords: [python]
  negative_keywords: []
  required_keywords: []
  preferred_companies: []
  blocked_companies: []
  preferred_locations: [remote]
  remote_bonus: 15
  days_threshold_fresh: 7
  days_threshold_old: 30

state_file: {state_file}
candidates_dir: {tmp_path / "candidates"}
scan_interval_hours: 24
auto_archive_days: 60
"""
    config_path.write_text(config_content)
    
    result = runner.invoke(cli, ["cleanup", "--config", str(config_path), "--days", "30"])
    assert result.exit_code == 0
    assert "Archived 1 jobs" in result.output


def test_init_help(runner: CliRunner) -> None:
    """Test init command help."""
    result = runner.invoke(cli, ["init", "--help"])
    assert result.exit_code == 0
    assert "Create a configuration file template" in result.output
    assert "--output" in result.output


def test_init_creates_config(runner: CliRunner, tmp_path: Path) -> None:
    """Test init command creates configuration template."""
    output_path = tmp_path / "new_config.yaml"
    result = runner.invoke(cli, ["init", "--output", str(output_path)])
    assert result.exit_code == 0
    assert "Created configuration template" in result.output
    assert output_path.exists()
    
    content = output_path.read_text()
    assert "sources:" in content
    assert "scoring:" in content
    assert "positive_keywords:" in content


def test_init_overwrite_prompt(runner: CliRunner, tmp_path: Path) -> None:
    """Test init command prompts for overwrite."""
    output_path = tmp_path / "existing_config.yaml"
    output_path.write_text("existing content")
    
    # Answer "n" to overwrite prompt
    result = runner.invoke(cli, ["init", "--output", str(output_path)], input="n\n")
    assert result.exit_code == 0
    assert "Aborted" in result.output
    assert output_path.read_text() == "existing content"
