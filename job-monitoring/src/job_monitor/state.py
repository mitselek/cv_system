"""
State management for job monitoring system.

Provides simple JSON persistence with atomic writes and backup.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from job_monitor.schemas import JobPosting, MonitorState


class StateManager:
    """Handles loading/saving monitor state and common operations."""

    def __init__(self, state_file: Path) -> None:
        self.state_file = state_file
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state: MonitorState | None = None

    @property
    def state(self) -> MonitorState:
        if self._state is None:
            self._state = self.load_state()
        return self._state

    def load_state(self) -> MonitorState:
        if not self.state_file.exists():
            return MonitorState(
                last_scan=None,
                total_jobs_seen=0,
                total_candidates=0,
                total_applications=0,
                seen_jobs={},
                new_jobs=[],
                candidates=[],
                applied=[],
                stats_by_source={},
            )
        with open(self.state_file, encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
        # Pydantic validates and coalesces
        return MonitorState(**data)

    def save_state(self, state: MonitorState | None = None) -> None:
        s = state or self.state
        tmp = self.state_file.with_suffix(self.state_file.suffix + ".tmp")
        backup = self.state_file.with_suffix(self.state_file.suffix + ".bak")
        payload = s.model_dump(mode="json")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        if self.state_file.exists():
            # best-effort backup
            try:
                self.state_file.replace(backup)
            except Exception:
                pass
        tmp.replace(self.state_file)

    def is_seen(self, job_id: str) -> bool:
        return job_id in self.state.seen_jobs

    def add_job(self, job: JobPosting) -> None:
        if self.is_seen(job.id):
            return
        self.state.seen_jobs[job.id] = job
        self.state.total_jobs_seen += 1
        self.state.new_jobs.append(job.id)
        src = job.source
        self.state.stats_by_source[src] = self.state.stats_by_source.get(src, 0) + 1

    def update_job(self, job: JobPosting) -> None:
        self.state.seen_jobs[job.id] = job

    def get_job(self, job_id: str) -> JobPosting | None:
        return self.state.seen_jobs.get(job_id)

    def cleanup_old_jobs(self, days: int) -> int:
        """Archive jobs older than given days. Returns number archived."""
        if days <= 0:
            return 0
        now = datetime.now(datetime.UTC)
        archived = 0
        for job_id, job in list(self.state.seen_jobs.items()):
            # Use discovered_date as reference
            try:
                age_days = (now - job.discovered_date.replace(tzinfo=datetime.UTC)).days
            except Exception:
                continue
            if age_days > days:
                archived += 1
                # Minimal: remove from new list; keep in seen for history
                if job_id in self.state.new_jobs:
                    self.state.new_jobs.remove(job_id)
        return archived

    def touch_scan_time(self) -> None:
        self.state.last_scan = datetime.now()
