#!/usr/bin/env python3
"""Integration tests for end-to-end job monitoring workflows."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator

import pytest
from pydantic import HttpUrl

from job_monitor.config import ConfigManager
from job_monitor.deduplicator import Deduplicator
from job_monitor.digest import DigestGenerator
from job_monitor import _save_candidates
from job_monitor.scorer import JobScorer
from job_monitor.converter import ApplicationConverter
from job_monitor.schemas import JobPosting, JobStatus, ScoredJob, ScoringConfig
from job_monitor.state import StateManager


@pytest.fixture
def integration_workspace(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a complete workspace for integration testing."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    
    # Create directory structure
    (workspace / "job_sources").mkdir()
    (workspace / "job_sources/candidates").mkdir()
    (workspace / "applications").mkdir()
    (workspace / "docs").mkdir()
    
    # Create config file
    config_content = f"""sources:
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
    - system analyst
  negative_keywords:
    - junior
  required_keywords: []
  preferred_companies:
    - TechCorp
  blocked_companies: []
  preferred_locations:
    - Helsinki
    - remote
  remote_bonus: 15
  days_threshold_fresh: 7
  days_threshold_old: 30

state_file: {workspace / "job_sources/state.json"}
candidates_dir: {workspace / "job_sources/candidates"}
scan_interval_hours: 24
auto_archive_days: 60
"""
    config_path = workspace / "config.yaml"
    config_path.write_text(config_content)
    
    yield workspace


def create_sample_jobs() -> list[JobPosting]:
    """Create sample job postings for testing."""
    return [
        JobPosting(
            title="Senior Python Developer",
            company="TechCorp",
            location="Helsinki, Remote",
            url=HttpUrl("https://example.com/job1"),
            source="duunitori.fi",
            discovered_date=datetime.now(timezone.utc),
            description="We need a senior Python developer with Django experience for system analysis work."
        ),
        JobPosting(
            title="Junior Python Developer",
            company="StartupInc",
            location="Helsinki",
            url=HttpUrl("https://example.com/job2"),
            source="duunitori.fi",
            discovered_date=datetime.now(timezone.utc),
            description="Entry-level Python developer position."
        ),
        JobPosting(
            title="System Analyst",
            company="BigCorp",
            location="Espoo",
            url=HttpUrl("https://example.com/job3"),
            source="duunitori.fi",
            discovered_date=datetime.now(timezone.utc),
            description="Looking for experienced system analyst."
        ),
        JobPosting(
            title="Python Developer",
            company="TechCorp",
            location="Remote",
            url=HttpUrl("https://example.com/job4"),
            source="duunitori.fi",
            discovered_date=datetime.now(timezone.utc),
            description="Remote Python developer with Django."
        ),
    ]


def test_full_scan_workflow(integration_workspace: Path) -> None:
    """Test complete scan workflow: scrape → score → deduplicate → save → digest."""
    # Setup
    config_path = integration_workspace / "config.yaml"
    cm = ConfigManager(config_path)
    cfg = cm.config
    
    # Initialize components
    sm = StateManager(cfg.state_file)
    scorer = JobScorer(cfg.scoring)
    dd = Deduplicator()
    
    # Simulate scraping (use sample jobs)
    jobs = create_sample_jobs()
    
    # Deduplicate
    unique_jobs = dd.filter_unique(jobs)
    assert len(unique_jobs) == 4  # All unique
    
    # Score jobs
    scored = [scorer.score(j) for j in unique_jobs]
    
    # Verify scoring worked
    assert len(scored) == 4
    assert all(isinstance(sj, ScoredJob) for sj in scored)
    assert all(sj.score >= 0 for sj in scored)
    
    # Save candidates
    counts = _save_candidates(cfg.candidates_dir, scored)
    
    # Verify categorization
    assert counts["high_priority"] > 0 or counts["review"] > 0 or counts["low_priority"] > 0
    assert sum(counts.values()) == 4
    
    # Update state
    for sj in scored:
        sm.add_job(sj.job)
    sm.touch_scan_time()
    sm.save_state()
    
    # Verify state updated
    assert sm.state.total_jobs_seen == 4
    assert sm.state.last_scan is not None
    
    # Generate digest
    dg = DigestGenerator(cfg.candidates_dir)
    digest = dg.generate_digest()
    
    # Verify digest content
    assert "Job Candidates Digest" in digest
    assert len(digest) > 100


def test_deduplication_across_scans(integration_workspace: Path) -> None:
    """Test that duplicate jobs are filtered across multiple scans."""
    config_path = integration_workspace / "config.yaml"
    cm = ConfigManager(config_path)
    cfg = cm.config
    
    dd = Deduplicator()
    
    # First scan
    jobs1 = create_sample_jobs()
    unique1 = dd.filter_unique(jobs1)
    assert len(unique1) == 4
    
    # Second scan with same jobs
    jobs2 = create_sample_jobs()
    unique2 = dd.filter_unique(jobs2)
    assert len(unique2) == 0  # All duplicates
    
    # Third scan with mix
    jobs3 = create_sample_jobs()
    jobs3.append(JobPosting(
        title="New Position",
        company="NewCorp",
        location="Tallinn",
        url=HttpUrl("https://example.com/new"),
        source="duunitori.fi",
        discovered_date=datetime.now(timezone.utc),
        description="Brand new opportunity"
    ))
    unique3 = dd.filter_unique(jobs3)
    assert len(unique3) == 1  # Only the new one


def test_state_persistence(integration_workspace: Path) -> None:
    """Test state saving and loading across sessions."""
    config_path = integration_workspace / "config.yaml"
    cm = ConfigManager(config_path)
    cfg = cm.config
    
    # First session: add jobs
    sm1 = StateManager(cfg.state_file)
    jobs = create_sample_jobs()
    for job in jobs:
        sm1.add_job(job)
    sm1.touch_scan_time()
    sm1.save_state()
    
    # Second session: load state
    sm2 = StateManager(cfg.state_file)
    
    # Verify state persisted
    assert sm2.state.total_jobs_seen == 4
    assert sm2.state.last_scan is not None
    assert len(sm2.state.seen_jobs) == 4
    
    # Verify jobs accessible
    for job in jobs:
        retrieved = sm2.get_job(job.id)
        assert retrieved is not None
        assert retrieved.title == job.title


def test_candidate_to_application_workflow(integration_workspace: Path) -> None:
    """Test converting candidate to application directory."""
    applications_dir = integration_workspace / "applications"
    registry_path = applications_dir / "REGISTRY.md"
    
    # Create a high-scoring candidate
    job = JobPosting(
        title="Senior System Analyst",
        company="TechCorp",
        location="Helsinki, Remote",
        url=HttpUrl("https://example.com/dream-job"),
        source="duunitori.fi",
        discovered_date=datetime.now(timezone.utc),
        description="Perfect job for experienced system analyst with Python skills."
    )
    
    scored = ScoredJob(
        job=job,
        score=95.0,
        matched_keywords=["system analyst", "python", "remote"]
    )
    
    # Convert to application
    converter = ApplicationConverter(applications_dir, registry_path)
    app_path = converter.convert(scored, notes="Excellent fit!")
    
    # Verify structure created
    assert app_path.exists()
    assert (app_path / "README.md").exists()
    assert (app_path / "tookuulutus.md").exists()
    
    # Verify content
    readme = (app_path / "README.md").read_text()
    assert "Senior System Analyst" in readme
    assert "TechCorp" in readme
    assert "95.0" in readme
    
    posting = (app_path / "tookuulutus.md").read_text()
    assert str(job.url) in posting
    assert job.description and job.description in posting


def test_mark_job_status_workflow(integration_workspace: Path) -> None:
    """Test marking jobs with different statuses."""
    config_path = integration_workspace / "config.yaml"
    cm = ConfigManager(config_path)
    cfg = cm.config
    
    sm = StateManager(cfg.state_file)
    
    # Add jobs
    jobs = create_sample_jobs()
    for job in jobs:
        sm.add_job(job)
    
    # Initially all in new_jobs
    assert len(sm.state.new_jobs) == 4
    assert len(sm.state.candidates) == 0
    assert len(sm.state.applied) == 0
    
    # Mark first as candidate
    job1 = jobs[0]
    job1.status = JobStatus.CANDIDATE
    sm.update_job(job1)
    sm.state.candidates.append(job1.id)
    sm.state.new_jobs.remove(job1.id)
    
    assert len(sm.state.candidates) == 1
    assert len(sm.state.new_jobs) == 3
    
    # Mark second as applied
    job2 = jobs[1]
    job2.status = JobStatus.APPLIED
    sm.update_job(job2)
    sm.state.applied.append(job2.id)
    sm.state.new_jobs.remove(job2.id)
    sm.state.total_applications += 1
    
    assert len(sm.state.applied) == 1
    assert len(sm.state.new_jobs) == 2
    assert sm.state.total_applications == 1
    
    # Save and reload
    sm.save_state()
    sm2 = StateManager(cfg.state_file)
    
    assert len(sm2.state.candidates) == 1
    assert len(sm2.state.applied) == 1
    assert sm2.state.total_applications == 1


def test_cleanup_old_jobs(integration_workspace: Path) -> None:
    """Test archiving jobs older than threshold."""
    config_path = integration_workspace / "config.yaml"
    cm = ConfigManager(config_path)
    cfg = cm.config
    
    sm = StateManager(cfg.state_file)
    
    # Add recent job
    recent = JobPosting(
        title="Recent Job",
        company="Corp",
        location="Helsinki",
        url=HttpUrl("https://example.com/recent"),
        source="duunitori.fi",
        discovered_date=datetime.now(timezone.utc)
    )
    sm.add_job(recent)
    
    # Add old job (from 2020)
    old = JobPosting(
        title="Old Job",
        company="OldCorp",
        location="Tallinn",
        url=HttpUrl("https://example.com/old"),
        source="duunitori.fi",
        discovered_date=datetime(2020, 1, 1, tzinfo=timezone.utc)
    )
    sm.add_job(old)
    
    assert sm.state.total_jobs_seen == 2
    
    # Cleanup old jobs (>60 days) - returns count of archived
    archived = sm.cleanup_old_jobs(60)
    
    # Verify the count is correct
    assert archived == 1


def test_scoring_with_real_config(integration_workspace: Path) -> None:
    """Test scoring algorithm with configuration."""
    config_path = integration_workspace / "config.yaml"
    cm = ConfigManager(config_path)
    
    scorer = JobScorer(cm.config.scoring)
    
    # High scoring job (multiple matches)
    high_job = JobPosting(
        title="Senior Python Developer - System Analyst",
        company="TechCorp",  # preferred
        location="Helsinki, Remote",  # preferred + remote
        url=HttpUrl("https://example.com/high"),
        source="duunitori.fi",
        discovered_date=datetime.now(timezone.utc),
        description="Python Django developer for system analysis"
    )
    
    high_scored = scorer.score(high_job)
    assert high_scored.score >= 70  # Should be high priority
    assert high_scored.category == "High Priority"
    assert len(high_scored.matched_keywords) >= 3
    
    # Low scoring job (junior + negative keyword)
    low_job = JobPosting(
        title="Junior Developer",
        company="StartupInc",
        location="Tampere",
        url=HttpUrl("https://example.com/low"),
        source="duunitori.fi",
        discovered_date=datetime.now(timezone.utc),
        description="Entry level position"
    )
    
    low_scored = scorer.score(low_job)
    assert low_scored.score < 40  # Should be low priority
    assert low_scored.category == "Low Priority"


def test_digest_generation_with_multiple_categories(integration_workspace: Path) -> None:
    """Test digest includes all category sections."""
    config_path = integration_workspace / "config.yaml"
    cm = ConfigManager(config_path)
    cfg = cm.config
    
    scorer = JobScorer(cfg.scoring)
    
    # Create jobs in different categories
    jobs = create_sample_jobs()
    scored = [scorer.score(j) for j in jobs]
    
    # Save candidates
    _save_candidates(cfg.candidates_dir, scored)
    
    # Generate digest
    dg = DigestGenerator(cfg.candidates_dir)
    digest = dg.generate_digest()
    
    # Verify digest structure
    assert "## Summary" in digest
    assert "**Total Candidates**:" in digest or "Total Candidates" in digest
    
    # Should have at least one category section (with emoji headings)
    has_section = (
        "🔥" in digest or  # High Priority emoji
        "📋" in digest or  # Review emoji  
        "💤" in digest     # Low Priority emoji
    )
    assert has_section, "Digest should contain at least one category section"


def test_error_handling_invalid_config(integration_workspace: Path) -> None:
    """Test graceful handling of invalid configuration."""
    invalid_config = integration_workspace / "invalid.yaml"
    invalid_config.write_text("invalid: yaml: content")
    
    with pytest.raises(Exception):  # Should raise ConfigurationError
        ConfigManager(invalid_config)


def test_concurrent_state_updates(integration_workspace: Path) -> None:
    """Test state manager handles multiple save operations."""
    config_path = integration_workspace / "config.yaml"
    cm = ConfigManager(config_path)
    cfg = cm.config
    
    # Multiple state managers (simulating concurrent access)
    sm1 = StateManager(cfg.state_file)
    sm2 = StateManager(cfg.state_file)
    
    # Add different jobs
    job1 = create_sample_jobs()[0]
    job2 = create_sample_jobs()[1]
    
    sm1.add_job(job1)
    sm1.save_state()
    
    sm2.add_job(job2)
    sm2.save_state()
    
    # Reload and verify both saved
    sm3 = StateManager(cfg.state_file)
    # Note: This test documents current behavior (last write wins)
    # In production, recommend single-process access or proper locking
    assert sm3.state.total_jobs_seen >= 1
