# Job Portal Integration Architecture

## Overview

Integrate automated job monitoring into the cv_system workflow with tracking, deduplication, and opportunity scoring.

## Directory Structure

```text
cv_system/
├── job_sources/              # NEW: Job portal monitoring
│   ├── config.json          # Source configurations
│   ├── state.json           # Tracking state (last scan, seen IDs)
│   ├── cache/               # Cached job listings
│   │   ├── duunitori/
│   │   ├── linkedin/
│   │   └── tyomarkkinatori/
│   ├── candidates/          # Promising jobs for review
│   │   └── YYYY-MM-DD/
│   └── archived/            # Rejected/outdated listings
│
├── scripts/
│   ├── job_scraper.py       # EXISTING: Portal scrapers
│   ├── job_monitor.py       # NEW: Orchestration & scheduling
│   ├── job_scorer.py        # NEW: Fit scoring algorithm
│   └── job_to_application.py # NEW: Convert candidate → application
│
└── applications/            # EXISTING: Application tracking
```

## Core Components

### 1. Source Configuration (`job_sources/config.json`)

```json
{
  "sources": [
    {
      "name": "duunitori",
      "enabled": true,
      "queries": [
        {
          "keywords": "system analyst",
          "location": "Helsinki",
          "priority": "high"
        },
        { "keywords": "IT projektijuht", "location": "", "priority": "high" },
        {
          "keywords": "software architect",
          "location": "Helsinki",
          "priority": "medium"
        },
        {
          "keywords": "project manager IT",
          "location": "",
          "priority": "medium"
        }
      ],
      "schedule": "daily",
      "max_results_per_query": 30,
      "cookie_file": "~/.config/job_scraper_cookies_duunitori.json"
    },
    {
      "name": "linkedin",
      "enabled": false,
      "queries": [
        { "keywords": "System Analyst Finland", "priority": "high" },
        { "keywords": "IT Project Manager Estonia", "priority": "high" }
      ],
      "schedule": "daily",
      "cookie_file": "~/.config/job_scraper_cookies_linkedin.json"
    }
  ],
  "scoring": {
    "keywords_match": {
      "system analyst": 10,
      "projektijuht": 10,
      "project manager": 8,
      "software": 7,
      "IT": 5,
      "architect": 6,
      "technical lead": 7
    },
    "companies_preferred": {
      "Playtech": 5,
      "Wise": 5,
      "Bolt": 5,
      "Pipedrive": 5
    },
    "locations_preferred": {
      "Helsinki": 3,
      "Tallinn": 5,
      "Espoo": 3,
      "remote": 2
    },
    "threshold_review": 15,
    "threshold_auto_apply": 25
  }
}
```

### 2. State Tracking (`job_sources/state.json`)

```json
{
  "last_scan": "2025-12-01T08:00:00Z",
  "sources": {
    "duunitori": {
      "last_successful_scan": "2025-12-01T08:00:00Z",
      "total_jobs_seen": 1247,
      "jobs_reviewed": 23,
      "jobs_applied": 5
    }
  },
  "seen_jobs": {
    "duunitori-19754571": {
      "first_seen": "2025-11-28T10:00:00Z",
      "last_seen": "2025-12-01T08:00:00Z",
      "url": "https://duunitori.fi/tyopaikat/...",
      "title": "Project Manager (Software)",
      "company": "Kultakiertue Oy",
      "status": "reviewed",
      "score": 18,
      "notes": "Not a good fit - too junior"
    }
  }
}
```

### 3. Job Monitor Script (`job_monitor.py`)

**Responsibilities:**

- Orchestrate scraping across all enabled sources
- Deduplicate jobs (by URL, title+company)
- Score each job against your profile
- Move high-scoring jobs to candidates/
- Update state tracking
- Generate daily digest

**Key Features:**

```python
class JobMonitor:
    def scan_sources()           # Run all configured queries
    def deduplicate(jobs)        # Remove duplicates & already-seen
    def score_job(job)           # Calculate fit score
    def categorize(job, score)   # candidates/ or archived/
    def generate_digest()        # Daily summary email/report
```

### 4. Job Scorer (`job_scorer.py`)

**Scoring Algorithm:**

```python
def score_job(job: Dict, config: Dict, profile: Dict) -> int:
    score = 0

    # Keywords in title/description
    for keyword, points in config['keywords_match'].items():
        if keyword.lower() in job['title'].lower():
            score += points

    # Preferred companies
    if job['company'] in config['companies_preferred']:
        score += config['companies_preferred'][job['company']]

    # Location preference
    for loc, points in config['locations_preferred'].items():
        if loc.lower() in job['location'].lower():
            score += points

    # Recency (newer = better)
    days_old = calculate_days_since_posted(job)
    if days_old <= 7:
        score += 5
    elif days_old <= 14:
        score += 2

    # Salary mentioned (positive signal)
    if 'salary' in job or '€' in job.get('description', ''):
        score += 3

    return score
```

### 5. Workflow Integration

#### Daily Automated Workflow

```bash
# Cron job: 0 8 * * * (daily at 8am)
./scripts/job_monitor.py scan --mode daily
```

**Process:**

1. Read `config.json` for enabled sources & queries
2. Scrape each source (respecting rate limits)
3. For each job:
   - Check if already seen (by URL hash)
   - If new: Score against profile
   - If score ≥ threshold_review: → `candidates/YYYY-MM-DD/`
   - If score < threshold: → `archived/`
   - Update `state.json`
4. Generate digest: `candidates/YYYY-MM-DD/DIGEST.md`

#### Manual Review Workflow

```bash
# Review today's candidates
ls job_sources/candidates/$(date +%Y-%m-%d)/

# View digest
cat job_sources/candidates/$(date +%Y-%m-%d)/DIGEST.md

# Promote candidate to application
./scripts/job_to_application.py \
  job_sources/candidates/2025-12-01/job_12345.json \
  --company "Wärtsilä" \
  --position "Senior System Analyst"
```

**Promotion creates:**

- `applications/Wartsila/Senior_System_Analyst/`
- Copies job posting → `job_posting.md`
- Creates `README.md` with metadata
- Updates `applications/REGISTRY.md`
- Prompts for application generation

## Commands Reference

### Setup

```bash
# Initialize job monitoring
./scripts/job_monitor.py init

# Configure sources
vi job_sources/config.json

# Test scraping (dry run)
./scripts/job_monitor.py scan --dry-run
```

### Daily Operations

```bash
# Manual scan (respects last_scan timestamp)
./scripts/job_monitor.py scan

# Force full re-scan
./scripts/job_monitor.py scan --force

# Review candidates
./scripts/job_monitor.py review --date today

# Show statistics
./scripts/job_monitor.py stats --days 7
```

### Job Management

```bash
# Score a specific job
./scripts/job_scorer.py score --url "https://..."

# Mark job as reviewed
./scripts/job_monitor.py mark <job_id> --status reviewed --notes "Not interested"

# Promote to application
./scripts/job_to_application.py <job_id> --auto-generate
```

## Advanced Features (Future)

### Phase 2: Smart Filtering

- **Duplicate detection across portals** (same job on multiple sites)
- **Company blacklist** (avoid certain employers)
- **Auto-archive old jobs** (>30 days)
- **Track application success rate** by source

### Phase 3: AI Enhancement

- **NLP-based job description analysis** (extract requirements)
- **Automated fit percentage** calculation
- **Similar job recommendations**
- **Salary prediction** based on title/location

### Phase 4: Automation

- **Auto-generate applications** for score ≥ threshold_auto_apply
- **Auto-submit** to portals with API (careful!)
- **Email alerts** for high-priority matches
- **Telegram/Slack notifications**

## Migration Plan

### Step 1: Core Infrastructure (Week 1)

- [ ] Create `job_sources/` structure
- [ ] Implement `job_monitor.py` basic scanning
- [ ] Implement deduplication by URL
- [ ] State tracking in `state.json`

### Step 2: Scoring System (Week 1)

- [ ] Implement `job_scorer.py`
- [ ] Define scoring rules in `config.json`
- [ ] Test scoring against known good/bad jobs
- [ ] Tune thresholds

### Step 3: Integration (Week 2)

- [ ] Daily cron job setup
- [ ] Digest generation
- [ ] `job_to_application.py` converter
- [ ] Update documentation

### Step 4: Expansion (Ongoing)

- [ ] Add LinkedIn scraper (when cookies provided)
- [ ] Add Tyomarkkinatori scraper
- [ ] Add more search queries
- [ ] Refine scoring based on outcomes

## Benefits

### Automation

- **Zero manual searching** - jobs come to you
- **Daily digest** of promising opportunities
- **No missed opportunities** - continuous monitoring

### Intelligence

- **Scored by fit** - focus on best matches first
- **Deduplication** - see each job once
- **Historical tracking** - learn what works

### Scale

- **Multiple sources** simultaneously
- **Multiple queries** per source
- **Handles 100s of jobs/day** efficiently

### Integration

- **Seamless with existing workflow**
- **One command** to promote candidate → application
- **Uses existing templates** and processes

## Privacy & Ethics

- **Rate limiting** - respect portal ToS
- **Cookie-based auth** - no password storage
- **Local storage only** - no external services
- **No auto-submission** without explicit approval
- **Transparent scoring** - you control criteria
