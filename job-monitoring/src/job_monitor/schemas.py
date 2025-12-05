"""
Pydantic schemas for job monitoring system.

This module defines all data models with runtime validation and type safety.
"""
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, model_validator


class JobStatus(str, Enum):
    """Status of a job posting in the monitoring workflow."""

    NEW = "new"  # Just discovered
    REVIEWED = "reviewed"  # Manually reviewed
    CANDIDATE = "candidate"  # Marked as candidate for application
    APPLIED = "applied"  # Application submitted
    REJECTED = "rejected"  # Not interested
    ARCHIVED = "archived"  # Old or no longer relevant


class JobPosting(BaseModel):
    """A job posting from any source portal."""

    # Identifiers
    id: str = Field(default="", description="Unique identifier (generated from url hash if not provided)")
    source: str = Field(default="unknown", description="Portal name (e.g., 'Duunitori', 'CV Keskus')")
    url: HttpUrl = Field(..., description="Direct link to job posting")

    # Core information
    title: str = Field(..., min_length=1, description="Job title")
    company: str = Field(default="Unknown", description="Company name")
    location: str = Field(default="", description="Job location")

    # Dates
    posted_date: str | None = Field(default=None, description="When job was posted (flexible format)")
    discovered_date: datetime = Field(default_factory=datetime.now, description="When we discovered it")

    # Content
    description: str | None = Field(default=None, description="Full job description (if available)")

    # Contact information (if available from job portal)
    contact_name: str | None = Field(default=None, description="Contact person name")
    contact_email: str | None = Field(default=None, description="Contact email address")
    contact_phone: str | None = Field(default=None, description="Contact phone number")

    # Status tracking
    status: JobStatus = Field(default=JobStatus.NEW, description="Current status in workflow")
    notes: str = Field(default="", description="User notes about this job")

    @model_validator(mode="before")
    @classmethod
    def generate_id_from_url(cls, data: Any) -> Any:
        """Generate ID from URL if not provided."""
        if isinstance(data, dict):
            if not data.get("id") or data.get("id") == "":
                if "url" in data:
                    import hashlib

                    url_str = str(data["url"])
                    data["id"] = hashlib.md5(url_str.encode()).hexdigest()[:16]
        return data

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "id": "a1b2c3d4e5f6g7h8",
                "source": "Duunitori",
                "url": "https://duunitori.fi/tyopaikat/tyo/12345",
                "title": "Project Manager - IT Infrastructure",
                "company": "TechCorp Oy",
                "location": "Helsinki",
                "posted_date": "2 days ago",
                "discovered_date": "2025-12-01T10:30:00",
                "description": "We are looking for an experienced project manager...",
                "status": "new",
                "notes": "",
            }
        }


class ScoredJob(BaseModel):
    """A job posting with calculated relevance score and metadata."""

    job: JobPosting = Field(..., description="The job posting")
    score: float = Field(..., ge=0.0, le=100.0, description="Relevance score (0-100)")
    score_breakdown: dict[str, float] = Field(
        default_factory=dict, description="Detailed scoring components"
    )
    matched_keywords: list[str] = Field(default_factory=list, description="Keywords that matched")
    category: str = Field(default="Review", description="High Priority / Review / Low Priority")

    @model_validator(mode="before")
    @classmethod
    def determine_category(cls, data: Any) -> Any:
        """Auto-determine category from score if not provided."""
        if isinstance(data, dict):
            # Only auto-determine if category not explicitly set or is default
            if "category" not in data or data.get("category") == "Review":
                if "score" in data:
                    score = data["score"]
                    if score >= 70:
                        data["category"] = "High Priority"
                    elif score >= 40:
                        data["category"] = "Review"
                    else:
                        data["category"] = "Low Priority"
        return data


class QueryConfig(BaseModel):
    """Configuration for a single job search query."""

    keywords: str = Field(..., min_length=1, description="Search keywords")
    location: str = Field(default="", description="Location filter")
    limit: int = Field(default=20, ge=1, le=100, description="Max results per source")


class SourceConfig(BaseModel):
    """Configuration for a job portal source."""

    name: str = Field(..., description="Portal name (duunitori, cvkeskus, etc.)")
    enabled: bool = Field(default=True, description="Whether to scrape this source")
    queries: list[QueryConfig] = Field(default_factory=list, description="Search queries for this source")
    cookies_file: Path | None = Field(default=None, description="Path to cookies file (if needed)")


class ScoringConfig(BaseModel):
    """Configuration for job scoring algorithm."""

    # Keyword matching
    positive_keywords: list[str] = Field(
        default_factory=list, description="Keywords that increase score (+10 each)"
    )
    negative_keywords: list[str] = Field(
        default_factory=list, description="Keywords that decrease score (-20 each)"
    )
    required_keywords: list[str] = Field(
        default_factory=list, description="Keywords that must be present (or -50 penalty)"
    )

    # Company preferences
    preferred_companies: list[str] = Field(
        default_factory=list, description="Companies to boost (+15 points)"
    )
    blocked_companies: list[str] = Field(
        default_factory=list, description="Companies to avoid (-100 points)"
    )

    # Location preferences
    preferred_locations: list[str] = Field(
        default_factory=list, description="Preferred locations (+10 points)"
    )
    remote_bonus: float = Field(default=15.0, description="Bonus for remote positions")

    # Recency
    days_threshold_fresh: int = Field(default=7, description="Jobs posted within this are 'fresh' (+10)")
    days_threshold_old: int = Field(default=30, description="Jobs older than this are 'old' (-10)")


class SystemConfig(BaseModel):
    """Top-level configuration for the job monitoring system."""

    sources: list[SourceConfig] = Field(default_factory=list, description="Job portals to scrape")
    scoring: ScoringConfig = Field(default_factory=ScoringConfig, description="Scoring algorithm config")

    # Storage
    state_file: Path = Field(
        default=Path("job_sources/monitor_state.json"), description="Where to store monitoring state"
    )
    candidates_dir: Path = Field(
        default=Path("job_sources/candidates"), description="Where to store candidate jobs"
    )

    # Behavior
    scan_interval_hours: int = Field(default=24, ge=1, description="How often to scan (for scheduled runs)")
    auto_archive_days: int = Field(default=60, description="Auto-archive jobs older than this")


class MonitorState(BaseModel):
    """Persistent state tracking for the job monitoring system."""

    last_scan: datetime | None = Field(default=None, description="When last scan completed")
    total_jobs_seen: int = Field(default=0, description="Total jobs discovered (all time)")
    total_candidates: int = Field(default=0, description="Total jobs marked as candidates")
    total_applications: int = Field(default=0, description="Total applications submitted")

    # All jobs ever seen (by ID)
    seen_jobs: dict[str, JobPosting] = Field(
        default_factory=dict, description="All jobs indexed by ID"
    )

    # Jobs by status
    new_jobs: list[str] = Field(default_factory=list, description="Job IDs with status=new")
    candidates: list[str] = Field(default_factory=list, description="Job IDs with status=candidate")
    applied: list[str] = Field(default_factory=list, description="Job IDs with status=applied")

    # Statistics by source
    stats_by_source: dict[str, int] = Field(
        default_factory=dict, description="Job count by portal name"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "last_scan": "2025-12-01T14:30:00",
                "total_jobs_seen": 157,
                "total_candidates": 12,
                "total_applications": 3,
                "seen_jobs": {},
                "new_jobs": [],
                "candidates": [],
                "applied": [],
                "stats_by_source": {"Duunitori": 89, "CV Keskus": 68},
            }
        }
