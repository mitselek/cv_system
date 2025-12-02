"""
Job scoring utilities.

Scores JobPosting instances according to ScoringConfig.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from job_monitor.schemas import JobPosting, ScoredJob, ScoringConfig


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _contains_any(text: str, terms: Iterable[str]) -> list[str]:
    t = _normalize(text)
    found: list[str] = []
    for term in terms:
        term_n = term.strip().lower()
        if term_n and term_n in t:
            found.append(term)
    return found


def _days_ago_from_posted(posted: str | None) -> int | None:
    if not posted:
        return None
    s = posted.strip().lower()
    # "2 days ago" / "1 day ago"
    m = re.search(r"(\d+)\s+day", s)
    if m:
        return int(m.group(1))
    # YYYY-MM-DD
    try:
        dt = datetime.strptime(posted[:10], "%Y-%m-%d")
        return max((datetime.now() - dt).days, 0)
    except Exception:
        return None


class JobScorer:
    def __init__(self, config: ScoringConfig) -> None:
        self.cfg = config

    def score(self, job: JobPosting) -> ScoredJob:
        text = " ".join(
            [job.title, job.company or "", job.location or "", job.description or ""]
        )
        score = 0.0
        breakdown: dict[str, float] = {}
        matched: list[str] = []

        pos = _contains_any(text, self.cfg.positive_keywords)
        val = 10.0 * len(pos)
        score += val
        if val:
            breakdown["positive_keywords"] = val
            matched.extend(pos)

        neg = _contains_any(text, self.cfg.negative_keywords)
        val = -20.0 * len(neg)
        score += val
        if val:
            breakdown["negative_keywords"] = val

        # required keywords penalty if any missing
        # Handle OR logic: "python OR javascript" means at least one must be present
        missing_req = []
        for req in self.cfg.required_keywords:
            if " OR " in req:
                # Split by OR and check if any term is present
                terms = [t.strip().strip('"').lower() for t in req.split(" OR ")]
                if not any(term in _normalize(text) for term in terms):
                    missing_req.append(req)
            else:
                # Simple term check
                if req.lower() not in _normalize(text):
                    missing_req.append(req)
        
        if missing_req and self.cfg.required_keywords:
            score -= 50.0
            breakdown["required_missing"] = -50.0

        # company preferences
        if job.company:
            if _contains_any(job.company, self.cfg.preferred_companies):
                score += 15.0
                breakdown["preferred_company"] = breakdown.get("preferred_company", 0.0) + 15.0
            if _contains_any(job.company, self.cfg.blocked_companies):
                score -= 100.0
                breakdown["blocked_company"] = -100.0

        # location
        if job.location:
            if _contains_any(job.location, self.cfg.preferred_locations):
                score += 10.0
                breakdown["preferred_location"] = breakdown.get("preferred_location", 0.0) + 10.0
            if "remote" in _normalize(job.location):
                score += float(self.cfg.remote_bonus)
                breakdown["remote_bonus"] = float(self.cfg.remote_bonus)

        # recency
        days = _days_ago_from_posted(job.posted_date)
        if days is not None:
            if days <= self.cfg.days_threshold_fresh:
                score += 10.0
                breakdown["recency_fresh"] = 10.0
            elif days >= self.cfg.days_threshold_old:
                score -= 10.0
                breakdown["recency_old"] = -10.0

        # clamp
        score = max(0.0, min(100.0, score))

        return ScoredJob(
            job=job,
            score=score,
            score_breakdown=breakdown,
            matched_keywords=matched,
        )
