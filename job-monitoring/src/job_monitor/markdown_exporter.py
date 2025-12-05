#!/usr/bin/env python3
"""
Markdown exporter for job candidates.

Generates human-readable Markdown files alongside JSON for better browsability.
"""
from pathlib import Path

from job_monitor.schemas import ScoredJob


class MarkdownExporter:
    """Exports job candidates to Markdown format."""

    @staticmethod
    def _format_score_emoji(score: float) -> str:
        """Return emoji based on score."""
        if score >= 90:
            return "🌟"
        elif score >= 80:
            return "⭐"
        elif score >= 70:
            return "✨"
        elif score >= 60:
            return "💫"
        else:
            return "📌"

    @staticmethod
    def _format_category_emoji(category: str) -> str:
        """Return emoji based on category."""
        if category == "High Priority":
            return "🔥"
        elif category == "Review":
            return "📋"
        else:
            return "📁"

    @staticmethod
    def export_job(scored_job: ScoredJob, output_path: Path) -> None:
        """
        Export a scored job to Markdown format.

        Args:
            scored_job: The scored job to export
            output_path: Path to save the Markdown file
        """
        job = scored_job.job

        # Build markdown content
        lines = []

        # Title
        lines.append(f"# {job.title} - {job.company}")
        lines.append("")

        # Score and category
        score_emoji = MarkdownExporter._format_score_emoji(scored_job.score)
        category_emoji = MarkdownExporter._format_category_emoji(scored_job.category)
        lines.append(f"**Score:** {scored_job.score:.0f}/100 {score_emoji}")
        lines.append(f"**Category:** {scored_job.category} {category_emoji}")
        lines.append(f"**Location:** {job.location}")
        if job.posted_date:
            lines.append(f"**Posted:** {job.posted_date}")
        lines.append(f"**Discovered:** {job.discovered_date.strftime('%Y-%m-%d')}")
        lines.append("")

        # Quick info section
        lines.append("## Quick Info")
        lines.append("")
        lines.append(f"- **Company:** {job.company}")
        lines.append(f"- **Source:** {job.source}")
        lines.append(f"- **Location:** {job.location}")
        lines.append(f"- **URL:** [{job.url}]({job.url})")
        lines.append("")

        # Contact information (if available)
        has_contact = False
        if job.contact_name:
            if not has_contact:
                lines.append("### Contact Information")
                lines.append("")
                has_contact = True
            lines.append(f"- **Contact Person:** {job.contact_name}")
        if job.contact_email:
            if not has_contact:
                lines.append("### Contact Information")
                lines.append("")
                has_contact = True
            lines.append(f"- **Email:** {job.contact_email}")
        if job.contact_phone:
            if not has_contact:
                lines.append("### Contact Information")
                lines.append("")
                has_contact = True
            lines.append(f"- **Phone:** {job.contact_phone}")
        if has_contact:
            lines.append("")

        # Score breakdown
        lines.append("## Score Breakdown")
        lines.append("")
        for key, value in scored_job.score_breakdown.items():
            # Format the key nicely
            display_key = key.replace('_', ' ').title()
            sign = "+" if value >= 0 else ""
            lines.append(f"- **{display_key}:** {sign}{value:.0f} points")
        lines.append("")
        lines.append(f"**Total:** {scored_job.score:.0f}/100")
        lines.append("")

        # Matched keywords
        if scored_job.matched_keywords:
            lines.append(f"## Matched Keywords ({len(scored_job.matched_keywords)})")
            lines.append("")
            # Display keywords as comma-separated list
            keywords_str = ", ".join(sorted(set(scored_job.matched_keywords)))
            lines.append(keywords_str)
            lines.append("")

        # Job description
        if job.description:
            lines.append("## Job Description")
            lines.append("")
            # Clean up the description a bit
            desc = job.description.strip()
            # Replace multiple spaces with single space
            desc = " ".join(desc.split())
            # Add paragraph breaks for better readability
            # (assuming sentences ending with period + space indicate paragraphs)
            desc = desc.replace(". ", ".\n\n")
            lines.append(desc)
            lines.append("")

        # Action checklist
        lines.append("## Actions")
        lines.append("")
        lines.append("- [ ] Review job posting in detail")
        lines.append("- [ ] Check company culture and reviews")
        lines.append("- [ ] Prepare tailored CV and cover letter")
        lines.append("- [ ] Submit application")
        lines.append("- [ ] Follow up after 1 week")
        lines.append("")

        # Metadata footer
        lines.append("---")
        lines.append("")
        lines.append(f"*Job ID: {job.id}*  ")
        lines.append(f"*Status: {job.status}*  ")
        lines.append(f"*Exported: {job.discovered_date.strftime('%Y-%m-%d %H:%M')}*")

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    @staticmethod
    def export_jobs_batch(scored_jobs: list[ScoredJob], base_dir: Path) -> int:
        """
        Export multiple jobs to Markdown files.

        Args:
            scored_jobs: List of scored jobs to export
            base_dir: Base directory (e.g., candidates/2025-12-01/high_priority/)

        Returns:
            Number of files exported
        """
        count = 0
        for sj in scored_jobs:
            md_path = base_dir / f"{sj.job.id}.md"
            MarkdownExporter.export_job(sj, md_path)
            count += 1
        return count
