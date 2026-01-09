# Applications MCP Server Design

**Date:** 2026-01-09
**Status:** Brainstorm complete, ready for implementation planning

## Problem Statement

Current file-system based storage with agent-generated content leads to:

- Inconsistent document structure (agents forget or make errors under pressure)
- Manual compilation steps
- Wrong language selection, missing frontmatter, PDF generation failures

Solution: MCP server as guardrails - agents can't create malformed records because tools enforce schema.

## Data Model

### Entities

```text
Company
  └── Correspondence (many)
  └── Postings (many)
        └── Application (0 or 1)
        └── Correspondence (many)
              └── Correspondence (many)
```

### Company

Implicit entity - created when first posting registered.

### Posting

**Required:**

- company
- position
- doc_language
- posting_md (job ad content)
- posting_url
- application_deadline

**Optional:**

- posting_source (platform, tool)
- contact
- salary_range
- location

### Application

Belongs to exactly one Posting. Created via `create_draft()`.

**Fields:**

- posting_id (FK)
- status: Draft | Ready | Submitted | Interview | Offer | Rejected | Withdrawn
- cv_md
- cover_letter_md
- fit_score
- applied_date
- revealed_path (filesystem export location)

### Correspondence

Linked to context (Company | Posting | Application).

**Fields:**

- context (polymorphic reference)
- date
- from ("me" = outgoing, otherwise sender address)
- to ("me" = incoming, otherwise recipient address)
- subject
- body
- attachments

### Event

Linked to context (Company | Posting | Application).

**Fields:**

- context
- date
- type: interview | promise | reminder | deadline
- description
- location (optional)
- status: pending | completed | cancelled | rescheduled
- rescheduled_to (event_id, if rescheduled)
- rescheduled_from (event_id, if created by reschedule)
- notes (optional, on completion/cancellation)
- reason (optional, on cancellation/reschedule)

## Tools

### Posting Management

```text
register_posting(
  company,
  position,
  doc_language,
  posting_md,
  posting_url,
  application_deadline,
  posting_source=None,
  contact=None,
  salary_range=None,
  location=None
)

list_postings()
```

### Application Workflow

```text
create_draft(posting_id)
# Creates application in Draft status

save_draft(application_id, cv_md, cover_letter_md)
# Updates draft content

reveal(application_id)
# Exports to filesystem, generates PDFs
# MCP remembers export path

sync_from_filesystem(application_id)
# Reads .md files from revealed path
# Updates database
# Regenerates PDFs

finalize(application_id)
# Status → Ready

mark_submitted(application_id)
# Status → Submitted
```

### Correspondence

```text
register_correspondence(
  context,    # company_id | posting_id | application_id
  date,
  from,       # "me" for outgoing
  to,         # "me" for incoming
  subject,
  body,
  attachments=None
)

correspondence(context)
# List all correspondence for context
```

### Events

```text
add_event(
  context,
  date,
  type,           # interview | promise | reminder | deadline
  description,
  location=None
)

reschedule_event(event_id, new_date, reason=None)
# Old event: status="rescheduled", rescheduled_to=new_event_id
# New event: created with same details, rescheduled_from=old_event_id

complete_event(event_id, notes=None)
# Status → completed

cancel_event(event_id, reason=None)
# Status → cancelled

list_events(context)
# All events for specific context (entity-focused)
# "What's the story of this thing?"

agenda(start_from=None, context=None)
# Time-focused view across all/filtered contexts
# "What needs my attention now?"
# Returns: { obligations: [...], deadlines: [...] }
```

### Agenda Response Format

```json
{
  "obligations": [
    {
      "id": "evt_123",
      "type": "interview",
      "date": "2026-01-10T10:00",
      "context": {
        "type": "application",
        "id": "app_456",
        "label": "Eesti Raudtee / Full-Stack arendaja"
      },
      "description": "On-site interview",
      "location": "Telliskivi tn 60/2",
      "status": "pending"
    }
  ],
  "deadlines": [
    {
      "id": "evt_789",
      "type": "deadline",
      "date": "2026-01-15",
      "context": {
        "type": "posting",
        "id": "post_321",
        "label": "Acme Corp / Backend Developer"
      },
      "description": "Application deadline",
      "status": "pending"
    }
  ]
}
```

### Status Tracking

```text
status(application_id)
# Returns list of status change events for the application
```

## Document Storage Philosophy

- **Database is source of truth** for all content
- **Filesystem is an export** via `reveal()`
- PDFs are generated on-the-fly, never stored
- `sync_from_filesystem()` reads edits back to database

## Naming Conventions

- `obligations` - things you committed to do (interviews, promises, reminders)
- `deadlines` - dates things close (application deadlines)
- `context` - polymorphic reference to Company | Posting | Application
- `from="me"` - outgoing correspondence
- `to="me"` - incoming correspondence

## Technology Decisions

- **Database:** EdgeDB (graph-relational, built on PostgreSQL)
- **Language:** TypeScript (best type inference with EdgeDB)
- **Deployment:** Docker (EdgeDB container, auto-starts with VS Code)
- **Event history:** All status changes kept (never delete, only mark status)
- **Reveal path:** `{export_root}/{Company}/{Position}/`

## Infrastructure

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

MCP servers run as TypeScript processes, connect to EdgeDB.

## Next Steps

1. Set up EdgeDB Docker + schema
2. Implement Applications MCP server (TypeScript)
3. Implement Knowledge Base MCP server (TypeScript)
4. Configure VS Code MCP integration
5. Migrate existing data
