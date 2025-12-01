# Job Sources Directory

This directory contains job monitoring data, state, and candidates.

## Structure

```text
job_sources/
├── candidates/          # Daily candidate directories
│   └── YYYY-MM-DD/     # Date-stamped folders
│       ├── high_priority/   # Score ≥70
│       ├── review/          # Score 40-70
│       ├── low_priority/    # Score <40
│       └── DIGEST.md        # Daily summary
├── state.json          # Monitoring state and history
└── cookies.json        # Authentication cookies for job portals
```

## Files

### candidates/

Contains all discovered job candidates organized by date and score category.

**Directory naming**: `YYYY-MM-DD` (e.g., `2025-12-01`)

**Categories**:

- `high_priority/`: Jobs scoring 70 or higher - excellent matches
- `review/`: Jobs scoring 40-69 - worth reviewing
- `low_priority/`: Jobs scoring below 40 - poor matches

Each candidate is stored as JSON with the full job posting and scoring details:

```json
{
  "job": {
    "id": "abc123def456",
    "title": "Senior System Analyst",
    "company": "Tech Corp",
    "location": "Helsinki",
    "url": "https://example.com/job",
    "source": "duunitori.fi",
    "discovered_date": "2025-12-01T08:00:00+00:00",
    "description": "Full job description...",
    "status": "new"
  },
  "score": 85.0,
  "category": "High Priority",
  "matched_keywords": ["system analyst", "python", "remote"],
  "reasons": [
    "+10: Keyword 'system analyst' in title",
    "+10: Keyword 'python' in description",
    "+15: Remote work available"
  ]
}
```

### DIGEST.md

Daily summary of candidates in markdown format. Generated automatically after each scan.

Contains:

- Summary statistics (total jobs, breakdown by category)
- High priority jobs listed first
- Review category jobs
- Low priority jobs (if any)
- Links to full JSON files

### state.json

Tracks all seen jobs and monitoring statistics. **Do not edit manually.**

Managed by `StateManager` class. Contains:

- Last scan timestamp
- Total counters (jobs seen, candidates, applications)
- Status lists (new jobs, candidates, applied)
- Complete job history with metadata
- Per-source statistics

### cookies.json

Authentication cookies for job portal scraping. Required for accessing job listings.

**Format**: JSON array of cookie objects:

```json
[
  {
    "name": "session_id",
    "value": "abc123...",
    "domain": ".duunitori.fi",
    "path": "/",
    "secure": true
  }
]
```

**How to obtain**:

1. Log into job portal in browser
2. Use browser extension (e.g., "Get cookies.txt") to export cookies
3. Save to this file
4. Update every 30 days or when scraping stops working

## Usage

### View Today's Candidates

```bash
# High priority
ls candidates/$(date +%Y-%m-%d)/high_priority/

# Read digest
cat candidates/$(date +%Y-%m-%d)/DIGEST.md
```

### Review a Specific Job

```bash
# View JSON details
cat candidates/2025-12-01/high_priority/abc123def456.json

# Or use jq for pretty print
jq . candidates/2025-12-01/high_priority/abc123def456.json
```

### Check State

```bash
# Pretty print state
jq . state.json

# Count total jobs seen
jq '.total_jobs_seen' state.json

# List candidates
jq '.candidates[]' state.json
```

## Maintenance

### Regular Cleanup

Run cleanup command weekly to archive old jobs:

```bash
python scripts/job_monitor.py cleanup --days 60
```

This removes jobs older than 60 days from state tracking.

### Backup State

State file contains valuable history. Back it up regularly:

```bash
cp state.json state.json.backup.$(date +%Y%m%d)
```

State manager automatically creates `state.json.backup` before each save.

### Update Cookies

When job scraping stops working:

1. Re-authenticate in browser
2. Export fresh cookies
3. Replace `cookies.json`
4. Test with: `python scripts/job_monitor.py scan --dry-run`

## Troubleshooting

### Missing Candidates Directory

If `candidates/` doesn't exist, it will be created automatically on first scan.

### Corrupted State File

If `state.json` is corrupted:

1. Check for `state.json.backup`
2. Restore: `mv state.json.backup state.json`
3. Or delete to start fresh: `rm state.json`

### Old Cookie Files

Cookies expire. Update them monthly or when you see errors like:

- "No jobs found" (when there should be jobs)
- HTTP 401/403 errors
- "Authentication required" messages

## See Also

- [Job Monitoring Workflows](../docs/job_monitoring_workflows.md) - Usage examples
- [Architecture](../docs/job_monitoring_architecture.md) - System design
- [Execution Plan](../docs/job_monitoring_execution_plan.md) - Implementation details
