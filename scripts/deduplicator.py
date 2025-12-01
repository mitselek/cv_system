"""
Duplicate detection for job postings.

Primary: URL (id)
Secondary: normalized (title + company)
"""
from __future__ import annotations

import re
from typing import Iterable

from schemas import JobPosting


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


class Deduplicator:
    def __init__(self) -> None:
        self.by_id: set[str] = set()
        self.by_fingerprint: set[str] = set()

    def _fingerprint(self, job: JobPosting) -> str:
        return f"{_norm(job.title)}|{_norm(job.company)}"

    def is_duplicate(self, job: JobPosting) -> bool:
        if job.id in self.by_id:
            return True
        fp = self._fingerprint(job)
        return fp in self.by_fingerprint

    def add(self, job: JobPosting) -> None:
        self.by_id.add(job.id)
        self.by_fingerprint.add(self._fingerprint(job))

    def filter_unique(self, jobs: Iterable[JobPosting]) -> list[JobPosting]:
        unique: list[JobPosting] = []
        for j in jobs:
            if not self.is_duplicate(j):
                self.add(j)
                unique.append(j)
        return unique
