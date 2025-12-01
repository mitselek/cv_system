# Execution Plan: Job Monitoring v1.0

**Duration**: 3 weeks (Dec 1 - Dec 22, 2025)

**Approach**: Sequential phase-gate with just-in-time breakdown

**Team**: 1 developer, full-time

**Current State**: Milestone and high-level issues created today (Dec 1), type annotations in job_scraper.py already complete

## Week-by-Week Timeline

### Week 1 (Dec 1-7): Phase 1 - Foundation & Type System

**Start**: Dec 2 (Monday)

**Breakdown**: Today (Dec 1)

**Daily Schedule**:

- **Mon Dec 2**: Create pyproject.toml with dependencies (pydantic>=2.0, mypy>=1.0, ruff, pytest), configure mypy strict mode, configure ruff linting rules, set up pytest configuration
- **Tue Dec 3**: Create schemas.py with all Pydantic models (JobPosting, JobStatus enum, ScoredJob, SourceConfig, QueryConfig, ScoringConfig, SystemConfig, MonitorState)
- **Wed Dec 4**: Build config_manager.py (load_config, validate_config, get_enabled_sources), start refactoring job_scraper.py to return JobPosting objects
- **Thu Dec 5**: Complete job_scraper.py refactoring with input validation, create test_schemas.py for validation tests
- **Fri Dec 6**: VALIDATION GATE - Run mypy strict, pytest, fix any issues
- **Fri-Sat Dec 6-7**: Break down Phase 2 (Issue #4) into 5 sub-issues

**Validation Gate (Dec 6)**:

- Run: `mypy scripts/ --strict`
- Expected: 0 errors
- Run: `pytest scripts/test_schemas.py`
- Expected: All tests green
- Verify: job_scraper.py returns JobPosting objects (not dicts)
- Verify: Config files load without validation errors

**If Failed**: Do NOT start Phase 2 - fix issues first. Allocate Dec 7 as buffer.

**Complexity Protocol**:

- If mypy strict reveals >50 errors by Dec 4 → Moderate complexity, create sub-issue "Fix mypy strict compatibility", extend Phase 1 to Dec 8
- If Pydantic schema conflicts with existing job_scraper.py structure → Create sub-issue "Refactor job_scraper.py for schema compatibility" (+2 days)

### Week 2 (Dec 8-14): Phases 2 & 3 Overlap

**Phase 2 Start**: Dec 9 (Monday)

**Breakdown Phase 2**: Dec 6-7 (while finishing Phase 1)

**Daily Schedule (Phase 2)**:

- **Mon Dec 9**: Create state_manager.py with StateManager class (load_state, save_state, add_job, update_job, get_job, cleanup_old_jobs, is_seen), implement atomic file operations with backup
- **Tue Dec 10**: Create job_scorer.py with JobScorer class, implement scoring algorithm (keyword matching, company/location preferences, recency bonus), add score explanation method
- **Wed Dec 11**: Create deduplicator.py (URL-based primary, title+company normalized secondary), begin job_monitor.py with JobMonitor class skeleton
- **Thu Dec 12**: Complete job_monitor.py orchestrator (scan workflow, _scrape_source, _process_jobs, _categorize_jobs, _save_candidates, _update_statistics), add --force and --dry-run support

**Phase 2 Validation Gate (Dec 12)**:

- Run: `./scripts/job_monitor.py scan --dry-run`
- Expected: Completes without errors
- Verify: State persistence works (load/save/update operations)
- Verify: Scoring produces expected results on test jobs (differentiation between priorities)
- Verify: Deduplication finds known duplicates (test with same job from different portals)

**If Failed**: Do NOT start Phase 3 - debug and fix issues. Document failure in issue comment.

**Phase 3 Start**: Dec 13 (Friday) - if Phase 2 passes validation

**Breakdown Phase 3**: Dec 11-12 (while finishing Phase 2)

**Daily Schedule (Phase 3)**:

- **Fri Dec 13**: Set up candidate directory structure (`job_sources/candidates/YYYY-MM-DD/`), create digest_generator.py to generate daily markdown reports with priority grouping
- **Mon Dec 15**: Create job_to_application.py converter (JSON → applications structure), test conversion against existing applications in REGISTRY.md
- **Tue Dec 16**: Extend job_monitor.py with click CLI commands (scan, review, stats, mark, cleanup, init), add help text and examples

### Week 3 (Dec 15-21): Phases 3 & 4

**Phase 3 Validation Gate (Dec 17)**:

- Test: Full manual workflow (scan → review candidates → convert to application → generate digest)
- Verify: Digest markdown is readable and accurate with proper priority grouping
- Verify: Application structure matches existing convention (compare with applications/REGISTRY.md entries)
- Verify: All CLI commands execute successfully (test each command with --help and actual runs)

**If Failed**: Do NOT start Phase 4 - fix integration issues first.

**Phase 4 Start**: Dec 18 (Wednesday)

**Breakdown Phase 4**: Dec 16-17 (while finishing Phase 3)

**Daily Schedule (Phase 4)**:

- **Wed Dec 18**: Create comprehensive test suite (test_schemas.py, test_scorer.py, test_deduplicator.py, test_state_manager.py), aim for >80% coverage
- **Thu Dec 19**: Create test_integration.py for end-to-end tests, update all documentation (job_monitoring_architecture.md, DUUNITORI_USAGE.md, create job_monitoring_workflows.md, job_sources/README.md, update main README.md)
- **Fri Dec 20**: Set up CI/CD (.github/workflows/job_monitoring.yml with mypy, ruff, pytest), FINAL VALIDATION

**Final Validation (Dec 20)**:

- Run: `pytest scripts/test_*.py --cov`
- Expected: All tests pass, coverage ≥80%
- Run: `mypy scripts/ --strict`
- Expected: 0 errors
- Run: `ruff check scripts/`
- Expected: 0 linting errors
- Verify: CI/CD pipeline green on GitHub Actions
- Verify: Documentation complete and accurate
- Test: User acceptance - complete workflow from scan to application

**Buffer**: Dec 21 (Saturday) - Final polish, address any remaining issues

**Milestone Complete**: Dec 22 (Sunday deadline)

## Breakdown Strategy

### Immediate (Today - Dec 1)

[ACTION] Break down Issue #3 (Phase 1) now into 5 sub-issues:

1. **"Setup Project Configuration"** (1 day) - Create pyproject.toml, configure mypy/ruff/pytest
2. **"Implement Pydantic Schemas"** (1 day) - Create schemas.py with all models
3. **"Build Configuration Manager"** (1 day) - Create config_manager.py
4. **"Refactor Job Scraper with Types"** (1 day) - Update job_scraper.py to return JobPosting objects (NOTE: Type annotations already complete!)
5. **"Setup Development Tooling"** (1 day) - Create test_schemas.py, verify mypy/ruff work

Label all sub-issues with: `type-system`, `enhancement`, assign to milestone "Job Monitoring v1.0"

### Rolling Breakdown (Each Phase)

Pattern: Break down next phase during final 2 days of current phase

- **Phase 1 (Dec 2-6)**: Break down Phase 2 on Dec 6-7
  - Create 4 sub-issues: State Manager, Job Scorer, Deduplicator, Main Orchestrator
  - Each ~1 day, label with `core-logic`, `enhancement`

- **Phase 2 (Dec 9-12)**: Break down Phase 3 on Dec 11-12
  - Create 4 sub-issues: Candidate Storage, Digest Generator, Application Converter, CLI Interface
  - Each ~1 day, label with `integration`, `enhancement`

- **Phase 3 (Dec 13-17)**: Break down Phase 4 on Dec 16-17
  - Create 4 sub-issues: Test Suite, Documentation, Example Workflows, CI/CD Integration
  - Each ~1 day, label with `testing`, `documentation`

### Why This Timing

- **Avoids over-planning**: Details about Phase 4 testing may change based on Phase 2 implementation approach
- **Reduces idle time**: Next phase ready when current completes, seamless transition
- **Incorporates learnings**: Phase 1 experience informs how to structure Phase 2 breakdown (e.g., if Pydantic schemas need more granularity)

## Dependency Management

### Critical Path

```text
Phase 1 (Foundation) → Phase 2 (Core Logic) → Phase 3 (Integration) → Phase 4 (Testing)
     4 days                 4 days                5 days                 3 days
  (Dec 2-6)              (Dec 9-12)            (Dec 13-17)            (Dec 18-20)
```

**Total Critical Path**: 16 days (with 5-day buffer for 21-day milestone)

### Blocking Relationships

**Phase 2 BLOCKED until Phase 1 completes**:

- Requires: schemas.py (JobPosting, ScoredJob, MonitorState models)
- Requires: config_manager.py (for loading source configurations)
- Requires: Refactored job_scraper.py (returns typed objects)
- Gate: mypy strict mode passes

**Phase 3 BLOCKED until Phase 2 completes**:

- Requires: job_monitor.py (to extend with CLI commands)
- Requires: state_manager.py (for candidate storage logic)
- Requires: job_scorer.py (for digest priority grouping)
- Gate: Dry-run scan completes successfully

**Phase 4 BLOCKED until Phase 3 completes**:

- Requires: All implementation complete (cannot write comprehensive tests for incomplete features)
- Requires: CLI commands working (for integration tests)
- Requires: Full workflow functional (for user acceptance testing)
- Gate: End-to-end manual workflow test passes

### Early Start Opportunities

While phases are sequential, preparatory research can happen in parallel without violating dependencies:

- **During Phase 1 (Dec 2-6)**:
  - Research scoring algorithms (keyword matching, TF-IDF, semantic similarity) for Phase 2
  - Review existing job_scraper.py patterns to inform Phase 2 orchestrator design
  - Draft example job postings for testing deduplication

- **During Phase 2 (Dec 9-12)**:
  - Draft CLI command structure and help text for Phase 3
  - Plan directory layout for candidates (where to store JSONs, digests)
  - Sketch digest markdown template format

- **During Phase 3 (Dec 13-17)**:
  - Outline test suite structure and test scenarios for Phase 4
  - Start documentation outline (table of contents, section structure)
  - Review CI/CD workflow examples from similar projects

## Complexity Handling Protocol

### If Estimate Exceeded

**Minor (+1-2 days)**:

1. Update issue estimate in comment with actual effort
2. Document reason (e.g., "unexpected mypy refactoring needed", "Pydantic validation more complex than expected")
3. Adjust next phase start date accordingly
4. No stakeholder escalation needed (single developer project)

**Example**: Phase 1 takes 6 days instead of 4 due to Pydantic schema complexity → Update Issue #3, shift Phase 2 start to Dec 11

**Moderate (+3-5 days)**:

1. Create new sub-issue for complex component (link to parent issue)
2. Document explanation in parent issue comment
3. Re-evaluate milestone timeline (may slip 1-2 days, still within buffer)
4. Consider if any Phase 4 scope can be deferred to v2.0

**Example**: Phase 2 scoring algorithm needs 7 days instead of 4 due to unexpected edge cases → Create sub-issue "Advanced scoring for remote vs hybrid positions" (+3 days), consider reducing Phase 4 test coverage from 80% to 70%

**Major (+5 days)**:

1. [RISK] Pause current work
2. Create planning discussion issue in GitHub
3. Evaluate options:
   - **Option A**: Extend milestone deadline to Dec 27 (+5 days buffer)
   - **Option B**: Descope non-critical features (reduce Phase 4 coverage to 60%, minimal docs)
   - **Option C**: Parallelize Phase 3 and Phase 4 (risky - overlap integration and testing)
4. Document decision in milestone description
5. Update timeline in this execution plan

**Example**: Phase 2 discovers that scoring algorithm needs ML model instead of keyword matching → [RISK] Pause, discuss options: keep simple keyword matching for v1.0 (defer ML to v2.0), or extend Phase 2 to 9 days and simplify Phase 4

### Discovered Complexity Examples

**Phase 1 Example**: Pydantic schema conflicts with existing job_scraper.py dict structure

- **Actual Complexity**: job_scraper.py uses nested dicts with optional fields, Pydantic requires explicit Optional typing
- **Action**: Create sub-issue "Refactor job_scraper.py dict returns to match Pydantic schema"
- **Estimate**: +2 days (moderate complexity)
- **Impact**: Phase 1 ends Dec 8 instead of Dec 6
- **Mitigation**: Start Phase 2 breakdown during extended Phase 1 (Dec 7-8), maintain momentum

**Phase 2 Example**: State management requires database instead of JSON files

- **Actual Complexity**: JSON file locking doesn't handle concurrent access, need SQLite
- **Action**: [RISK] Pause and evaluate - this is architectural change
- **Options**:
  - Keep JSON for v1.0 (document limitation: single-user only), defer SQLite to v2.0
  - Extend Phase 2 to 7 days to implement basic SQLite with proper locking
  - Use file locking library (fcntl) to make JSON concurrent-safe (+1 day)
- **Decision**: Choose simplest option that meets v1.0 requirements (likely file locking)

**Phase 3 Example**: Application converter breaks existing REGISTRY.md format

- **Actual Complexity**: Existing applications have inconsistent metadata format
- **Action**: Create sub-issue "Standardize REGISTRY.md format before conversion integration"
- **Estimate**: +1 day (minor complexity)
- **Impact**: Phase 3 takes 5 days instead of 4 (still within schedule)
- **Mitigation**: Use buffer day Dec 21 if needed

## Validation Checkpoints

### Phase 1 Gate (Dec 6)

**Must Pass**:

- [ ] `mypy scripts/ --strict` exits with 0 errors
- [ ] `pytest scripts/test_schemas.py` all tests green
- [ ] job_scraper.py returns JobPosting objects (not dict)
- [ ] Config files load without validation errors (test with sample config)
- [ ] All Pydantic models validate successfully (test with valid and invalid data)

**If Failed**:

- Do NOT start Phase 2 - fix issues first
- Allocate Dec 7 as buffer day for fixes
- If still failing by Dec 7 evening, trigger moderate complexity protocol

**Success Criteria**: All checkboxes above must be checked before Phase 2 breakdown

### Phase 2 Gate (Dec 12)

**Must Pass**:

- [ ] `./scripts/job_monitor.py scan --dry-run` completes without errors
- [ ] State persistence works: save state → load state → verify identical
- [ ] Scoring produces expected results on 10 test jobs (verify score differentiation)
- [ ] Deduplication finds known duplicates (test with same job, different URLs)
- [ ] Job categorization works: High Priority (>70), Review (40-70), Low Priority (<40)

**If Failed**:

- Do NOT start Phase 3 - debug and fix issues first
- Document failure mode in Issue #4 comment
- If scoring algorithm fundamentally broken, consider simple fallback (all jobs get medium score)

**Success Criteria**: Dry-run scan must complete full workflow without exceptions

### Phase 3 Gate (Dec 17)

**Must Pass**:

- [ ] Full workflow test: `scan` → `review` → convert → apply candidate
- [ ] Digest markdown is readable and accurate (verify formatting, links work)
- [ ] Application structure matches existing convention (compare with 3 existing applications)
- [ ] All CLI commands execute successfully: scan, review, stats, mark, cleanup, init
- [ ] Converted application appears correctly in `applications/REGISTRY.md`

**If Failed**:

- Do NOT start Phase 4 - fix integration issues first
- Most likely issue: directory structure mismatch or REGISTRY.md format error
- Test conversion with existing application first, then troubleshoot differences

**Success Criteria**: Must successfully convert 1 test candidate to application and verify in REGISTRY.md

### Phase 4 Gate (Dec 20)

**Must Pass**:

- [ ] Test coverage ≥80%: `pytest scripts/test_*.py --cov`
- [ ] CI/CD pipeline green on GitHub Actions (all checks pass)
- [ ] Documentation complete: all sections filled, no TODOs remaining
- [ ] User acceptance test: complete workflow from fresh scan to application submission
- [ ] Type checking passes: `mypy scripts/ --strict` with 0 errors
- [ ] Linting passes: `ruff check scripts/` with 0 errors

**If Failed**:

- If tests fail: Fix tests first, coverage is secondary
- If documentation incomplete: Use buffer day Dec 21 to finish
- If CI/CD fails: Check if issue is configuration or code (fix config issues immediately)

**Success Criteria**: All automated checks green + 1 successful end-to-end manual test

## Risk Mitigation

### Identified Risks

**[RISK-001]**: Phase 1 type system more complex than expected

- **Likelihood**: Medium
- **Impact**: High (blocks all subsequent phases)
- **Description**: job_scraper.py already has type annotations (completed earlier), but Pydantic schema integration may reveal conflicts. Mypy strict mode may expose hidden type issues in existing code.
- **Mitigation**:
  - Allocate Dec 7 as explicit buffer day for Phase 1
  - Use incremental refactoring: start with simple schemas, add complexity iteratively
  - If mypy shows >50 errors, create focused sub-issue and extend timeline
- **Trigger**: If mypy errors > 50 by Dec 4, or Pydantic validation fails on existing job data
- **Contingency**: If Phase 1 takes 6+ days, compress Phase 4 (reduce test coverage to 70%, defer documentation to post-v1.0)

**[RISK-002]**: Scoring algorithm ineffective

- **Likelihood**: Low
- **Impact**: Medium (may require algorithm redesign mid-implementation)
- **Description**: Keyword-based scoring may not differentiate jobs effectively. All jobs score similarly (all high or all low), making prioritization useless.
- **Mitigation**:
  - Prepare simple fallback: all jobs score 50 (manual review decides)
  - Test scoring with 20 real job postings early (Dec 10)
  - Document scoring as "v1.0 baseline" with clear upgrade path to ML in v2.0
- **Trigger**: Test jobs score unexpectedly (standard deviation <10 points, all jobs within 40-60 range)
- **Contingency**: Switch to simple category tags (must-apply, review, skip) instead of numeric scores

**[RISK-003]**: Integration with existing cv_system structure breaks

- **Likelihood**: Low
- **Impact**: High (breaks existing Copilot workflow)
- **Description**: Application converter creates incompatible directory structure or REGISTRY.md format, breaking existing application submission process.
- **Mitigation**:
  - Test application conversion early (Dec 15)
  - Compare against 3 existing applications in REGISTRY.md before implementation
  - Keep converter output identical to manual application creation
- **Trigger**: Existing application structure differs from assumptions in implementation plan
- **Contingency**: Manual application creation for v1.0, defer automated conversion to v1.1

**[RISK-004]**: Cookie authentication failures during development

- **Likelihood**: Medium
- **Impact**: Low (development can continue with test data)
- **Description**: Cookies expire quickly (CV Keskus requires active session), 403/401 errors during testing block integration validation.
- **Mitigation**:
  - Document cookie refresh procedure in DUUNITORI_USAGE.md (already exists)
  - Use --dry-run mode with cached test data for most testing
  - Refresh cookies once per week (Mondays) for integration tests
- **Trigger**: 403/401 errors during scan operations
- **Contingency**: Use mock data from existing successful scrapes stored in git for testing

**[RISK-005]**: Schedule slippage due to single developer

- **Likelihood**: Medium
- **Impact**: Medium (no parallel work possible to recover time)
- **Description**: Single developer means no backup if blocked or unavailable. Any significant blocker (illness, urgent issue) delays entire timeline.
- **Mitigation**:
  - Build in 5-day buffer (16 days work in 21-day milestone)
  - Identify descope candidates early (Phase 4 coverage, documentation depth)
  - Commit working code daily (allows resuming from known-good state)
- **Trigger**: 2+ days behind schedule by Week 2 (Dec 13)
- **Contingency Plans**: See below

### Contingency Plans

**If 2+ days behind by Week 2 (Dec 13)**:

- **Option A (Descope Phase 4)**: Reduce test coverage requirement from 80% to 60%, create minimal documentation (README updates only), defer comprehensive docs to v1.1
  - Recovers: ~2 days
  - Risk: Lower quality, technical debt

- **Option B (Extend Milestone)**: Extend milestone deadline to Dec 27 (+5 days buffer available)
  - Recovers: Full schedule flexibility
  - Risk: Delays other planned work

- **Option C (Parallel Phase 3/4)**: Start writing tests during Phase 3 implementation (risky - tests for incomplete code)
  - Recovers: ~2 days
  - Risk: High - tests may need complete rewrite

**Recommendation**: Option B (extend deadline) if serious issues, Option A (descope) if minor delays

**If critical blocker occurs (>5 days delay)**:

1. Pause work, document blocker in GitHub issue
2. Identify minimum viable product (MVP): Phases 1-2 only (scanning and scoring work, no UI)
3. Defer Phases 3-4 to "Job Monitoring v1.1" milestone
4. Ship MVP by Dec 15, complete v1.1 by Dec 27

## Communication Plan

### Daily

**What to Document**:

- Commit messages follow conventional format: `feat(module): description`, `fix(module): description`, `test(module): description`
- Update issue status in GitHub: add `in-progress` label when starting, remove when completing
- Document blockers immediately in issue comments with `[BLOCKED]` prefix
- Log any complexity discoveries in issue comments with `[COMPLEXITY]` prefix

**Example Commit**: `feat(schemas): Add Pydantic models for JobPosting and ScoredJob`

**Example Issue Comment**: `[COMPLEXITY] Discovered that mypy strict mode requires explicit Optional[] for all nullable fields. Adding +1 day to handle 30 affected locations.`

### Phase Boundaries

**What to Communicate** (document in phase issue comment):

- Validation checkpoint results: paste command outputs (mypy, pytest) into comment
- Next phase breakdown completion: link to created sub-issues
- Risks/blockers encountered during phase: document what triggered risk, how handled
- Lessons learned: what went well, what to adjust for next phase

**Example Phase 1 Completion Comment**:

```markdown
## Phase 1 Validation Complete ✓

**Validation Results**:
- mypy scripts/ --strict: 0 errors ✓
- pytest scripts/test_schemas.py: 15 tests passed ✓
- job_scraper.py returns JobPosting objects ✓

**Complexity Encountered**:
- Pydantic schema required more explicit typing than expected (+1 day)
- Resolved by adding Optional[] wrappers and default values

**Phase 2 Breakdown**:
Created sub-issues #7, #8, #9, #10 (see milestone)

**Lessons Learned**:
- Mypy strict mode catches many edge cases early - valuable
- Pydantic validation messages are helpful for debugging

**Ready to proceed to Phase 2** ✓
```

### Weekly (Fridays)

**Review Activities**:

- Review milestone progress using GitHub Projects view (if set up) or milestone page
- Update this execution plan if timeline adjusted (commit changes to plan document)
- Document any risks that materialized during week
- Estimate % completion vs schedule (on track / 1-2 days behind / 3+ days behind)

**Friday Check-in Template**:

```markdown
## Week N Check-in (Dec X)

**Progress**: Phase N: XX% complete
**Status**: [On Track | 1-2 Days Behind | Blocked]
**Risks Triggered**: [RISK-00X description] or "None"
**Adjustments**: [Describe any timeline or scope changes]
**Next Week Focus**: [Phase N completion and Phase N+1 start]
```

### Milestone Completion

**Deliverables to Create**:

1. **Close all issues**: Mark Issues #3, #4, #5, #6 as closed with completion comments
2. **Update implementation plan**: Edit `docs/job_monitoring_implementation_plan.md` with "Actual Effort" column showing real vs estimated days
3. **Document architectural decisions**: Create `docs/job_monitoring_decisions.md` capturing key design choices and rationale
4. **Create retrospective**: Create `docs/job_monitoring_retrospective.md` with:
   - What went well
   - What could be improved
   - Lessons learned for future phases
   - Ideas for v2.0

**Milestone Closure Comment**:

```markdown
## Job Monitoring v1.0 Complete ✓

**Completion Date**: Dec XX, 2025
**Planned Duration**: 21 days
**Actual Duration**: XX days

**Deliverables**:
- All 4 phases complete
- Test coverage: XX%
- Documentation: Complete
- CI/CD: Green

**See**:
- Retrospective: docs/job_monitoring_retrospective.md
- Architecture Decisions: docs/job_monitoring_decisions.md
- Updated Plan: docs/job_monitoring_implementation_plan.md
```

## Next Actions

### Immediate (Today - Dec 1)

1. [ACTION] Break down Issue #3 (Phase 1) into 5 sub-issues:
   - "Setup Project Configuration (pyproject.toml, mypy, ruff, pytest)"
   - "Implement Pydantic Schemas (schemas.py with all models)"
   - "Build Configuration Manager (config_manager.py)"
   - "Refactor Job Scraper with Types (job_scraper.py returns JobPosting)"
   - "Setup Development Tooling (test_schemas.py, validation)"

2. [ACTION] Set up development environment:
   - Ensure Python 3.11+ installed
   - Create virtual environment: `python -m venv venv`
   - Activate: `source venv/bin/activate`
   - Install initial dependencies: `pip install pydantic mypy ruff pytest`

3. [ACTION] Review existing code:
   - Read `scripts/job_scraper.py` (type annotations already complete)
   - Read `applications/REGISTRY.md` (understand application structure)
   - Read `docs/job_monitoring_implementation_plan.md` (detailed specs)

4. [ACTION] Schedule Phase 1 validation for Friday Dec 6 afternoon (3pm)

### Tomorrow (Dec 2 - Phase 1 Start)

1. [ACTION] Create `pyproject.toml` with project configuration:
   - Add dependencies: pydantic>=2.0, mypy>=1.0, ruff, pytest
   - Configure mypy strict mode with appropriate exclusions
   - Configure ruff linting rules for scripts/

2. [ACTION] Test mypy and ruff on existing code:
   - Run: `mypy scripts/job_scraper.py --strict`
   - Run: `ruff check scripts/job_scraper.py`
   - Document any existing issues to address during refactoring

3. [ACTION] Document any unexpected complexity immediately in Issue #3 comments

### This Week Focus (Dec 2-6)

**Primary Goal**: Complete Phase 1 and pass validation gate

**Key Milestones**:

- Mon-Tue: Configuration and schemas foundation
- Wed-Thu: Refactoring and testing
- Fri: Validation and Phase 2 breakdown

**Daily Checklist**:

- [ ] Commit working code at end of day
- [ ] Update sub-issue status (close when complete)
- [ ] Document blockers in issue comments
- [ ] Run mypy/ruff before committing

**Success Metric**: Phase 1 validation passes by Friday Dec 6, ready to start Phase 2 on Monday Dec 9

---

**This execution plan is a living document. Update as phases complete and new information emerges.**
