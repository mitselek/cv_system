# CV System - AI Agent Instructions

## Architecture Overview

Multi-component career management system:

| Component | Language | Purpose |
|-----------|----------|---------|
| `job-monitoring/` | Python 3.12+ | Job discovery, scoring, CLI (v1.0.0) |
| `mcp-servers/knowledge-base/` | TypeScript | MCP server for EdgeDB knowledge base |
| `email-monitor/` | Go | IMAP email classification |
| `applications/` | Markdown | Application tracking registry |
| `knowledge_base/` | Markdown+YAML | Source of truth for CV data |

**Data Flow:** `knowledge_base/*.md` → MCP Server → EdgeDB (`localhost:5656`) ← Job Monitor

## Critical: Database & CLI

**Docker EdgeDB only** - never create local gel instances:

```bash
docker compose up -d edgedb          # Start: localhost:5656/main
gel -H localhost -P 5656 query "..." # Direct queries
gel migration create                 # After dbschema/default.gel changes
```

MCP server connects via `edgedb://edgedb@localhost:5656/main` (see `mcp-servers/knowledge-base/src/edgedb.ts`).

## Strict Policies

### Zero-Fabrication Rule (Constitutional Principle)

**Every claim in generated CVs/cover letters must trace to `knowledge_base/` files.**

- Quote exact source text - no paraphrasing or embellishment
- When uncertain: **OMIT entirely** (sparse content > fabricated content)
- Forbidden: inferred skills, "with focus on...", descriptive phrases not in source

### No Emojis

- **Forbidden in:** CVs, cover letters, commits, code comments
- **Allowed only:** Runtime CLI output (status indicators)
- Use: `[DONE]`, `[TODO]`, `[FAILED]` instead

### Type Safety

```python
# Python: mypy --strict, type narrowing for Optional
assert description is not None  # Before using Optional[str]
job = JobPosting(url=HttpUrl("https://..."))  # Explicit Pydantic v2 wrapping
```

```typescript
// TypeScript: strict mode, typed EdgeDB queries
const result = await client.query<{ id: string; title: string }>(query);
```

**Always check VS Code Problems panel after edits.**

## Developer Commands

```bash
# Job monitoring
cd job-monitoring && pip install -e ".[dev]"
job-monitor scan --config config.yaml
pytest tests/ -q && mypy src/ && ruff check src/

# MCP Knowledge Base
cd mcp-servers/knowledge-base
npm run dev     # tsx watch mode
npm test        # Vitest

# Email monitor (Go)
cd email-monitor && go build -o email-monitor ./cmd/
./email-monitor  # Requires .env with IMAP credentials
```

## Extending the System

### New Job Scrapers

1. Create `job-monitoring/src/job_monitor/scrapers/{portal}.py`
2. Inherit `BaseScraper` (see `scrapers/base.py` for ABC)
3. Define: `SCRAPER_ID`, `DISPLAY_NAME`, `REQUIRES_COOKIES`
4. Implement: `_setup()`, `validate_config()`, `search() -> list[JobPosting]`
5. Register in `scrapers/__init__.py`, test in `tests/test_scrapers/`

### Knowledge Base Entries

Each file: YAML frontmatter + Markdown body. Relationships via `skills_demonstrated: [skill-id]` in frontmatter.

MCP tools: `add_experience`, `add_skill`, `search_skills`, `get_tag_usage`, etc.

## Application Workflow

[applications/REGISTRY.md](../applications/REGISTRY.md) tracks all applications.

Structure: `applications/{Company}/{Position}/README.md` + CV + cover letter

Status flow: `Draft → Ready → Submitted → Interview → Offer/Rejected`

## Key Files

- [docs/constitution.md](../docs/constitution.md) - Governing principles (MUST READ)
- [job-monitoring/src/job_monitor/schemas.py](../job-monitoring/src/job_monitor/schemas.py) - Pydantic models
- [dbschema/default.gel](../dbschema/default.gel) - EdgeDB schema
- [mcp-servers/knowledge-base/src/server.ts](../mcp-servers/knowledge-base/src/server.ts) - MCP tool definitions
- [knowledge_base/_compiled_context.md](../knowledge_base/_compiled_context.md) - Compiled CV context for LLMs