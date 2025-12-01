"""Tests for state_manager.py"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from schemas import JobPosting, MonitorState
from state_manager import StateManager


@pytest.fixture
def temp_state_file() -> Path:
    """Create a temporary state file."""
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir) / "state.json"


@pytest.fixture
def sample_job() -> JobPosting:
    """Create a sample job posting."""
    return JobPosting(
        url="https://example.com/job/123",
        title="Senior Python Developer",
        company="Test Company",
        location="Remote",
        description="Great job",
        posted_date="2025-12-01",
        source="duunitori",
    )


def test_load_state_creates_default(temp_state_file: Path) -> None:
    """Test loading state creates default when file doesn't exist."""
    sm = StateManager(temp_state_file)
    state = sm.load_state()
    
    assert state.last_scan is None
    assert state.total_jobs_seen == 0
    assert state.total_candidates == 0
    assert len(state.seen_jobs) == 0


def test_save_and_load_state(temp_state_file: Path, sample_job: JobPosting) -> None:
    """Test saving and loading state preserves data."""
    sm = StateManager(temp_state_file)
    sm.add_job(sample_job)
    sm.touch_scan_time()
    sm.save_state()
    
    # Load in new manager
    sm2 = StateManager(temp_state_file)
    state2 = sm2.load_state()
    
    assert state2.total_jobs_seen == 1
    assert sample_job.id in state2.seen_jobs
    assert state2.last_scan is not None


def test_is_seen(temp_state_file: Path, sample_job: JobPosting) -> None:
    """Test is_seen returns correct result."""
    sm = StateManager(temp_state_file)
    
    assert not sm.is_seen(sample_job.id)
    sm.add_job(sample_job)
    assert sm.is_seen(sample_job.id)


def test_add_job_increments_stats(temp_state_file: Path, sample_job: JobPosting) -> None:
    """Test add_job increments counters."""
    sm = StateManager(temp_state_file)
    
    sm.add_job(sample_job)
    
    assert sm.state.total_jobs_seen == 1
    assert sample_job.id in sm.state.new_jobs
    assert sm.state.stats_by_source["duunitori"] == 1


def test_add_job_idempotent(temp_state_file: Path, sample_job: JobPosting) -> None:
    """Test adding same job twice doesn't duplicate."""
    sm = StateManager(temp_state_file)
    
    sm.add_job(sample_job)
    sm.add_job(sample_job)
    
    assert sm.state.total_jobs_seen == 1


def test_update_job(temp_state_file: Path, sample_job: JobPosting) -> None:
    """Test update_job modifies existing job."""
    sm = StateManager(temp_state_file)
    sm.add_job(sample_job)
    
    # Modify job
    sample_job.description = "Updated description"
    sm.update_job(sample_job)
    
    retrieved = sm.get_job(sample_job.id)
    assert retrieved is not None
    assert retrieved.description == "Updated description"


def test_get_job(temp_state_file: Path, sample_job: JobPosting) -> None:
    """Test get_job retrieves correct job."""
    sm = StateManager(temp_state_file)
    
    assert sm.get_job(sample_job.id) is None
    
    sm.add_job(sample_job)
    retrieved = sm.get_job(sample_job.id)
    
    assert retrieved is not None
    assert retrieved.id == sample_job.id


def test_cleanup_old_jobs(temp_state_file: Path) -> None:
    """Test cleanup_old_jobs archives old jobs."""
    sm = StateManager(temp_state_file)
    
    # Add old job
    old_job = JobPosting(
        url="https://example.com/old/1",
        title="Old Job",
        company="Old Co",
        location="Remote",
        source="duunitori",
    )
    # Manually set old discovered_date
    old_date = datetime.now(timezone.utc) - timedelta(days=40)
    old_job.discovered_date = old_date
    sm.add_job(old_job)
    
    # Add recent job
    recent_job = JobPosting(
        url="https://example.com/recent/2",
        title="Recent Job",
        company="Recent Co",
        location="Remote",
        source="duunitori",
    )
    sm.add_job(recent_job)
    
    # Cleanup jobs older than 30 days
    archived = sm.cleanup_old_jobs(30)
    
    assert archived == 1
    assert recent_job.id in sm.state.new_jobs
    # Old job should be removed from new_jobs but still in seen_jobs
    assert old_job.id not in sm.state.new_jobs


def test_atomic_write_creates_backup(temp_state_file: Path, sample_job: JobPosting) -> None:
    """Test atomic write creates backup file."""
    sm = StateManager(temp_state_file)
    sm.add_job(sample_job)
    sm.save_state()
    
    # Save again to trigger backup creation
    sample_job.description = "Updated"
    sm.update_job(sample_job)
    sm.save_state()
    
    # Check backup exists
    backup_file = temp_state_file.with_suffix(temp_state_file.suffix + ".bak")
    assert backup_file.exists()
