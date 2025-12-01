"""Tests for job_monitor.py candidate storage"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from job_monitor import _save_candidates
from schemas import JobPosting, ScoredJob


@pytest.fixture
def sample_scored_jobs() -> list[ScoredJob]:
    """Create sample scored jobs in different categories."""
    high_job = JobPosting(
        url="https://example.com/high/1",
        title="Senior Python Developer",
        company="Great Co",
        location="Remote",
        source="duunitori",
    )
    
    review_job = JobPosting(
        url="https://example.com/review/2",
        title="Python Developer",
        company="OK Co",
        location="Office",
        source="duunitori",
    )
    
    low_job = JobPosting(
        url="https://example.com/low/3",
        title="Junior Developer",
        company="Small Co",
        location="On-site",
        source="duunitori",
    )
    
    return [
        ScoredJob(job=high_job, score=85.0, score_breakdown={}, matched_keywords=[]),
        ScoredJob(job=review_job, score=55.0, score_breakdown={}, matched_keywords=[]),
        ScoredJob(job=low_job, score=25.0, score_breakdown={}, matched_keywords=[]),
    ]


def test_save_candidates_creates_directories(sample_scored_jobs: list[ScoredJob]) -> None:
    """Test that candidate directories are created."""
    with TemporaryDirectory() as tmpdir:
        candidates_dir = Path(tmpdir)
        
        counts = _save_candidates(candidates_dir, sample_scored_jobs)
        
        today = datetime.now().strftime("%Y-%m-%d")
        day_dir = candidates_dir / today
        
        assert day_dir.exists()
        assert (day_dir / "high_priority").exists()
        assert (day_dir / "review").exists()
        assert (day_dir / "low_priority").exists()


def test_save_candidates_returns_counts(sample_scored_jobs: list[ScoredJob]) -> None:
    """Test that correct counts are returned."""
    with TemporaryDirectory() as tmpdir:
        candidates_dir = Path(tmpdir)
        
        counts = _save_candidates(candidates_dir, sample_scored_jobs)
        
        assert counts["high_priority"] == 1
        assert counts["review"] == 1
        assert counts["low_priority"] == 1


def test_save_candidates_creates_json_files(sample_scored_jobs: list[ScoredJob]) -> None:
    """Test that JSON files are created with correct content."""
    with TemporaryDirectory() as tmpdir:
        candidates_dir = Path(tmpdir)
        
        _save_candidates(candidates_dir, sample_scored_jobs)
        
        today = datetime.now().strftime("%Y-%m-%d")
        day_dir = candidates_dir / today
        
        # Check high priority job
        high_files = list((day_dir / "high_priority").glob("*.json"))
        assert len(high_files) == 1
        
        with open(high_files[0], "r") as f:
            data = json.load(f)
            assert data["score"] == 85.0
            assert data["job"]["title"] == "Senior Python Developer"
            assert data["category"] == "High Priority"


def test_save_candidates_uses_job_id_as_filename(sample_scored_jobs: list[ScoredJob]) -> None:
    """Test that files are named using job ID."""
    with TemporaryDirectory() as tmpdir:
        candidates_dir = Path(tmpdir)
        
        _save_candidates(candidates_dir, sample_scored_jobs)
        
        today = datetime.now().strftime("%Y-%m-%d")
        day_dir = candidates_dir / today
        
        high_files = list((day_dir / "high_priority").glob("*.json"))
        assert len(high_files) == 1
        
        # Filename should be job ID + .json
        expected_id = sample_scored_jobs[0].job.id
        assert high_files[0].stem == expected_id


def test_save_candidates_handles_empty_list() -> None:
    """Test handling of empty scored jobs list."""
    with TemporaryDirectory() as tmpdir:
        candidates_dir = Path(tmpdir)
        
        counts = _save_candidates(candidates_dir, [])
        
        assert counts["high_priority"] == 0
        assert counts["review"] == 0
        assert counts["low_priority"] == 0


def test_save_candidates_categorizes_correctly() -> None:
    """Test that jobs are categorized to correct directories."""
    with TemporaryDirectory() as tmpdir:
        candidates_dir = Path(tmpdir)
        
        jobs = [
            ScoredJob(
                job=JobPosting(
                    url=f"https://example.com/job/{i}",
                    title=f"Job {i}",
                    company="Co",
                    location="Remote",
                    source="duunitori",
                ),
                score=score,
                score_breakdown={},
                matched_keywords=[],
            )
            for i, score in enumerate([90, 75, 60, 50, 30, 15])
        ]
        
        counts = _save_candidates(candidates_dir, jobs)
        
        # Scores >= 70: high priority (2 jobs)
        # Scores 40-69: review (2 jobs)  
        # Scores < 40: low priority (2 jobs)
        assert counts["high_priority"] == 2
        assert counts["review"] == 2
        assert counts["low_priority"] == 2
