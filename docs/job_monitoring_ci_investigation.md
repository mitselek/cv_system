# Job Monitoring CI Workflow Investigation

**Issue:** #34 - Fix job_monitoring.yml workflow: test failure and missing htmlcov/ artifact

**Investigation Date:** December 5, 2025

## Problem Summary

The `job_monitoring.yml` CI/CD workflow is failing with:

1. Test process exit code 1
2. Missing `htmlcov/` coverage report directory
3. Codecov upload failure

## Root Cause Analysis

### Issue 1: Incorrect Test Path Configuration

**Current Workflow:**

```yaml
- name: Run tests with coverage
  run: |
    pytest scripts/ --cov=scripts --cov-report=term --cov-report=xml --cov-report=html
```

**Problem:**

- Tests are configured to run from `scripts/` directory
- Actual test suite is located in `job-monitoring/tests/`
- `scripts/test_cvee_api.py` is not part of the main job monitoring test suite
- Mismatch between configured path and actual source structure

**Evidence:**

- Directory structure:
  - `/job-monitoring/tests/` - Main test suite (15+ test files)
  - `/job-monitoring/src/job_monitor/` - Source code
  - `/job-monitoring/pyproject.toml` - Project config specifies `testpaths = ["tests"]`
  - `/scripts/test_cvee_api.py` - Single utility test

### Issue 2: Missing Working Directory Context

**Problem:**

- Workflow runs from repository root (default)
- Attempts to run `pytest scripts/` which doesn't have all dependencies configured
- `pip install -e .` installs from repo root, not from `job-monitoring/` subdirectory
- `pyproject.toml` in `job-monitoring/` has specific pytest configuration that's not being used

**Evidence:**

```yaml
# pyproject.toml specifies:
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

### Issue 3: Missing Coverage Configuration

**Problem:**

- Coverage report generation depends on test discovery and execution
- If tests fail to run or collect properly, `htmlcov/` directory is never created
- Codecov action tries to upload report from `./coverage.xml` which also fails to generate

**Evidence:**

- GitHub Actions error: "No files were found with the provided path: htmlcov/"
- This indicates pytest's coverage report generation step never completed

## Solution

### Fix 1: Update Workflow Working Directory and Test Path

**Change from:**

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -e .
    pip install pytest pytest-cov mypy ruff types-pyyaml types-requests

- name: Run ruff linting
  run: |
    ruff check scripts/

- name: Run mypy type checking
  run: |
    mypy scripts/ --strict

- name: Run tests with coverage
  run: |
    pytest scripts/ --cov=scripts --cov-report=term --cov-report=xml --cov-report=html
```

**Change to:**

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    cd job-monitoring && pip install -e . && pip install pytest pytest-cov mypy ruff types-pyyaml types-requests

- name: Run ruff linting
  run: |
    cd job-monitoring && ruff check src/

- name: Run mypy type checking
  run: |
    cd job-monitoring && mypy src/ --strict

- name: Run tests with coverage
  run: |
    cd job-monitoring && pytest tests/ --cov=src --cov-report=term --cov-report=xml --cov-report=html
```

### Rationale

1. **`pip install -e .`** must run in `job-monitoring/` where `pyproject.toml` exists
2. **Linting and type checking** should target `src/job_monitor/` source code
3. **Tests** should run from `tests/` directory with pytest configuration from `pyproject.toml`
4. **Coverage reports** will be generated automatically in `job-monitoring/htmlcov/`

### Fix 2: Update Artifact Path

**Change from:**

```yaml
- name: Upload coverage HTML
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: coverage-report
    path: htmlcov/
```

**Change to:**

```yaml
- name: Upload coverage HTML
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: coverage-report
    path: job-monitoring/htmlcov/
```

### Fix 3: Update Test Count Check

**Change from:**

```yaml
- name: Check test count
  run: |
    TEST_COUNT=$(pytest scripts/ --collect-only -q | tail -1 | awk '{print $1}')
    echo "Total tests: $TEST_COUNT"
    if [ "$TEST_COUNT" -lt 100 ]; then
      echo "❌ Expected at least 100 tests, found $TEST_COUNT"
      exit 1
    fi
    echo "✅ Test count OK: $TEST_COUNT tests"
```

**Change to:**

```yaml
- name: Check test count
  run: |
    cd job-monitoring
    TEST_COUNT=$(pytest tests/ --collect-only -q | tail -1 | awk '{print $1}')
    echo "Total tests: $TEST_COUNT"
    if [ "$TEST_COUNT" -lt 100 ]; then
      echo "❌ Expected at least 100 tests, found $TEST_COUNT"
      exit 1
    fi
    echo "✅ Test count OK: $TEST_COUNT tests"
```

## Expected Outcome After Fix

1. ✅ All tests will be discovered from `job-monitoring/tests/`
2. ✅ Coverage report will be generated at `job-monitoring/htmlcov/`
3. ✅ Codecov will successfully upload coverage from `job-monitoring/coverage.xml`
4. ✅ Test count check will verify 100+ tests are passing
5. ✅ Workflow will complete successfully

## Testing the Fix

Before committing workflow changes:

```bash
cd job-monitoring
pip install -e .
pip install pytest pytest-cov mypy ruff types-pyyaml types-requests

# Test collection
pytest tests/ --collect-only -q

# Run tests with coverage
pytest tests/ --cov=src --cov-report=term --cov-report=xml --cov-report=html

# Verify htmlcov directory exists
ls -la htmlcov/
```

## References

- Workflow file: `.github/workflows/job_monitoring.yml`
- Project config: `job-monitoring/pyproject.toml`
- Test suite: `job-monitoring/tests/`
- Source code: `job-monitoring/src/job_monitor/`
