"""
Application converter for job candidates.

Converts candidate JSON to application directory structure.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from job_monitor.schemas import ScoredJob


def sanitize_name(name: str) -> str:
    """Sanitize a name for use as directory name.
    
    Removes special characters, replaces spaces with underscores.
    """
    # Remove or replace problematic characters
    name = name.replace("õ", "o").replace("ä", "a").replace("ö", "o").replace("ü", "u")
    name = name.replace("Õ", "O").replace("Ä", "A").replace("Ö", "O").replace("Ü", "U")
    
    # Remove other special characters, keep alphanumeric, spaces, and hyphens
    name = re.sub(r'[^\w\s-]', '', name)
    
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    
    # Remove multiple consecutive underscores
    name = re.sub(r'_+', '_', name)
    
    # Strip leading/trailing underscores
    name = name.strip('_')
    
    return name


class ApplicationConverter:
    """Convert candidate jobs to application directory structure."""
    
    def __init__(self, applications_dir: Path, registry_path: Path) -> None:
        self.applications_dir = applications_dir
        self.registry_path = registry_path
    
    def convert(self, scored_job: ScoredJob, notes: str = "") -> Path:
        """Convert a scored job to application structure.
        
        Args:
            scored_job: The scored job to convert
            notes: Optional notes to add to README
            
        Returns:
            Path to created application directory
        """
        job = scored_job.job
        
        # Sanitize names for directory structure
        company_dir = sanitize_name(job.company)
        position_dir = sanitize_name(job.title)
        
        # Create directory structure
        app_dir = self.applications_dir / company_dir / position_dir
        app_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (app_dir / "communications").mkdir(exist_ok=True)
        (app_dir / "delivery").mkdir(exist_ok=True)
        
        # Generate README.md
        readme_content = self._generate_readme(scored_job, notes)
        readme_path = app_dir / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        # Create placeholder job posting file
        posting_path = app_dir / "tookuulutus.md"
        with open(posting_path, "w", encoding="utf-8") as f:
            f.write(self._generate_posting(scored_job))
        
        return app_dir
    
    def _generate_readme(self, scored_job: ScoredJob, notes: str) -> str:
        """Generate README.md content for application."""
        job = scored_job.job
        today = datetime.now().strftime("%Y-%m-%d")
        
        lines = [
            f"# {job.company} - {job.title} Application",
            "",
            f"**Company:** {job.company}",
            f"**Position:** {job.title}",
            f"**Application Date:** {today}",
            f"**Source:** {job.source}",
            f"**Job URL:** {job.url}",
        ]
        
        if job.location:
            lines.append(f"**Location:** {job.location}")
        
        if job.posted_date:
            lines.append(f"**Posted Date:** {job.posted_date}")
        
        lines.extend([
            "",
            "---",
            "",
            "## Job Score Analysis",
            "",
            f"### Overall Score: {scored_job.score:.1f}/100",
            "",
            f"**Category:** {scored_job.category}",
            "",
        ])
        
        if scored_job.matched_keywords:
            lines.extend([
                "**Matched Keywords:**",
                "",
            ])
            for kw in scored_job.matched_keywords:
                lines.append(f"- {kw}")
            lines.append("")
        
        if scored_job.score_breakdown:
            lines.extend([
                "**Score Breakdown:**",
                "",
            ])
            for key, value in scored_job.score_breakdown.items():
                lines.append(f"- {key}: {value:+.1f}")
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "## Job Description",
            "",
        ])
        
        if job.description:
            lines.append(job.description)
        else:
            lines.append("*No description available*")
        
        lines.extend([
            "",
            "---",
            "",
            "## Application Status",
            "",
            "**Status:** Draft",
            "",
        ])
        
        if notes:
            lines.extend([
                "**Notes:**",
                "",
                notes,
                "",
            ])
        
        lines.extend([
            "## Next Steps",
            "",
            "- [ ] Review job requirements in detail",
            "- [ ] Prepare tailored CV",
            "- [ ] Write motivation letter",
            "- [ ] Submit application",
            "",
        ])
        
        return "\n".join(lines)
    
    def _generate_posting(self, scored_job: ScoredJob) -> str:
        """Generate job posting markdown."""
        job = scored_job.job
        
        lines = [
            f"# {job.title}",
            "",
            f"**Company:** {job.company}",
            f"**Location:** {job.location or 'Not specified'}",
            f"**Posted:** {job.posted_date or 'Unknown'}",
            f"**Source:** {job.source}",
            f"**URL:** {job.url}",
            "",
            "---",
            "",
            "## Description",
            "",
        ]
        
        if job.description:
            lines.append(job.description)
        else:
            lines.append("*No description available*")
        
        lines.append("")
        
        return "\n".join(lines)
    
    def update_registry(
        self,
        company: str,
        position: str,
        score: float,
        app_link: str,
        notes: str = "",
    ) -> None:
        """Update applications/REGISTRY.md with new entry.
        
        Args:
            company: Company name
            position: Position title
            score: Fit score (0-100)
            app_link: Relative link to README
            notes: Optional notes
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Read current registry
        with open(self.registry_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find the table
        lines = content.split("\n")
        
        # Find where to insert (after last data row, before statistics)
        insert_idx = None
        for i, line in enumerate(lines):
            if line.startswith("## Statistics"):
                insert_idx = i - 1
                # Skip back past empty lines
                while insert_idx > 0 and not lines[insert_idx].strip():
                    insert_idx -= 1
                insert_idx += 1
                break
        
        if insert_idx is None:
            # Fallback: insert before last section
            insert_idx = len(lines) - 10
        
        # Create new entry row
        fit_score = f"{score:.0f}%"
        new_row = f"| {today} | {company} | {position} | {fit_score} | [README]({app_link}) | Not specified | Draft | {notes} |"
        
        # Insert new row
        lines.insert(insert_idx, new_row)
        
        # Update statistics
        for i, line in enumerate(lines):
            if line.startswith("- **Total Applications:**"):
                # Extract current count
                match = re.search(r'(\d+)', line)
                if match:
                    current = int(match.group(1))
                    lines[i] = f"- **Total Applications:** {current + 1}"
            elif line.startswith("- **Active (Draft/Ready):**"):
                match = re.search(r'(\d+)', line)
                if match:
                    current = int(match.group(1))
                    lines[i] = f"- **Active (Draft/Ready):** {current + 1}"
            elif line.startswith("**Last Updated:**"):
                lines[i] = f"**Last Updated:** {today}"
        
        # Write back
        with open(self.registry_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
