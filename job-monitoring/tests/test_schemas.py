"""
Basic tests for Pydantic schemas.

Tests model instantiation and validators.
"""

from datetime import datetime
from pathlib import Path
from typing import cast
from pydantic import HttpUrl

from job_monitor.schemas import (
    JobPosting,
    JobStatus,
    QueryConfig,
    ScoredJob,
    SourceConfig,
    ScoringConfig,
    SystemConfig,
    MonitorState,
)


def test_job_posting_id_generation() -> None:
    """Test that ID is auto-generated from URL."""
    job = JobPosting(
        url=cast(HttpUrl, "https://example.com/job/123"),
        title="Test Job",
        company="Test Company",
        location="Tallinn",
        posted_date="2025-12-01",
        discovered_date=datetime.now(),
        description="Test description",
    )
    assert job.id  # Should be generated
    assert len(job.id) == 16  # MD5 hash truncated to 16 chars
    print(f"✅ Job ID auto-generated: {job.id}")


def test_job_posting_explicit_id() -> None:
    """Test that explicit ID is preserved."""
    explicit_id = "custom_id_123"
    job = JobPosting(
        id=explicit_id,
        url=cast(HttpUrl, "https://example.com/job/456"),
        title="Test Job",
        company="Test Company",
        location="Tallinn",
        posted_date="2025-12-01",
        discovered_date=datetime.now(),
        description="Test description",
    )
    assert job.id == explicit_id
    print(f"✅ Explicit ID preserved: {job.id}")


def test_scored_job_category_high() -> None:
    """Test category auto-determination for high score."""
    job = JobPosting(
        url=cast(HttpUrl, "https://example.com/job/789"),
        title="Python Developer",
        company="Tech Corp",
        location="Tallinn",
        posted_date="2025-12-01",
        discovered_date=datetime.now(),
        description="Python development",
    )
    scored = ScoredJob(
        job=job,
        score=85.0,
        score_breakdown={"keyword_match": 50.0, "company_match": 35.0},
        matched_keywords=["python", "django"],
    )
    assert scored.category == "High Priority"
    print(f"✅ Category auto-determined: {scored.category} (score: {scored.score})")


def test_scored_job_category_review() -> None:
    """Test category auto-determination for medium score."""
    job = JobPosting(
        url=cast(HttpUrl, "https://example.com/job/101"),
        title="Developer",
        company="Some Corp",
        location="Remote",
        posted_date="2025-12-01",
        discovered_date=datetime.now(),
        description="Development work",
    )
    scored = ScoredJob(
        job=job,
        score=55.0,
        score_breakdown={"keyword_match": 30.0, "location_match": 25.0},
        matched_keywords=["python"],
    )
    assert scored.category == "Review"
    print(f"✅ Category auto-determined: {scored.category} (score: {scored.score})")


def test_scored_job_category_low() -> None:
    """Test category auto-determination for low score."""
    job = JobPosting(
        url=cast(HttpUrl, "https://example.com/job/202"),
        title="Manager",
        company="Corp",
        location="Helsinki",
        posted_date="2025-12-01",
        discovered_date=datetime.now(),
        description="Management",
    )
    scored = ScoredJob(
        job=job,
        score=25.0,
        score_breakdown={"keyword_match": 10.0, "recency": 15.0},
        matched_keywords=[],
    )
    assert scored.category == "Low Priority"
    print(f"✅ Category auto-determined: {scored.category} (score: {scored.score})")


def test_query_config() -> None:
    """Test QueryConfig validation."""
    query = QueryConfig(keywords="python django", location="tallinn", limit=50)
    assert query.keywords == "python django"
    assert query.limit == 50
    print(f"✅ QueryConfig valid: {query.keywords} (limit: {query.limit})")


def test_source_config() -> None:
    """Test SourceConfig with queries."""
    source = SourceConfig(
        name="cv.ee",
        enabled=True,
        queries=[
            QueryConfig(keywords="python", location="tallinn", limit=20),
            QueryConfig(keywords="django", location="remote", limit=10),
        ],
    )
    assert source.name == "cv.ee"
    assert len(source.queries) == 2
    print(f"✅ SourceConfig valid: {source.name} with {len(source.queries)} queries")


def test_scoring_config() -> None:
    """Test ScoringConfig."""
    scoring = ScoringConfig(
        positive_keywords=["python", "django", "postgresql"],
        negative_keywords=["php", "wordpress"],
        required_keywords=["python"],
        preferred_companies=["Microsoft", "Google"],
        blocked_companies=["BadCorp"],
        preferred_locations=["tallinn", "remote"],
        remote_bonus=10.0,
        days_threshold_fresh=7,
        days_threshold_old=30,
    )
    assert len(scoring.positive_keywords) == 3
    assert scoring.remote_bonus == 10.0
    print(f"✅ ScoringConfig valid: {len(scoring.positive_keywords)} positive keywords")


def test_system_config() -> None:
    """Test SystemConfig."""
    config = SystemConfig(
        sources=[
            SourceConfig(
                name="cv.ee",
                enabled=True,
                queries=[QueryConfig(keywords="python", location="tallinn")],
            )
        ],
        scoring=ScoringConfig(
            positive_keywords=["python"],
            negative_keywords=[],
            required_keywords=[],
        ),
        state_file=Path("state.json"),
        candidates_dir=Path("candidates/"),
    )
    assert len(config.sources) == 1
    assert config.state_file == Path("state.json")
    print(f"✅ SystemConfig valid: {len(config.sources)} sources")


def test_monitor_state() -> None:
    """Test MonitorState."""
    state = MonitorState(
        last_scan=datetime.now(),
        total_jobs_seen=100,
        total_candidates=15,
        total_applications=5,
        seen_jobs={},
        new_jobs=["job2", "job3"],
        candidates=["job4"],
        applied=["job5"],
    )
    assert state.total_jobs_seen == 100
    assert len(state.new_jobs) == 2
    print(f"✅ MonitorState valid: {state.total_jobs_seen} jobs seen")


def test_job_status_enum() -> None:
    """Test JobStatus enum."""
    assert JobStatus.NEW.value == "new"
    assert JobStatus.REVIEWED.value == "reviewed"
    assert JobStatus.CANDIDATE.value == "candidate"
    assert JobStatus.APPLIED.value == "applied"
    assert JobStatus.REJECTED.value == "rejected"
    assert JobStatus.ARCHIVED.value == "archived"
    print("✅ JobStatus enum valid: all 6 states")


if __name__ == "__main__":
    test_job_posting_id_generation()
    test_job_posting_explicit_id()
    test_scored_job_category_high()
    test_scored_job_category_review()
    test_scored_job_category_low()
    test_query_config()
    test_source_config()
    test_scoring_config()
    test_system_config()
    test_monitor_state()
    test_job_status_enum()
    print("\n🎉 All tests passed!")
