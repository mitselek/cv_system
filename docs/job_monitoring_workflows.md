# Job Monitoring Workflows

## Overview

This document provides practical examples of common job monitoring workflows using the `job_monitor.py` CLI.

## Initial Setup

### 1. Create Configuration File

```bash
cd ~/Documents/github/cv_system
python scripts/job_monitor.py init --output config.yaml
```

This creates a configuration template. Edit it to customize:

```bash
vi config.yaml
```

Key settings to configure:
- **sources**: Enable/disable job portals, add search queries
- **scoring.positive_keywords**: Keywords that increase job score
- **scoring.negative_keywords**: Keywords that decrease score  
- **scoring.preferred_locations**: Add your preferred work locations
- **scoring.remote_bonus**: Points added for remote positions

### 2. Verify Configuration

```bash
python scripts/job_monitor.py scan --config config.yaml --dry-run
```

This performs a dry-run scan without saving state or candidates.

## Daily Workflows

### Morning Routine: Review New Candidates

**Step 1: Run daily scan**

```bash
python scripts/job_monitor.py scan
```

This will:
- Scrape all enabled job sources
- Score and categorize new jobs
- Save candidates to `job_sources/candidates/YYYY-MM-DD/`
- Generate a digest at `job_sources/candidates/YYYY-MM-DD/DIGEST.md`

**Step 2: Read the digest**

```bash
cat job_sources/candidates/$(date +%Y-%m-%d)/DIGEST.md
```

Or use the review command with filters:

```bash
# Review all candidates
python scripts/job_monitor.py review

# Only high priority
python scripts/job_monitor.py review --category high

# Filter by score
python scripts/job_monitor.py review --min-score 70

# Filter by source
python scripts/job_monitor.py review --source duunitori.fi
```

**Step 3: Mark interesting jobs**

```bash
# Mark a job as candidate for later review
python scripts/job_monitor.py mark <job_id> candidate

# Mark as applied after submitting application
python scripts/job_monitor.py mark <job_id> applied

# Mark as rejected if not interested
python scripts/job_monitor.py mark <job_id> rejected
```

### Weekly Routine: Statistics and Cleanup

**Check monitoring statistics**

```bash
python scripts/job_monitor.py stats
```

This shows:
- Last scan time
- Total jobs seen/candidates/applications
- Status breakdown (new, candidates, applied)
- Stats by source

**Archive old jobs**

```bash
# Preview what would be archived (>60 days old)
python scripts/job_monitor.py cleanup --days 60 --dry-run

# Actually archive them
python scripts/job_monitor.py cleanup --days 60
```

## Application Workflow

### Converting Candidate to Application

When you find a promising candidate and want to prepare an application:

**Option 1: Using ApplicationConverter directly**

```python
from pathlib import Path
from job_to_application import ApplicationConverter
import json

# Load the candidate JSON
candidate_path = Path("job_sources/candidates/2025-12-01/high_priority/abc123.json")
with open(candidate_path) as f:
    data = json.load(f)
    
from schemas import ScoredJob
sj = ScoredJob(**data)

# Convert to application structure
converter = ApplicationConverter(applications_dir=Path("applications"))
app_path = converter.convert(sj, notes="Looks like a perfect fit!")

print(f"Application created at: {app_path}")
```

**Option 2: Manual process**

1. Review the candidate file:
   ```bash
   cat job_sources/candidates/2025-12-01/high_priority/abc123.json
   ```

2. Create application directory:
   ```bash
   mkdir -p applications/Company_Name/Position_Title
   ```

3. Use existing application templates to craft your application

## Advanced Workflows

### Force Re-scan All Sources

```bash
# Force rescan ignoring last scan time
python scripts/job_monitor.py scan --force
```

### Review Historical Candidates

```bash
# Review candidates from specific date
python scripts/job_monitor.py review --date 2025-11-28

# Review with multiple filters
python scripts/job_monitor.py review --date 2025-11-28 --category high --min-score 75
```

### Batch Operations

```bash
# Archive all candidates from November
for dir in job_sources/candidates/2025-11-*; do
  echo "Archiving $dir"
  # Process each day's candidates
done
```

## Troubleshooting

### No Jobs Found

**Problem**: Scan runs but finds 0 jobs

**Solutions**:
1. Check if sources are enabled in config
2. Verify cookies are valid (may need to re-authenticate)
3. Try `--dry-run` to see error messages
4. Check internet connectivity

### Low Scoring Jobs

**Problem**: All jobs score too low

**Solutions**:
1. Review `scoring.positive_keywords` - add more relevant terms
2. Lower score thresholds in configuration
3. Add more preferred companies/locations
4. Check if `negative_keywords` are too restrictive

### Duplicate Jobs

**Problem**: Same job appears multiple times

**Solutions**:
1. Deduplicator uses URL and title+company fingerprint
2. Check if job URL is different (same job, different links)
3. This is working as intended - different URLs = different postings

### State File Corruption

**Problem**: `state.json` appears corrupted

**Solutions**:
1. Check for backup: `state.json.backup`
2. Restore from backup if needed
3. Delete `state.json` to start fresh (loses history)

## Cookie Maintenance

### When to Update Cookies

Job scraping requires authentication cookies. Update when:
- Jobs aren't being found
- You see authentication errors
- It's been >30 days since last update

### How to Update

1. Use browser extension to export cookies
2. Save to `job_sources/cookies.json`
3. Format should be:
   ```json
   [
     {
       "name": "cookie_name",
       "value": "cookie_value",
       "domain": ".duunitori.fi"
     }
   ]
   ```

## Best Practices

### Daily Habits

1. **Morning scan**: Run `scan` command once per day
2. **Review digest**: Check high-priority candidates first
3. **Quick triage**: Mark jobs immediately (candidate/rejected)
4. **Weekly cleanup**: Archive old jobs every Friday

### Configuration Tuning

1. **Start broad**: Begin with general keywords
2. **Refine gradually**: Add negative keywords based on results
3. **Track success**: Note which sources/keywords lead to applications
4. **Adjust scores**: Tune thresholds based on actual job quality

### State Management

1. **Never edit state.json manually**: Use CLI commands
2. **Backup regularly**: State file contains valuable history
3. **Clean up periodically**: Archive old jobs to keep state small

## Example Daily Script

Create `~/bin/daily-job-scan.sh`:

```bash
#!/bin/bash
# Daily job monitoring routine

cd ~/Documents/github/cv_system

# Run scan
echo "=== Running job scan ==="
python scripts/job_monitor.py scan

# Show today's candidates
echo ""
echo "=== Today's High Priority Candidates ==="
python scripts/job_monitor.py review --category high --date $(date +%Y-%m-%d)

# Show stats
echo ""
echo "=== Statistics ==="
python scripts/job_monitor.py stats
```

Make it executable and run daily:

```bash
chmod +x ~/bin/daily-job-scan.sh
# Add to crontab: 0 8 * * * ~/bin/daily-job-scan.sh
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `scan` | Scrape job sources and save candidates |
| `scan --dry-run` | Test configuration without saving |
| `scan --force` | Force full rescan ignoring timestamps |
| `review` | Display candidates with filters |
| `review --category high` | Show only high-priority jobs |
| `review --min-score 70` | Filter by minimum score |
| `stats` | Show monitoring statistics |
| `mark <id> candidate` | Mark job for later review |
| `mark <id> applied` | Mark job as applied |
| `mark <id> rejected` | Mark job as rejected |
| `cleanup --days 60` | Archive jobs older than 60 days |
| `init` | Create configuration template |

## See Also

- [Architecture Documentation](job_monitoring_architecture.md)
- [Implementation Plan](job_monitoring_implementation_plan.md)
- [Execution Plan](job_monitoring_execution_plan.md)
