# CV System - AI Agent Instructions

## Project Overview

Multi-component career management system with four main subsystems:

| Component | Language | Status | Purpose |
|-----------|----------|--------|---------|
| `job-monitoring/` | Python 3.12+ | v1.0.0 (prod) | Job discovery, scoring, CLI |
| `mcp-servers/knowledge-base/` | TypeScript | Active | MCP server for EdgeDB knowledge base |
| `email-monitor/` | Go | Phase 2 complete | IMAP email classification |
| `applications/` | Markdown | Active | Application tracking registry |

## Architecture

```
job-monitoring/src/job_monitor/   # Python: scrapers are plugins
  scrapers/base.py                # BaseScraper ABC - inherit for new portals
  scrapers/{cvee,duunitori}.py    # Existing implementations
  schemas.py                      # Pydantic models (JobPosting, ScoredJob, etc.)
  
mcp-servers/knowledge-base/       # TypeScript MCP server
  src/server.ts                   # Tool definitions (add_experience, search_skills, etc.)
  src/services/                   # EdgeDB service layer
  src/edgedb.ts                   # EdgeDB client wrapper

dbschema/default.esdl             # EdgeDB schema (Company, Posting, Application, etc.)
knowledge_base/                   # Markdown+YAML → compiled to _compiled_context.md
applications/REGISTRY.md          # Central tracking index
```

## Critical Conventions

### Type Safety (Strictly Enforced)
- **Always check VS Code Problems panel** after edits; fix type errors immediately

```python
# Python: mypy --strict must pass. Use type narrowing for Optional:
description: Optional[str] = get_description()
assert description is not None  # Required before using description
```

```typescript
// TypeScript: strict mode. EdgeDB queries return typed results:
const result = await client.query<{ id: string; title: string }>(query);
```

### No Emojis Policy

- **FORBIDDEN**: CVs, cover letters, commit messages, code comments
- **ALLOWED ONLY**: Runtime CLI output (warnings, status indicators)
- Use text markers: `[DONE]`, `[TODO]`, `[FAILED]` instead

### Pydantic Patterns

```python
# Always wrap URLs explicitly (Pydantic v2 requirement)
job = JobPosting(url=HttpUrl("https://example.com"), ...)

# Schemas auto-generate IDs from URL hash if not provided (see schemas.py model_validator)
```

## Developer Commands

```bash
# Job monitoring (Python)
cd job-monitoring && pip install -e ".[dev]"
job-monitor scan --config config.yaml              # Quick scan
pytest tests/ -q && mypy src/ && ruff check src/   # Full validation

# MCP Knowledge Base (TypeScript)
cd mcp-servers/knowledge-base
npm run dev                  # Watch mode with tsx
npm test                     # Vitest tests

# EdgeDB (Docker)
docker compose up -d edgedb  # Start database (port 5656)
edgedb migration create      # After schema changes in dbschema/default.esdl

# Knowledge Base Compilation
npm run compile              # Regenerate _compiled_context.md from knowledge_base/
```

## Adding New Job Scrapers

Pattern in [docs/adding-new-scrapers.md](../docs/adding-new-scrapers.md):

1. Create `job-monitoring/src/job_monitor/scrapers/{portal}.py`
2. Inherit `BaseScraper`, define: `SCRAPER_ID`, `DISPLAY_NAME`, `REQUIRES_COOKIES`
3. Implement: `_setup()`, `validate_config()`, `search(query: dict) -> list[JobPosting]`
4. Register in `scrapers/__init__.py`
5. Add tests in `tests/test_scrapers/`

## Knowledge Base Integrity

**Zero fabrication tolerance** - every claim must trace to a source file in `knowledge_base/`.

- Quote exact text; never infer or embellish
- When uncertain: **omit entirely**
- MCP server provides tools: `add_experience`, `search_skills`, `get_tag_usage`, etc.

## Application Tracking

- [applications/REGISTRY.md](../applications/REGISTRY.md) - central index with status
- Each application: `applications/{Company}/{Position}/` with README.md, CV, cover letter
- Status flow: Draft → Ready → Submitted → Interview → Offer/Rejected

## Key References

- [docs/constitution.md](../docs/constitution.md) - Core principles (MUST READ)
- [job-monitoring/src/job_monitor/schemas.py](../job-monitoring/src/job_monitor/schemas.py) - All Pydantic models
- [dbschema/default.esdl](../dbschema/default.esdl) - EdgeDB schema definitions
- [mcp-servers/knowledge-base/src/server.ts](../mcp-servers/knowledge-base/src/server.ts) - MCP tool definitions