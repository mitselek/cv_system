"""
Job Monitoring System - Automated job discovery and tracking.

This package provides tools for monitoring job postings across multiple
job boards, scoring candidates, and tracking application status.
"""

__version__ = "1.0.0"

from .schemas import (
    JobPosting,
    JobStatus,
    ScoredJob,
    ScoringConfig,
    SourceConfig,
    SystemConfig,
)

__all__ = [
    "JobPosting",
    "JobStatus",
    "ScoredJob",
    "ScoringConfig",
    "SourceConfig",
    "SystemConfig",
]
