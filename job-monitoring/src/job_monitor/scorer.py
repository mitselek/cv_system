"""
Job scoring utilities.

Scores JobPosting instances according to ScoringConfig.
"""
from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import datetime

from job_monitor.schemas import JobPosting, ScoredJob, ScoringConfig


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _contains_any(text: str, terms: Iterable[str], use_word_boundary: bool = False) -> list[str]:
    t = _normalize(text)
    found: list[str] = []
    for term in terms:
        term_n = term.strip().lower()
        if not term_n:
            continue
        if use_word_boundary:
            # Use word boundary regex to avoid substring matches like "intern" in "international"
            pattern = r'\b' + re.escape(term_n) + r'\b'
            if re.search(pattern, t):
                found.append(term)
        else:
            if term_n in t:
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

        # Use word boundary for negative keywords to avoid "intern" matching "international"
        neg = _contains_any(text, self.cfg.negative_keywords, use_word_boundary=True)
        val = -20.0 * len(neg)
        score += val
        if val:
            breakdown["negative_keywords"] = val

        # Title-based scoring: software/developer/arendaja titles get bonus
        title_lower = job.title.lower() if job.title else ""
        title_keywords = ["arendaja", "developer", "engineer", "programmer", "programmeerija",
                          "architect", "arhitekt", "lead", "manager"]
        if any(kw in title_lower for kw in title_keywords):
            score += 15.0
            breakdown["title_match"] = 15.0

        # Language bonus: Latvian or Russian in title/description
        lang_text = f"{job.title or ''} {job.description or ''}".lower()
        if "läti" in lang_text or "latvian" in lang_text or "latviešu" in lang_text:
            score += 20.0
            breakdown["language_latvian"] = 20.0
        if "vene" in lang_text or "russian" in lang_text or "русский" in lang_text:
            score += 10.0
            breakdown["language_russian"] = 10.0

        # required keywords penalty if any missing
        # Handle OR logic: "python OR javascript" means at least one must be present
        # But be lenient if description is missing/short (image-based ads)
        desc_len = len(job.description or "")
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
            # Softer penalty if description is missing/short (likely image-based ad)
            if desc_len < 100:
                score -= 15.0  # Mild penalty - we just don't know enough
                breakdown["required_missing_no_desc"] = -15.0
            else:
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
