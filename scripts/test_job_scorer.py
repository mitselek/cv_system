"""Tests for job_scorer.py"""
from __future__ import annotations

from schemas import JobPosting, ScoringConfig
from job_scorer import JobScorer


def test_score_positive_keywords() -> None:
    """Test scoring with positive keywords."""
    config = ScoringConfig(
        positive_keywords=["python", "remote"],
        negative_keywords=[],
        required_keywords=[],
        preferred_companies=[],
        blocked_companies=[],
        preferred_locations=[],
        remote_bonus=5,
        days_threshold_fresh=7,
        days_threshold_old=60,
    )
    
    scorer = JobScorer(config)
    job = JobPosting(
        url="https://example.com/job/1",
        title="Python Developer",
        company="Tech Co",
        location="Remote",
        description="We need Python experts",
        source="duunitori",
    )
    
    scored = scorer.score(job)
    
    # 2 positive keywords matched (python, remote) = 20 points
    # remote bonus = 5 points
    # Total = 25 points
    assert scored.score == 25
    assert "python" in scored.matched_keywords or "remote" in scored.matched_keywords


def test_score_negative_keywords() -> None:
    """Test scoring with negative keywords."""
    config = ScoringConfig(
        positive_keywords=[],
        negative_keywords=["java", "windows"],
        required_keywords=[],
        preferred_companies=[],
        blocked_companies=[],
        preferred_locations=[],
        remote_bonus=0,
        days_threshold_fresh=7,
        days_threshold_old=60,
    )
    
    scorer = JobScorer(config)
    job = JobPosting(
        url="https://example.com/job/2",
        title="Java Developer",
        company="Corp",
        location="Office",
        description="Windows environment",
        source="duunitori",
    )
    
    scored = scorer.score(job)
    
    # 2 negative keywords = -40 points, clamped to 0
    assert scored.score == 0


def test_score_required_keywords_missing() -> None:
    """Test scoring penalizes missing required keywords."""
    config = ScoringConfig(
        positive_keywords=[],
        negative_keywords=[],
        required_keywords=["python", "kubernetes"],
        preferred_companies=[],
        blocked_companies=[],
        preferred_locations=[],
        remote_bonus=0,
        days_threshold_fresh=7,
        days_threshold_old=60,
    )
    
    scorer = JobScorer(config)
    job = JobPosting(
        url="https://example.com/job/3",
        title="Developer",
        company="Tech",
        location="Remote",
        description="We need someone",
        source="duunitori",
    )
    
    scored = scorer.score(job)
    
    # Missing required keywords = -50 points, clamped to 0
    assert scored.score == 0
    assert "required_missing" in scored.score_breakdown


def test_score_preferred_company() -> None:
    """Test scoring gives bonus for preferred companies."""
    config = ScoringConfig(
        positive_keywords=[],
        negative_keywords=[],
        required_keywords=[],
        preferred_companies=["Google", "Microsoft"],
        blocked_companies=[],
        preferred_locations=[],
        remote_bonus=0,
        days_threshold_fresh=7,
        days_threshold_old=60,
    )
    
    scorer = JobScorer(config)
    job = JobPosting(
        url="https://example.com/job/4",
        title="Engineer",
        company="Google",
        location="Remote",
        source="duunitori",
    )
    
    scored = scorer.score(job)
    
    # Preferred company = +15 points
    assert scored.score >= 15
    assert "preferred_company" in scored.score_breakdown


def test_score_blocked_company() -> None:
    """Test scoring heavily penalizes blocked companies."""
    config = ScoringConfig(
        positive_keywords=[],
        negative_keywords=[],
        required_keywords=[],
        preferred_companies=[],
        blocked_companies=["BadCorp"],
        preferred_locations=[],
        remote_bonus=0,
        days_threshold_fresh=7,
        days_threshold_old=60,
    )
    
    scorer = JobScorer(config)
    job = JobPosting(
        url="https://example.com/job/5",
        title="Great Job",
        company="BadCorp",
        location="Remote",
        source="duunitori",
    )
    
    scored = scorer.score(job)
    
    # Blocked company = -100 points, clamped to 0
    assert scored.score == 0
    assert "blocked_company" in scored.score_breakdown


def test_score_remote_bonus() -> None:
    """Test scoring gives bonus for remote positions."""
    config = ScoringConfig(
        positive_keywords=[],
        negative_keywords=[],
        required_keywords=[],
        preferred_companies=[],
        blocked_companies=[],
        preferred_locations=[],
        remote_bonus=20,
        days_threshold_fresh=7,
        days_threshold_old=60,
    )
    
    scorer = JobScorer(config)
    job = JobPosting(
        url="https://example.com/job/6",
        title="Developer",
        company="Tech",
        location="Remote",
        source="duunitori",
    )
    
    scored = scorer.score(job)
    
    # Remote bonus = 20 points
    assert scored.score >= 20
    assert "remote_bonus" in scored.score_breakdown


def test_score_recency_fresh() -> None:
    """Test scoring gives bonus for fresh postings."""
    config = ScoringConfig(
        positive_keywords=[],
        negative_keywords=[],
        required_keywords=[],
        preferred_companies=[],
        blocked_companies=[],
        preferred_locations=[],
        remote_bonus=0,
        days_threshold_fresh=7,
        days_threshold_old=60,
    )
    
    scorer = JobScorer(config)
    job = JobPosting(
        url="https://example.com/job/7",
        title="Developer",
        company="Tech",
        location="Remote",
        posted_date="2 days ago",
        source="duunitori",
    )
    
    scored = scorer.score(job)
    
    # Fresh posting = +10 points
    assert scored.score >= 10
    assert "recency_fresh" in scored.score_breakdown


def test_score_clamping() -> None:
    """Test score is clamped between 0 and 100."""
    config = ScoringConfig(
        positive_keywords=["python"] * 20,  # Would give 200+ points
        negative_keywords=[],
        required_keywords=[],
        preferred_companies=[],
        blocked_companies=[],
        preferred_locations=[],
        remote_bonus=0,
        days_threshold_fresh=7,
        days_threshold_old=60,
    )
    
    scorer = JobScorer(config)
    job = JobPosting(
        url="https://example.com/job/8",
        title="Python Python Python Developer",
        company="Tech",
        location="Remote",
        description="Python everywhere",
        source="duunitori",
    )
    
    scored = scorer.score(job)
    
    # Should be clamped to 100
    assert scored.score == 100


def test_score_category_high() -> None:
    """Test high-scoring job gets correct category."""
    config = ScoringConfig(
        positive_keywords=["python", "kubernetes", "docker"],
        negative_keywords=[],
        required_keywords=[],
        preferred_companies=["Google"],
        blocked_companies=[],
        preferred_locations=["Helsinki"],
        remote_bonus=10,
        days_threshold_fresh=7,
        days_threshold_old=60,
    )
    
    scorer = JobScorer(config)
    job = JobPosting(
        url="https://example.com/job/9",
        title="Python Kubernetes Engineer",
        company="Google",
        location="Helsinki Remote",
        description="Docker expertise required",
        posted_date="1 day ago",
        source="duunitori",
    )
    
    scored = scorer.score(job)
    
    # Should score high with multiple matches
    assert scored.score >= 70
    assert scored.category == "High Priority"
