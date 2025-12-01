#!/usr/bin/env python3
"""Tests for markdown exporter."""
from datetime import datetime
from pathlib import Path
import pytest

from job_monitor.markdown_exporter import MarkdownExporter
from job_monitor.schemas import JobPosting, ScoredJob


def test_export_job_basic(tmp_path: Path) -> None:
    """Test basic markdown export."""
    job = JobPosting(
        id="test123",
        title="Senior Python Developer",
        company="Example Corp",
        location="Helsinki",
        url="https://example.com/job/123",
        source="duunitori",
        discovered_date=datetime(2025, 12, 1),
        posted_date="2025-11-28",
        description="We are looking for a skilled Python developer with experience in web frameworks.",
        status="new"
    )
    
    scored = ScoredJob(
        job=job,
        score=85.0,
        category="High Priority",
        matched_keywords=["python", "web", "developer"],
        score_breakdown={
            "keyword_matches": 30,
            "preferred_companies": 0,
            "location_bonus": 10,
            "remote_bonus": 0
        }
    )
    
    output_path = tmp_path / "test123.md"
    MarkdownExporter.export_job(scored, output_path)
    
    assert output_path.exists()
    content = output_path.read_text()
    
    # Check key sections
    assert "# Senior Python Developer - Example Corp" in content
    assert "**Score:** 85/100" in content
    assert "**Category:** High Priority" in content
    assert "## Quick Info" in content
    assert "**Company:** Example Corp" in content
    assert "**Location:** Helsinki" in content
    assert "https://example.com/job/123" in content
    assert "## Score Breakdown" in content
    assert "**Keyword Matches:** +30 points" in content
    assert "**Total:** 85/100" in content
    assert "## Matched Keywords (3)" in content
    assert "python" in content
    assert "## Job Description" in content
    assert "We are looking for a skilled Python developer" in content
    assert "## Actions" in content
    assert "- [ ] Review job posting in detail" in content
    assert "*Job ID: test123*" in content


def test_export_job_no_description(tmp_path: Path) -> None:
    """Test markdown export without description."""
    job = JobPosting(
        id="test456",
        title="Software Architect",
        company="Tech Inc",
        location="Remote",
        url="https://example.com/job/456",
        source="linkedin",
        discovered_date=datetime(2025, 12, 1),
        status="new"
    )
    
    scored = ScoredJob(
        job=job,
        score=45.0,
        category="Review",
        matched_keywords=["software", "architect"],
        score_breakdown={
            "keyword_matches": 20,
            "preferred_companies": 0,
            "location_bonus": 0,
            "remote_bonus": 5
        }
    )
    
    output_path = tmp_path / "test456.md"
    MarkdownExporter.export_job(scored, output_path)
    
    assert output_path.exists()
    content = output_path.read_text()
    
    assert "# Software Architect - Tech Inc" in content
    assert "**Score:** 45/100" in content
    assert "**Category:** Review" in content
    assert "## Job Description" not in content  # No description section


def test_export_job_with_emojis(tmp_path: Path) -> None:
    """Test that emojis are included based on score/category."""
    job = JobPosting(
        id="test789",
        title="Data Analyst",
        company="DataCo",
        location="Tampere",
        url="https://example.com/job/789",
        source="duunitori",
        discovered_date=datetime(2025, 12, 1),
        status="new"
    )
    
    # High score (90+) should get star emoji
    scored = ScoredJob(
        job=job,
        score=95.0,
        category="High Priority",
        matched_keywords=["data", "analyst"],
        score_breakdown={"keyword_matches": 95}
    )
    
    output_path = tmp_path / "test789.md"
    MarkdownExporter.export_job(scored, output_path)
    
    content = output_path.read_text()
    assert "🌟" in content  # 90+ score emoji
    assert "🔥" in content  # High Priority emoji


def test_export_jobs_batch(tmp_path: Path) -> None:
    """Test batch export of multiple jobs."""
    jobs = []
    for i in range(3):
        job = JobPosting(
            id=f"batch{i}",
            title=f"Job {i}",
            company=f"Company {i}",
            location="Helsinki",
            url=f"https://example.com/job/{i}",
            source="duunitori",
            discovered_date=datetime(2025, 12, 1),
            status="new"
        )
        scored = ScoredJob(
            job=job,
            score=50.0 + i * 10,
            category="Review",
            matched_keywords=[],
            score_breakdown={"keyword_matches": 50 + i * 10}
        )
        jobs.append(scored)
    
    count = MarkdownExporter.export_jobs_batch(jobs, tmp_path)
    
    assert count == 3
    assert (tmp_path / "batch0.md").exists()
    assert (tmp_path / "batch1.md").exists()
    assert (tmp_path / "batch2.md").exists()


def test_export_creates_parent_dirs(tmp_path: Path) -> None:
    """Test that export creates parent directories if needed."""
    job = JobPosting(
        id="nested123",
        title="Test Job",
        company="Test Co",
        location="Helsinki",
        url="https://example.com/job/nested",
        source="duunitori",
        discovered_date=datetime(2025, 12, 1),
        status="new"
    )
    
    scored = ScoredJob(
        job=job,
        score=60.0,
        category="Review",
        matched_keywords=[],
        score_breakdown={"keyword_matches": 60}
    )
    
    nested_path = tmp_path / "deep" / "nested" / "path" / "nested123.md"
    MarkdownExporter.export_job(scored, nested_path)
    
    assert nested_path.exists()
    assert nested_path.parent.exists()
