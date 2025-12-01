"""Tests for deduplicator.py"""
from __future__ import annotations

from pydantic import HttpUrl
from schemas import JobPosting
from deduplicator import Deduplicator


def test_is_duplicate_by_id() -> None:
    """Test duplicate detection by URL/ID."""
    dd = Deduplicator()
    
    job1 = JobPosting(
        url=HttpUrl("https://example.com/job/123"),
        title="Python Developer",
        company="Tech Co",
        location="Remote",
        source="duunitori",
    )
    
    job2 = JobPosting(
        url=HttpUrl("https://example.com/job/123"),  # Same URL
        title="Senior Python Developer",  # Different title
        company="Different Co",  # Different company
        location="Office",
        source="linkedin",
    )
    
    assert not dd.is_duplicate(job1)
    dd.add(job1)
    assert dd.is_duplicate(job2)  # Same ID despite different details


def test_is_duplicate_by_fingerprint() -> None:
    """Test duplicate detection by title+company fingerprint."""
    dd = Deduplicator()
    
    job1 = JobPosting(
        url=HttpUrl("https://duunitori.fi/job/123"),
        title="Python Developer",
        company="Tech Company",
        location="Remote",
        source="duunitori",
    )
    
    job2 = JobPosting(
        url=HttpUrl("https://linkedin.com/jobs/456"),  # Different URL
        title="Python Developer",  # Same title
        company="Tech Company",  # Same company
        location="Office",
        source="linkedin",
    )
    
    assert not dd.is_duplicate(job1)
    dd.add(job1)
    assert dd.is_duplicate(job2)  # Same fingerprint


def test_not_duplicate_different_jobs() -> None:
    """Test different jobs are not marked as duplicates."""
    dd = Deduplicator()
    
    job1 = JobPosting(
        url=HttpUrl("https://example.com/job/1"),
        title="Python Developer",
        company="Company A",
        location="Remote",
        source="duunitori",
    )
    
    job2 = JobPosting(
        url=HttpUrl("https://example.com/job/2"),
        title="Java Developer",
        company="Company B",
        location="Office",
        source="linkedin",
    )
    
    dd.add(job1)
    assert not dd.is_duplicate(job2)


def test_fingerprint_normalization() -> None:
    """Test fingerprint normalizes whitespace and case."""
    dd = Deduplicator()
    
    job1 = JobPosting(
        url=HttpUrl("https://example.com/job/1"),
        title="Python   Developer",  # Extra spaces
        company="Tech Company",
        location="Remote",
        source="duunitori",
    )
    
    job2 = JobPosting(
        url=HttpUrl("https://example.com/job/2"),
        title="python developer",  # Lowercase, single space
        company="TECH COMPANY",  # Uppercase
        location="Office",
        source="linkedin",
    )
    
    dd.add(job1)
    assert dd.is_duplicate(job2)


def test_filter_unique() -> None:
    """Test filter_unique returns only unique jobs."""
    dd = Deduplicator()
    
    job1 = JobPosting(
        url=HttpUrl("https://example.com/job/1"),
        title="Python Developer",
        company="Tech Co",
        location="Remote",
        source="duunitori",
    )
    
    job2 = JobPosting(
        url=HttpUrl("https://example.com/job/2"),
        title="Java Developer",
        company="Other Co",
        location="Office",
        source="duunitori",
    )
    
    job3 = JobPosting(
        url=HttpUrl("https://example.com/job/1"),  # Duplicate of job1
        title="Python Developer",
        company="Tech Co",
        location="Remote",
        source="linkedin",
    )
    
    jobs = [job1, job2, job3]
    unique = dd.filter_unique(jobs)
    
    assert len(unique) == 2
    assert job1 in unique
    assert job2 in unique
    assert job3 not in unique


def test_filter_unique_maintains_order() -> None:
    """Test filter_unique maintains original order."""
    dd = Deduplicator()
    
    jobs = [
        JobPosting(
            url=HttpUrl(f"https://example.com/job/{i}"),
            title=f"Job {i}",
            company=f"Company {i}",
            location="Remote",
            source="duunitori",
        )
        for i in range(5)
    ]
    
    unique = dd.filter_unique(jobs)
    
    assert len(unique) == 5
    for i, job in enumerate(unique):
        assert job.title == f"Job {i}"


def test_empty_input() -> None:
    """Test handling of empty job list."""
    dd = Deduplicator()
    
    unique = dd.filter_unique([])
    
    assert len(unique) == 0
