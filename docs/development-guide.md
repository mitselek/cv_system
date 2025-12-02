# Development Guide

**Last Updated:** December 2, 2025  
**Author:** Mihkel Putrinš

## Overview

This guide provides essential rules and best practices for developers working on the CV System project. All development must adhere to the principles defined in `/docs/constitution.md`.

## Code Quality Requirements

### 1. Type Safety (CRITICAL)

**Always check the problems tool after making code changes.**

- All Python code MUST have complete type hints
- Code MUST pass Pylance/mypy type checking without errors
- Fix type errors IMMEDIATELY before committing
- Use type narrowing assertions when needed (e.g., `assert value is not None`)

**Example Type Narrowing:**

```python
# BAD - causes type error
description: Optional[str] = get_description()
self.assertIn("keyword", description)  # ERROR: description might be None

# GOOD - type narrowing
description: Optional[str] = get_description()
self.assertIsNotNone(description)
assert description is not None  # Type narrowing for static checkers
self.assertIn("keyword", description)  # OK - description is str here
```

### 2. No Emojis Policy

**Emojis are restricted across the codebase:**

- **FORBIDDEN**: Professional documents (CVs, cover letters), commit messages, code comments
- **MINIMAL**: Technical documentation (only for critical status indicators)
- **ALLOWED**: User-facing runtime output where they add genuine value (⚠️ warnings, [ERROR])

**Preferred Alternatives:**

- Use text markers: `[DONE]`, `[TODO]`, `[FAILED]`, `[CRITICAL]`, `[WARNING]`
- Use clear labels: `Status: Complete`, `Priority: High`
- In code output: Use symbols sparingly and consistently

**Example:**

```python
# BAD
print(f"✅ Test passed!")
print(f"🔍 Searching for jobs...")

# GOOD
print(f"[DONE] Test passed")
print(f"Searching for jobs...")

# ACCEPTABLE in user-facing CLI output
print(f"⚠️  Warning: Rate limit approaching")
```

### 3. Testing Requirements

- All new features MUST have tests
- Run full test suite before committing: `pytest tests/ -q`
- Test coverage should not decrease
- Integration tests for cross-component functionality

### 4. Documentation Standards

- Update documentation alongside code changes
- Follow strict Markdown linting (see constitution.md)
- No trailing whitespace
- Single newline at end of file
- Blank lines before/after headings, lists, code blocks

### 5. Commit Message Guidelines

**Format:**

```text
Brief summary (imperative mood, <72 chars)

- Detailed change 1
- Detailed change 2
- Impact/rationale

Result: Tests passing, no type errors
```

**NO emojis, NO decorative symbols, just clear communication.**

## Common Patterns

### Working with Optional Types

```python
from typing import Optional

def process_data(value: Optional[str]) -> str:
    if value is None:
        return "default"
    # value is now known to be str
    return value.upper()
```

### Pydantic HttpUrl Usage

```python
from pydantic import HttpUrl

# BAD
job = JobPosting(url="https://example.com", ...)

# GOOD
job = JobPosting(url=HttpUrl("https://example.com"), ...)
```

### Error Handling in Scrapers

```python
try:
    result = risky_operation()
except Exception as e:
    print(f"Error: {e}")  # No emoji, clear message
    return []
```

## Development Workflow

1. **Before starting:**
   - Check open issues
   - Read relevant documentation
   - Understand the constitution rules

2. **During development:**
   - Write code with type hints
   - Check problems tool frequently
   - Write tests as you go
   - Follow no-emoji policy

3. **Before committing:**
   - Run full test suite
   - Check for type errors
   - Review changes for emojis
   - Update documentation if needed

4. **Commit:**
   - Clear, descriptive message
   - No emojis
   - Reference issues if applicable

## Tools & Commands

### Run Tests

```bash
# All tests
pytest tests/ -q

# Specific file
pytest tests/test_scrapers/test_duunitori.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### Type Checking

```bash
# Via Pylance in VS Code (automatic)
# Check problems panel regularly

# Via mypy (command line)
mypy src/
```

### Linting

```bash
# Python (via ruff or similar)
ruff check src/

# Markdown (markdownlint)
markdownlint docs/**/*.md
```

## Key Principles from Constitution

1. **Integrity:** Never fabricate or embellish data
2. **Structure:** Keep code modular and well-organized
3. **Quality:** Maintain high standards through testing and type safety
4. **Automation:** Automate repetitive tasks, focus human effort on strategy

## Questions?

- Review `/docs/constitution.md` for comprehensive rules
- Check existing code for patterns
- Ask for clarification in issues rather than assuming

## Remember

**Fix type errors immediately. Keep emojis out of code and commits. Test everything. Read the constitution.**
