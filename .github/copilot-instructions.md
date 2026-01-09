# CV System - AI Agent Instructions

## Project Overview

Multi-component career management system: job monitoring (Python), knowledge base compiler (TypeScript), email monitor (Go), and application tracking. The **job-monitoring** system is production-ready (v1.0.0, 209 tests passing).

## Architecture

```
job-monitoring/           # Python: job discovery & scoring (primary component)
  src/job_monitor/
    scrapers/             # Plugin-based scrapers (Duunitori, CV.ee)
    schemas.py            # Pydantic models (JobPosting, JobStatus, etc.)
    scorer.py             # Keyword-based job ranking
knowledge_base/           # Markdown files with YAML frontmatter → compiled by TypeScript
applications/             # Job application tracking (REGISTRY.md is the index)
email-monitor/            # Go: IMAP email monitoring for job alerts
```

## Critical Conventions

### Type Safety (Enforced)

- **All Python code requires complete type hints** - code must pass `mypy --strict`
- **Always check VS Code Problems panel** after edits; fix type errors immediately
- Use type narrowing when working with Optional types:

```python
# Required pattern for Optional types
description: Optional[str] = get_description()
assert description is not None  # Type narrowing for static checkers
```

### No Emojis Policy

- **FORBIDDEN**: CVs, cover letters, commit messages, code comments
- **ALLOWED ONLY**: Runtime CLI output (⚠️ warnings, status indicators)
- Use text markers: `[DONE]`, `[TODO]`, `[FAILED]` instead

### Pydantic HttpUrl Usage

```python
# Always wrap URLs explicitly
job = JobPosting(url=HttpUrl("https://example.com"), ...)
```

## Developer Commands

```bash
# Job monitoring - primary workflow
cd job-monitoring
pip install -e ".[dev]"
job-monitor scan --config config.yaml           # Quick scan
job-monitor scan --config config.yaml --full-details  # Detailed (1.5s/job)

# Run tests (required before commits)
pytest tests/ -q                # All tests
pytest tests/ --cov=src         # With coverage

# Type checking
mypy src/

# Linting
ruff check src/
```

## Adding New Job Scrapers

Follow the plugin pattern in [docs/adding-new-scrapers.md](../docs/adding-new-scrapers.md):

1. Create `src/job_monitor/scrapers/{portal}.py` inheriting from `BaseScraper`
2. Define required class attributes: `SCRAPER_ID`, `DISPLAY_NAME`, `REQUIRES_COOKIES`
3. Implement `_setup()`, `validate_config()`, and `search()` methods
4. Register in `scrapers/__init__.py`
5. Add tests in `tests/test_scrapers/`

## Knowledge Base Integrity

The `knowledge_base/` is the **single source of truth** for all professional information. When generating application materials:

- **Zero fabrication tolerance** - every claim must trace to a source file
- Quote exact text from sources; never infer or embellish
- When uncertain about a detail: **omit it entirely**
- Run `npm run compile` after knowledge base updates to regenerate `_compiled_context.md`

## Application Tracking

- [applications/REGISTRY.md](../applications/REGISTRY.md) tracks all applications with status
- Each application has a subdirectory: `applications/{Company}/{Position}/`
- Status flow: Draft → Ready → Submitted → Interview → Offer/Rejected

## Key Files

- [docs/constitution.md](../docs/constitution.md) - Core principles and rules
- [docs/development-guide.md](../docs/development-guide.md) - Development workflow
- [job-monitoring/src/job_monitor/schemas.py](../job-monitoring/src/job_monitor/schemas.py) - Data models
- [job-monitoring/src/job_monitor/scrapers/](../job-monitoring/src/job_monitor/scrapers/) - Scraper plugins