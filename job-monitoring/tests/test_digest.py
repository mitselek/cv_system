"""Tests for digest_generator.py"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

import pytest
from pydantic import HttpUrl

from job_monitor.digest import DigestGenerator
from job_monitor.schemas import JobPosting, ScoredJob


@pytest.fixture
def sample_candidates_dir() -> Generator[Path, None, None]:
    """Create a temporary candidates directory with sample data."""
    with TemporaryDirectory() as tmpdir:
        candidates_dir = Path(tmpdir)
        today = datetime.now().strftime("%Y-%m-%d")
        day_dir = candidates_dir / today
        
        # Create category directories
        (day_dir / "high_priority").mkdir(parents=True)
        (day_dir / "review").mkdir(parents=True)
        (day_dir / "low_priority").mkdir(parents=True)
        
        # Add sample jobs
        high_job = ScoredJob(
            job=JobPosting(
                url=HttpUrl("https://example.com/high/1"),
                title="Senior Python Developer",
                company="Tech Corp",
                location="Remote",
                description="Great opportunity for Python expert",
                source="duunitori",
            ),
            score=85.0,
            score_breakdown={"positive_keywords": 30.0, "remote_bonus": 15.0},
            matched_keywords=["python", "remote"],
        )
        
        review_job = ScoredJob(
            job=JobPosting(
                url=HttpUrl("https://example.com/review/2"),
                title="Python Developer",
                company="Medium Co",
                location="Helsinki",
                description="Looking for Python developer",
                source="duunitori",
            ),
            score=55.0,
            score_breakdown={"positive_keywords": 20.0},
            matched_keywords=["python"],
        )
        
        low_job = ScoredJob(
            job=JobPosting(
                url=HttpUrl("https://example.com/low/3"),
                title="Junior Developer",
                company="Startup",
                location="Office",
                source="duunitori",
            ),
            score=25.0,
            score_breakdown={},
            matched_keywords=[],
        )
        
        # Save to JSON files
        with open(day_dir / "high_priority" / f"{high_job.job.id}.json", "w") as f:
            json.dump(high_job.model_dump(mode="json"), f)
        
        with open(day_dir / "review" / f"{review_job.job.id}.json", "w") as f:
            json.dump(review_job.model_dump(mode="json"), f)
        
        with open(day_dir / "low_priority" / f"{low_job.job.id}.json", "w") as f:
            json.dump(low_job.model_dump(mode="json"), f)
        
        yield candidates_dir


def test_generate_digest_creates_markdown(sample_candidates_dir: Path) -> None:
    """Test that digest generates valid markdown."""
    dg = DigestGenerator(sample_candidates_dir)
    
    digest = dg.generate_digest()
    
    assert digest.startswith("# Job Candidates Digest")
    assert "## Summary" in digest
    assert "## 🔥 High Priority" in digest
    assert "## 📋 Review" in digest
    assert "## 💤 Low Priority" in digest


def test_generate_digest_includes_summary(sample_candidates_dir: Path) -> None:
    """Test that digest includes summary statistics."""
    dg = DigestGenerator(sample_candidates_dir)
    
    digest = dg.generate_digest()
    
    assert "**Total Candidates**: 3" in digest
    assert "🔥 High Priority: 1" in digest
    assert "📋 Review: 1" in digest
    assert "💤 Low Priority: 1" in digest


def test_generate_digest_includes_job_details(sample_candidates_dir: Path) -> None:
    """Test that digest includes job details."""
    dg = DigestGenerator(sample_candidates_dir)
    
    digest = dg.generate_digest()
    
    assert "Senior Python Developer" in digest
    assert "Tech Corp" in digest
    assert "Remote" in digest
    assert "**Score**: 85.0/100" in digest
    assert "**Matched Keywords**: python, remote" in digest


def test_generate_digest_sorts_by_score(sample_candidates_dir: Path) -> None:
    """Test that jobs are sorted by score within categories."""
    # Add another high priority job with lower score
    today = datetime.now().strftime("%Y-%m-%d")
    day_dir = sample_candidates_dir / today
    
    extra_job = ScoredJob(
        job=JobPosting(
            url=HttpUrl("https://example.com/high/4"),
            title="Lead Developer",
            company="Big Corp",
            location="Remote",
            source="duunitori",
        ),
        score=90.0,
        score_breakdown={},
        matched_keywords=[],
    )
    
    with open(day_dir / "high_priority" / f"{extra_job.job.id}.json", "w") as f:
        json.dump(extra_job.model_dump(mode="json"), f)
    
    dg = DigestGenerator(sample_candidates_dir)
    digest = dg.generate_digest()
    
    # Higher score should appear first
    lead_pos = digest.find("Lead Developer")
    senior_pos = digest.find("Senior Python Developer")
    assert lead_pos < senior_pos


def test_save_digest_creates_file(sample_candidates_dir: Path) -> None:
    """Test that save_digest creates digest.md file."""
    dg = DigestGenerator(sample_candidates_dir)
    
    digest_path = dg.save_digest()
    
    assert digest_path.exists()
    assert digest_path.name == "digest.md"
    
    # Verify content is same as generate_digest
    with open(digest_path, "r") as f:
        saved_content = f.read()
    
    generated_content = dg.generate_digest()
    assert saved_content == generated_content


def test_generate_digest_handles_no_candidates() -> None:
    """Test digest generation with no candidates."""
    with TemporaryDirectory() as tmpdir:
        candidates_dir = Path(tmpdir)
        dg = DigestGenerator(candidates_dir)
        
        digest = dg.generate_digest()
        
        assert "No candidates found" in digest


def test_generate_digest_includes_json_links(sample_candidates_dir: Path) -> None:
    """Test that digest includes links to JSON files."""
    dg = DigestGenerator(sample_candidates_dir)
    
    digest = dg.generate_digest()
    
    # Should have links to full details
    assert "📄 [Full Details]" in digest
    assert ".json)" in digest


def test_generate_digest_truncates_long_descriptions(sample_candidates_dir: Path) -> None:
    """Test that long descriptions are truncated."""
    # Add job with very long description
    today = datetime.now().strftime("%Y-%m-%d")
    day_dir = sample_candidates_dir / today
    
    long_desc = "A" * 300  # 300 characters
    long_job = ScoredJob(
        job=JobPosting(
            url=HttpUrl("https://example.com/long/5"),
            title="Verbose Job",
            company="Talky Corp",
            location="Remote",
            description=long_desc,
            source="duunitori",
        ),
        score=75.0,
        score_breakdown={},
        matched_keywords=[],
    )
    
    with open(day_dir / "high_priority" / f"{long_job.job.id}.json", "w") as f:
        json.dump(long_job.model_dump(mode="json"), f)
    
    dg = DigestGenerator(sample_candidates_dir)
    digest = dg.generate_digest()
    
    # Description should be truncated with ...
    assert "..." in digest
    # Full 300 character string should not appear
    assert long_desc not in digest
