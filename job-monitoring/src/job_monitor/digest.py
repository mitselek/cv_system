"""
Daily digest generator for job candidates.

Creates markdown reports grouping candidates by priority.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Sequence

from job_monitor.schemas import ScoredJob


class DigestGenerator:
    """Generate markdown digest reports from scored job candidates."""

    def __init__(self, candidates_dir: Path) -> None:
        self.candidates_dir = candidates_dir

    def generate_digest(self, date: str | None = None) -> str:
        """Generate markdown digest for a specific date.

        Args:
            date: Date string in YYYY-MM-DD format. If None, uses today.

        Returns:
            Markdown formatted digest string.
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        day_dir = self.candidates_dir / date

        if not day_dir.exists():
            return f"# Job Candidates Digest - {date}\n\nNo candidates found for this date.\n"

        # Load candidates from all categories
        high_jobs = self._load_candidates(day_dir / "high_priority")
        review_jobs = self._load_candidates(day_dir / "review")
        low_jobs = self._load_candidates(day_dir / "low_priority")

        # Sort by score within each category (highest first)
        high_jobs.sort(key=lambda x: x.score, reverse=True)
        review_jobs.sort(key=lambda x: x.score, reverse=True)
        low_jobs.sort(key=lambda x: x.score, reverse=True)

        total = len(high_jobs) + len(review_jobs) + len(low_jobs)

        # Build markdown
        lines = [
            f"# Job Candidates Digest - {date}",
            "",
            "## Summary",
            "",
            f"**Total Candidates**: {total}",
            f"- 🔥 High Priority: {len(high_jobs)}",
            f"- 📋 Review: {len(review_jobs)}",
            f"- 💤 Low Priority: {len(low_jobs)}",
            "",
        ]

        if high_jobs:
            lines.extend(self._format_section("🔥 High Priority", high_jobs, day_dir))

        if review_jobs:
            lines.extend(self._format_section("📋 Review", review_jobs, day_dir))

        if low_jobs:
            lines.extend(self._format_section("💤 Low Priority", low_jobs, day_dir))

        return "\n".join(lines)

    def _load_candidates(self, category_dir: Path) -> list[ScoredJob]:
        """Load all scored jobs from a category directory."""
        import json

        if not category_dir.exists():
            return []

        jobs = []
        for json_file in category_dir.glob("*.json"):
            try:
                with open(json_file, encoding="utf-8") as f:
                    data = json.load(f)
                    jobs.append(ScoredJob(**data))
            except Exception as e:
                print(f"Warning: Failed to load {json_file}: {e}")

        return jobs

    def _format_section(self, title: str, jobs: Sequence[ScoredJob], day_dir: Path) -> list[str]:
        """Format a section of jobs for the digest."""
        lines = [
            f"## {title}",
            "",
        ]

        for i, sj in enumerate(jobs, 1):
            job = sj.job

            # Determine category subdirectory
            if "High" in title:
                category = "high_priority"
            elif "Review" in title:
                category = "review"
            else:
                category = "low_priority"

            json_path = day_dir / category / f"{job.id}.json"
            # Path relative to the digest file location (day_dir)
            relative_json = category + "/" + f"{job.id}.json"

            lines.extend([
                f"### {i}. {job.title}",
                "",
                f"**Company**: {job.company}",
                f"**Location**: {job.location or 'N/A'}",
                f"**Score**: {sj.score:.1f}/100",
                f"**Source**: {job.source}",
                f"**URL**: {job.url}",
            ])

            if job.posted_date:
                lines.append(f"**Posted**: {job.posted_date}")

            if sj.matched_keywords:
                keywords = ", ".join(sj.matched_keywords)
                lines.append(f"**Matched Keywords**: {keywords}")

            if job.description:
                # Truncate long descriptions
                desc = job.description[:200] + "..." if len(job.description) > 200 else job.description
                lines.extend([
                    "",
                    f"**Description**: {desc}",
                ])

            lines.extend([
                "",
                f"📄 [Full Details]({relative_json})",
                "",
            ])

        return lines

    def save_digest(self, date: str | None = None) -> Path:
        """Generate and save digest to file.

        Args:
            date: Date string in YYYY-MM-DD format. If None, uses today.

        Returns:
            Path to saved digest file.
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        digest = self.generate_digest(date)

        day_dir = self.candidates_dir / date
        day_dir.mkdir(parents=True, exist_ok=True)

        digest_path = day_dir / "digest.md"
        with open(digest_path, "w", encoding="utf-8") as f:
            f.write(digest)

        return digest_path
