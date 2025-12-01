# Job Monitoring System - Implementation Plan

**Status:** Planning Phase  
**Timeline:** 3 weeks (12-16 days effort)  
**Start Date:** TBD  
**Target Completion:** TBD

## Overview

Implement automated job portal monitoring system with type-safe architecture, integrated scoring, and seamless cv_system workflow integration.

## Architectural Decisions

### Core Technology Stack

- **Language:** Python 3.12+ with strict typing
- **Validation:** Pydantic v2 for runtime validation + schema generation
- **Type Checking:** mypy in strict mode for compile-time verification
- **Code Quality:** ruff for linting and formatting
- **Testing:** pytest with coverage reporting

### Key Design Principles

1. **Single Source of Truth:** Pydantic models define both runtime validation and TypeScript-equivalent type safety
2. **Explicit Over Implicit:** Pre-stage candidates, require human promotion to applications
3. **Progressive Complexity:** Start simple (state.json), migrate if needed (cache+index)
4. **Local-First:** All processing on local machine, no external services
5. **Manual Control:** No auto-apply, no auto-notifications initially

## Phase 1: Foundation & Type System (Week 1, Days 1-4)

### Deliverables

#### 1.1 Project Configuration

- **File:** `pyproject.toml`
- **Content:**
  - Dependencies: pydantic>=2.0, mypy>=1.0, ruff, pytest, requests, beautifulsoup4
  - Tool configurations: mypy strict settings, ruff rules, pytest options
  - Project metadata and scripts

#### 1.2 Type System Implementation

- **File:** `scripts/schemas.py`
- **Models:**

  ```python
  class JobPosting(BaseModel):
      id: str
      source: Literal["duunitori", "linkedin", "tyomarkkinatori"]
      url: str
      title: str
      company: str
      location: str
      posted_date: datetime | None
      discovered_date: datetime
      description: str | None
      salary: str | None
      contact: str | None

  class JobStatus(str, Enum):
      NEW = "new"
      REVIEWED = "reviewed"
      CANDIDATE = "candidate"
      APPLIED = "applied"
      REJECTED = "rejected"
      ARCHIVED = "archived"

  class ScoredJob(BaseModel):
      job: JobPosting
      score: int
      status: JobStatus
      first_seen: datetime
      last_seen: datetime
      notes: str | None

  class SourceConfig(BaseModel):
      name: str
      enabled: bool
      queries: list[QueryConfig]
      schedule: str
      max_results_per_query: int
      cookie_file: str

  class QueryConfig(BaseModel):
      keywords: str
      location: str = ""
      priority: Literal["high", "medium", "low"] = "medium"
      comment: str | None = None

  class ScoringConfig(BaseModel):
      keywords_match: dict[str, int]
      negative_keywords: dict[str, int] = {}
      companies_preferred: dict[str, int] = {}
      locations_preferred: dict[str, int] = {}
      recency_bonus: dict[str, int]
      threshold_review: int
      threshold_high_priority: int
      threshold_auto_apply: int

  class SystemConfig(BaseModel):
      sources: list[SourceConfig]
      scoring: ScoringConfig
      deduplication: dict[str, Any]
      notifications: dict[str, Any]
      retention: dict[str, int]

  class MonitorState(BaseModel):
      last_scan: datetime | None
      sources: dict[str, SourceState]
      seen_jobs: dict[str, ScoredJob]
      statistics: Statistics
  ```

#### 1.3 Configuration Manager

- **File:** `scripts/config_manager.py`
- **Functions:**
  - `load_config(path: Path) -> SystemConfig`
  - `validate_config(config: SystemConfig) -> list[str]`
  - `get_enabled_sources(config: SystemConfig) -> list[SourceConfig]`
  - `get_queries_for_source(source: SourceConfig) -> list[QueryConfig]`

#### 1.4 Refactor Existing Scraper

- **File:** `scripts/job_scraper.py` (modify)
- **Changes:**
  - Add type hints: `def search_duunitori(...) -> list[JobPosting]`
  - Replace dict returns with Pydantic models
  - Update `_parse_duunitori_job()` to return `JobPosting`
  - Add schema validation for inputs

#### 1.5 Development Tooling

- **Setup:**
  - Configure mypy: `mypy scripts/ --strict`
  - Configure ruff: `ruff check scripts/`
  - Add pre-commit hooks (optional)
  - Create `scripts/test_schemas.py` for validation tests

### Validation Checkpoint 1

- [ ] All schemas pass mypy strict mode
- [ ] Config files load without validation errors
- [ ] job_scraper.py returns properly typed JobPosting objects
- [ ] Run: `mypy scripts/ && pytest scripts/test_schemas.py`

## Phase 2: Core Monitoring Logic (Week 2, Days 5-8)

### Deliverables

#### 2.1 State Management

- **File:** `scripts/state_manager.py`
- **Class:** `StateManager`
- **Methods:**

  ```python
  def load_state(path: Path) -> MonitorState
  def save_state(state: MonitorState, path: Path) -> None
  def add_job(state: MonitorState, job: JobPosting, score: int) -> None
  def update_job(state: MonitorState, job_id: str, **updates) -> None
  def get_job(state: MonitorState, job_id: str) -> ScoredJob | None
  def cleanup_old_jobs(state: MonitorState, days: int) -> int
  def is_seen(state: MonitorState, job_id: str) -> bool
  ```

#### 2.2 Job Scoring Engine

- **File:** `scripts/job_scorer.py`
- **Class:** `JobScorer`
- **Methods:**

  ```python
  def __init__(config: ScoringConfig)
  def score_job(job: JobPosting) -> int
  def _score_keywords(text: str) -> int
  def _score_company(company: str) -> int
  def _score_location(location: str) -> int
  def _score_recency(posted_date: datetime | None) -> int
  def categorize(score: int) -> JobStatus
  def explain_score(job: JobPosting) -> dict[str, int]
  ```

#### 2.3 Deduplication System

- **File:** `scripts/deduplicator.py`
- **Functions:**

  ```python
  def generate_job_id(job: JobPosting) -> str  # URL hash
  def normalize_title_company(title: str, company: str) -> str
  def find_duplicates(jobs: list[JobPosting]) -> dict[str, list[JobPosting]]
  def is_duplicate(job1: JobPosting, job2: JobPosting, threshold: float) -> bool
  ```

#### 2.4 Main Orchestrator

- **File:** `scripts/job_monitor.py`
- **Class:** `JobMonitor`
- **Methods:**

  ```python
  def __init__(config_path: Path, state_path: Path)
  def scan(force: bool = False, dry_run: bool = False) -> ScanResult
  def _scrape_source(source: SourceConfig) -> list[JobPosting]
  def _process_jobs(jobs: list[JobPosting]) -> list[ScoredJob]
  def _categorize_jobs(scored_jobs: list[ScoredJob]) -> dict[JobStatus, list[ScoredJob]]
  def _save_candidates(candidates: list[ScoredJob], date: str) -> None
  def _update_statistics(result: ScanResult) -> None
  ```

### Validation Checkpoint 2

- [ ] State persistence works (load/save/update)
- [ ] Scoring algorithm produces expected results
- [ ] Duplicate detection finds same jobs
- [ ] Full scan completes without errors
- [ ] Run: `./scripts/job_monitor.py scan --dry-run`

## Phase 3: User Interface & Integration (Week 3, Days 9-12)

### Deliverables

#### 3.1 Candidate Storage

- **Structure:**

  ```text
  job_sources/
  ├── candidates/
  │   └── YYYY-MM-DD/
  │       ├── job_<id>.json       # Full JobPosting data
  │       ├── job_<id>_score.txt  # Score breakdown
  │       └── DIGEST.md           # Daily summary
  ```

#### 3.2 Digest Generator

- **File:** `scripts/digest_generator.py`
- **Functions:**

  ```python
  def generate_daily_digest(candidates: list[ScoredJob], date: str) -> str
  def format_job_summary(job: ScoredJob) -> str
  def create_digest_markdown(summaries: list[str]) -> str
  def save_digest(content: str, output_path: Path) -> None
  ```

- **Output Format:**

  ```markdown
  # Job Candidates - 2025-12-01

  ## High Priority (Score ≥ 20)

  ### Senior System Analyst @ Wärtsilä (Score: 23)

  - **Location:** Helsinki
  - **Posted:** 2 days ago
  - **Link:** https://...
  - **Why:** Keywords: system analyst (10), senior (2), location: Helsinki (3)

  ## Review (Score ≥ 15)

  ...
  ```

#### 3.3 Application Converter

- **File:** `scripts/job_to_application.py`
- **Functions:**

  ```python
  def convert_to_application(job_path: Path, company: str, position: str) -> Path
  def create_application_structure(company: str, position: str) -> Path
  def copy_job_posting(job: JobPosting, target_dir: Path) -> None
  def create_readme(job: JobPosting, target_dir: Path) -> None
  def update_registry(app_path: Path) -> None
  ```

- **Usage:**

  ```bash
  ./scripts/job_to_application.py \
    job_sources/candidates/2025-12-01/job_abc123.json \
    --company "Wärtsilä" \
    --position "Senior System Analyst"
  ```

#### 3.4 CLI Interface

- **File:** `scripts/job_monitor.py` (extend)
- **Commands:**

  ```python
  @click.group()
  def cli(): ...

  @cli.command()
  def scan(force: bool, dry_run: bool): ...

  @cli.command()
  def review(date: str): ...

  @cli.command()
  def stats(days: int): ...

  @cli.command()
  def mark(job_id: str, status: str, notes: str): ...

  @cli.command()
  def cleanup(days: int, dry_run: bool): ...

  @cli.command()
  def init(): ...
  ```

### Validation Checkpoint 3

- [ ] Digest generation produces readable markdown
- [ ] Candidate → application conversion creates proper structure
- [ ] CLI commands execute successfully
- [ ] Manual workflow test: scan → review → convert → apply
- [ ] Run: Full workflow simulation

## Phase 4: Testing & Documentation (Days 13-16)

### Deliverables

#### 4.1 Test Suite

- **Files:**
  - `scripts/test_schemas.py` - Model validation tests
  - `scripts/test_scorer.py` - Scoring algorithm tests
  - `scripts/test_deduplicator.py` - Duplicate detection tests
  - `scripts/test_state_manager.py` - State persistence tests
  - `scripts/test_integration.py` - End-to-end workflow tests

#### 4.2 Documentation

- **Update Files:**
  - `docs/job_monitoring_architecture.md` - Architecture overview (already exists)
  - `scripts/DUUNITORI_USAGE.md` - User guide (already exists, update)
  - `README.md` - Add job monitoring section
  - `job_sources/README.md` - Explain directory structure

#### 4.3 Example Workflows

- **File:** `docs/job_monitoring_workflows.md`
- **Content:**
  - Daily scan workflow
  - Manual review process
  - Application generation from candidate
  - Troubleshooting common issues
  - Cookie maintenance

#### 4.4 CI/CD Integration

- **Setup:**
  - Add GitHub Actions workflow for type checking
  - Add automated testing on PR
  - Add linting checks (ruff, mypy)

### Final Validation

- [ ] All tests pass: `pytest scripts/test_*.py`
- [ ] Type checking passes: `mypy scripts/ --strict`
- [ ] Linting passes: `ruff check scripts/`
- [ ] Documentation complete and accurate
- [ ] User acceptance testing: Manual scan → review → apply

## File Inventory

### New Files (17)

```text
pyproject.toml                           # Project config
scripts/schemas.py                       # Type definitions (500+ lines)
scripts/config_manager.py                # Config loading (200 lines)
scripts/state_manager.py                 # State persistence (300 lines)
scripts/job_scorer.py                    # Scoring engine (250 lines)
scripts/deduplicator.py                  # Duplicate detection (150 lines)
scripts/job_monitor.py                   # Main orchestrator (400 lines)
scripts/digest_generator.py              # Report generation (200 lines)
scripts/job_to_application.py            # Conversion tool (250 lines)
scripts/test_schemas.py                  # Unit tests (200 lines)
scripts/test_scorer.py                   # Unit tests (150 lines)
scripts/test_deduplicator.py             # Unit tests (100 lines)
scripts/test_state_manager.py            # Unit tests (150 lines)
scripts/test_integration.py              # Integration tests (200 lines)
docs/job_monitoring_workflows.md         # User workflows (100 lines)
job_sources/README.md                    # Directory guide (50 lines)
.github/workflows/job_monitoring.yml     # CI/CD (50 lines)
```

### Modified Files (3)

```text
scripts/job_scraper.py                   # Add type hints
docs/job_monitoring_architecture.md      # Update with actuals
scripts/DUUNITORI_USAGE.md               # Update commands
```

### Total Effort

- **New Code:** ~3,150 lines
- **Tests:** ~800 lines
- **Documentation:** ~150 lines
- **Total:** ~4,100 lines
- **Estimated Time:** 12-16 days (including testing/debugging)

## Risk Mitigation

### Technical Risks

1. **Cookie Expiration:** Implement expiration detection and user notification
2. **Portal Changes:** Abstract scraper interface, isolate portal-specific code
3. **Type System Complexity:** Start with essential models, expand as needed
4. **Performance:** Profile if state.json grows large (>10K jobs)

### Process Risks

1. **Scope Creep:** Defer Phase 2-4 architecture features to later iterations
2. **Time Overrun:** Prioritize Phase 1-3, Phase 4 can be incremental
3. **Integration Issues:** Test conversion workflow early (Phase 3.3)

## Success Criteria

### Functional Requirements

- ✅ Can scan multiple portals with multiple queries
- ✅ Deduplicates jobs across scans
- ✅ Scores jobs accurately (manual validation)
- ✅ Generates readable daily digest
- ✅ Converts candidates to applications smoothly

### Non-Functional Requirements

- ✅ Type-safe: mypy strict mode passes
- ✅ Reliable: All tests pass with >80% coverage
- ✅ Maintainable: Code follows PEP 8, documented
- ✅ Performant: Scan completes in <2 minutes
- ✅ User-friendly: Clear CLI, good error messages

## Next Steps

1. **Review & Approve Plan:** User confirms approach
2. **Set Up Milestone:** Create GitHub milestone "Job Monitoring v1.0"
3. **Create Issues:** Break down each phase into high-level issues
4. **Begin Phase 1:** Start with pyproject.toml and schemas.py
5. **Iterate:** Regular checkpoints, adjust plan as needed

## Notes

- Implementation plan assumes familiarity with Python, Pydantic, and cv_system
- Suitable for delegation to external developers with this document
- Each phase builds on previous - maintain strict ordering
- Checkpoints are mandatory - do not proceed if validation fails
- Plan is living document - update as work progresses
