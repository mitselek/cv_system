"""Tests for job_to_application.py"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from pydantic import HttpUrl

from job_monitor.converter import ApplicationConverter, sanitize_name
from job_monitor.schemas import JobPosting, ScoredJob


def test_sanitize_name_basic() -> None:
    """Test basic name sanitization."""
    assert sanitize_name("Senior Python Developer") == "Senior_Python_Developer"
    assert sanitize_name("Full-Stack Developer") == "Full-Stack_Developer"


def test_sanitize_name_special_chars() -> None:
    """Test sanitization of Estonian characters."""
    assert sanitize_name("Süsteemianalüütik") == "Susteemianaluutik"
    assert sanitize_name("IT-osakonna juhataja") == "IT-osakonna_juhataja"
    assert sanitize_name("Äriprojektijuht") == "Ariprojektijuht"


def test_sanitize_name_removes_punctuation() -> None:
    """Test removal of special punctuation."""
    assert sanitize_name("Project Manager (Remote)") == "Project_Manager_Remote"
    assert sanitize_name("Dev & QA Lead") == "Dev_QA_Lead"


def test_sanitize_name_handles_multiple_spaces() -> None:
    """Test handling of multiple consecutive spaces."""
    assert sanitize_name("Senior    Developer") == "Senior_Developer"
    assert sanitize_name("  Lead  Engineer  ") == "Lead_Engineer"


@pytest.fixture
def sample_scored_job() -> ScoredJob:
    """Create a sample scored job for testing."""
    return ScoredJob(
        job=JobPosting(
            url=HttpUrl("https://example.com/job/123"),
            title="Senior Python Developer",
            company="Tech Corp",
            location="Remote",
            description="We are looking for a Senior Python Developer",
            posted_date="2025-12-01",
            source="duunitori",
        ),
        score=85.0,
        score_breakdown={"positive_keywords": 30.0, "remote_bonus": 15.0},
        matched_keywords=["python", "remote"],
    )


def test_convert_creates_directory_structure(sample_scored_job: ScoredJob) -> None:
    """Test that convert creates proper directory structure."""
    with TemporaryDirectory() as tmpdir:
        apps_dir = Path(tmpdir) / "applications"
        registry_path = Path(tmpdir) / "REGISTRY.md"
        
        # Create minimal registry
        registry_path.write_text("# Registry\n\n| Date | Company | Position |\n|------|---------|----------|\n")
        
        converter = ApplicationConverter(apps_dir, registry_path)
        app_dir = converter.convert(sample_scored_job)
        
        assert app_dir.exists()
        assert (app_dir / "README.md").exists()
        assert (app_dir / "tookuulutus.md").exists()
        assert (app_dir / "communications").exists()
        assert (app_dir / "communications").is_dir()
        assert (app_dir / "delivery").exists()
        assert (app_dir / "delivery").is_dir()


def test_convert_sanitizes_directory_names(sample_scored_job: ScoredJob) -> None:
    """Test that directory names are properly sanitized."""
    with TemporaryDirectory() as tmpdir:
        apps_dir = Path(tmpdir) / "applications"
        registry_path = Path(tmpdir) / "REGISTRY.md"
        registry_path.write_text("# Registry\n")
        
        converter = ApplicationConverter(apps_dir, registry_path)
        app_dir = converter.convert(sample_scored_job)
        
        # Should have Tech_Corp/Senior_Python_Developer structure
        assert app_dir.parent.name == "Tech_Corp"
        assert app_dir.name == "Senior_Python_Developer"


def test_readme_contains_job_details(sample_scored_job: ScoredJob) -> None:
    """Test that README contains all job details."""
    with TemporaryDirectory() as tmpdir:
        apps_dir = Path(tmpdir) / "applications"
        registry_path = Path(tmpdir) / "REGISTRY.md"
        registry_path.write_text("# Registry\n")
        
        converter = ApplicationConverter(apps_dir, registry_path)
        app_dir = converter.convert(sample_scored_job)
        
        readme = (app_dir / "README.md").read_text()
        
        assert "Senior Python Developer" in readme
        assert "Tech Corp" in readme
        assert "Remote" in readme
        assert "85.0/100" in readme
        assert "python" in readme
        assert "remote" in readme


def test_readme_includes_score_breakdown(sample_scored_job: ScoredJob) -> None:
    """Test that README includes score breakdown."""
    with TemporaryDirectory() as tmpdir:
        apps_dir = Path(tmpdir) / "applications"
        registry_path = Path(tmpdir) / "REGISTRY.md"
        registry_path.write_text("# Registry\n")
        
        converter = ApplicationConverter(apps_dir, registry_path)
        app_dir = converter.convert(sample_scored_job)
        
        readme = (app_dir / "README.md").read_text()
        
        assert "Score Breakdown" in readme
        assert "positive_keywords" in readme
        assert "remote_bonus" in readme


def test_readme_includes_notes(sample_scored_job: ScoredJob) -> None:
    """Test that notes are included in README."""
    with TemporaryDirectory() as tmpdir:
        apps_dir = Path(tmpdir) / "applications"
        registry_path = Path(tmpdir) / "REGISTRY.md"
        registry_path.write_text("# Registry\n")
        
        converter = ApplicationConverter(apps_dir, registry_path)
        notes = "Strong technical fit, great company culture"
        app_dir = converter.convert(sample_scored_job, notes=notes)
        
        readme = (app_dir / "README.md").read_text()
        
        assert notes in readme


def test_posting_file_contains_details(sample_scored_job: ScoredJob) -> None:
    """Test that tookuulutus.md contains job posting details."""
    with TemporaryDirectory() as tmpdir:
        apps_dir = Path(tmpdir) / "applications"
        registry_path = Path(tmpdir) / "REGISTRY.md"
        registry_path.write_text("# Registry\n")
        
        converter = ApplicationConverter(apps_dir, registry_path)
        app_dir = converter.convert(sample_scored_job)
        
        posting = (app_dir / "tookuulutus.md").read_text()
        
        assert "Senior Python Developer" in posting
        assert "Tech Corp" in posting
        assert "We are looking for a Senior Python Developer" in posting


def test_update_registry_adds_entry(sample_scored_job: ScoredJob) -> None:
    """Test that registry is updated with new entry."""
    with TemporaryDirectory() as tmpdir:
        registry_path = Path(tmpdir) / "REGISTRY.md"
        
        # Create realistic registry structure
        initial_content = """# Job Applications Registry

## Applications

| Date Applied | Company | Position | Fit Score | Application Link | Deadline | Status | Notes |
|-------------|---------|----------|-----------|------------------|----------|--------|-------|
| 2025-11-21 | OldCo | Old Position | 70% | [README](OldCo/Old_Position/README.md) | 2025-12-21 | Submitted | Test |

## Statistics

- **Total Applications:** 1
- **Active (Draft/Ready):** 0
- **Submitted:** 1

---

**Last Updated:** 2025-11-21
"""
        registry_path.write_text(initial_content)
        
        apps_dir = Path(tmpdir) / "applications"
        converter = ApplicationConverter(apps_dir, registry_path)
        
        converter.update_registry(
            company="Tech Corp",
            position="Senior Python Developer",
            score=85.0,
            app_link="Tech_Corp/Senior_Python_Developer/README.md",
            notes="Great fit"
        )
        
        updated = registry_path.read_text()
        
        assert "Tech Corp" in updated
        assert "Senior Python Developer" in updated
        assert "85%" in updated
        assert "Great fit" in updated


def test_update_registry_increments_counts(sample_scored_job: ScoredJob) -> None:
    """Test that registry statistics are updated."""
    with TemporaryDirectory() as tmpdir:
        registry_path = Path(tmpdir) / "REGISTRY.md"
        
        initial_content = """# Job Applications Registry

## Applications

| Date Applied | Company | Position | Fit Score | Application Link | Deadline | Status | Notes |
|-------------|---------|----------|-----------|------------------|----------|--------|-------|

## Statistics

- **Total Applications:** 5
- **Active (Draft/Ready):** 2
- **Submitted:** 3

---

**Last Updated:** 2025-11-21
"""
        registry_path.write_text(initial_content)
        
        apps_dir = Path(tmpdir) / "applications"
        converter = ApplicationConverter(apps_dir, registry_path)
        
        converter.update_registry(
            company="NewCo",
            position="New Position",
            score=90.0,
            app_link="NewCo/New_Position/README.md"
        )
        
        updated = registry_path.read_text()
        
        assert "**Total Applications:** 6" in updated
        assert "**Active (Draft/Ready):** 3" in updated
