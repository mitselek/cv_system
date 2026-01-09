# Knowledge Base MCP Server Design

**Date:** 2026-01-09
**Status:** Brainstorm complete, ready for implementation planning

## Problem Statement

Current file-based knowledge base works but has friction:

- Agents read entire `_compiled_context.md` (~1000+ lines) even when only 20% is relevant
- Manual compilation step after edits (sometimes agent does it, sometimes not)
- No schema enforcement on writes - agents can create malformed entries

## Solution

MCP server that provides:

1. **Focused queries** - search by tags, keywords, filters
2. **Schema enforcement** - valid entries only
3. **Auto-compile** - `_compiled_context.md` regenerates on any change
4. **Controlled vocabulary** - classifiers with helpful error messages

## Data Model

### Core Entities

**Experience**

- id
- company (et/en)
- title (et/en)
- dates (start, end)
- location
- description (et/en)
- tags[]
- skills_demonstrated[]
- achievements[]
- technologies[]
- url, repository (optional)
- status, last_verified

**Skill**

- id
- skill_name (et/en)
- category
- proficiency_level
- tags[]
- usage_period
- evidence[]

**Achievement**

- id
- title (et/en)
- description (et/en)
- experience_id (optional link)
- date
- tags[]

### Classifiers

**Tag** - controlled vocabulary for categorization
**Category** - skill categories (Development Tools, Data, etc.)

## Tools

### Experience Operations

```text
search_experiences(
  tags=None,        # filter by controlled tags
  keywords=None,    # free-text search in content
  date_range=None   # {start, end}
)

get_experience(id)

add_experience(
  company,
  title,
  dates,
  location,
  description,
  tags=[],
  skills_demonstrated=[],
  ...
)

update_experience(id, ...)
```

### Skill Operations

```text
search_skills(
  category=None,
  min_proficiency=None,
  tags=None,
  keywords=None
)

get_skill(id)

add_skill(
  skill_name,
  category,
  proficiency_level,
  tags=[],
  ...
)

update_skill(id, ...)
```

### Achievement Operations

```text
search_achievements(
  keywords=None,
  experience_id=None,
  tags=None
)

get_achievement(id)

add_achievement(
  title,
  description,
  experience_id=None,
  date=None,
  tags=[],
  ...
)

update_achievement(id, ...)
```

### Classifier Operations

```text
list_tags()
add_tag(name)

list_categories()
add_category(name)
```

## Search Semantics

**tags** - structured, controlled vocabulary

- Exact match on predefined values
- Example: `tags=["java", "spring-boot"]`

**keywords** - free-text search in content

- Searches in title, description, company name, etc.
- Example: `keywords="migration"` finds "email migration", "data migration"

Both can be combined: experiences tagged "java" AND mentioning "migration".

## Classifier Behavior

When unknown classifier value is used:

```text
add_experience(..., tags=["java", "cloud-native"])
```

MCP responds with error:

```text
{
  "error": "unknown_tag",
  "message": "'cloud-native' is new for me.",
  "existing_tags": ["java", "spring-boot", "python", "nodejs", ...],
  "hint": "If you still want to add this tag (maybe consult user), use add_tag('cloud-native') first."
}
```

This teaches agents the vocabulary while requiring explicit intent for new terms.

## Auto-Compile Behavior

Any write operation triggers:

1. Update internal database
2. Regenerate `_compiled_context.md`
3. Return success with updated entity

No manual compile step needed.

## Obsidian Compatibility

The knowledge base should remain Obsidian-friendly:

- Markdown files in `knowledge_base/` directory
- YAML frontmatter for structured data
- `[[wikilinks]]` for connections
- MCP reads/writes these files (or syncs to them)

## Technology Decisions

- **Source of truth:** Database (EdgeDB)
- **Database:** EdgeDB (shared with Applications MCP)
- **Language:** TypeScript (best type inference with EdgeDB)
- **Output:** Auto-compile generates `_compiled_context.md` only (no individual .md export for now)
- **Entity patterns:** Education, certifications, projects follow same patterns as experiences

## Integration with Applications MCP

When drafting an application:

1. Agent reads posting from Applications MCP
2. Agent queries KnB MCP: `search_experiences(tags=["java"])`, `search_skills(...)`
3. Agent writes CV/cover letter
4. Agent saves to Applications MCP

Both MCPs share the same EdgeDB instance, but are separate MCP servers.

## Infrastructure

Shared with Applications MCP:

```yaml
# docker-compose.yml
services:
  edgedb:
    image: edgedb/edgedb
    volumes:
      - edgedb-data:/var/lib/edgedb
    ports:
      - "5656:5656"
```

## Next Steps

1. Define EdgeDB schema for KnB entities
2. Implement KnB MCP server (TypeScript)
3. Migrate existing knowledge_base/ data to EdgeDB
4. Configure auto-compile trigger
