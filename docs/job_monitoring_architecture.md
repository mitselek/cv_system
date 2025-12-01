# Job Portal Integration Architecture

## Overview

Integrate automated job monitoring into the cv_system workflow with tracking, deduplication, and opportunity scoring.

## Directory Structure

```text
cv_system/
├── job_sources/              # Job portal monitoring
│   ├── candidates/          # Scored jobs by date
│   │   └── YYYY-MM-DD/     # Daily directories
│   │       ├── high_priority/   # Score ≥70
│   │       ├── review/          # Score 40-70
│   │       ├── low_priority/    # Score <40
│   │       └── DIGEST.md        # Daily summary
│   ├── state.json          # Monitoring state (last scan, seen jobs)
│   └── cookies.json        # Authentication cookies
│
├── scripts/
│   ├── schemas.py           # Pydantic models (JobPosting, ScoredJob, etc.)
│   ├── config_manager.py    # Configuration loading & validation
│   ├── job_scraper.py       # Portal scrapers (duunitori, linkedin, etc.)
│   ├── job_scorer.py        # Scoring algorithm
│   ├── deduplicator.py      # Duplicate detection
│   ├── state_manager.py     # State persistence
│   ├── digest_generator.py  # Markdown digest generation
│   ├── job_monitor.py       # CLI orchestrator
│   └── job_to_application.py # Candidate → application converter
│
├── applications/            # Application tracking
│   ├── Company_Name/
│   │   └── Position_Title/
│   │       ├── README.md
│   │       └── job_posting.md
│   └── REGISTRY.md
│
└── config.example.yaml      # Configuration template
```

## Core Components

### 1. Source Configuration (`config.example.yaml`)

```yaml
sources:
  - name: duunitori.fi
    enabled: true
    queries:
      - keywords: system analyst
        location: Helsinki
        limit: 20
      - keywords: projektijuht
        location: Tallinn
        limit: 20
    cookies_file: job_sources/cookies.json

  - name: linkedin.com
    enabled: false
    queries:
      - keywords: System Analyst Finland
        limit: 25

scoring:
  positive_keywords:
    - system analyst
    - projektijuht
    - project manager
    - software architect
    - technical lead
  
  negative_keywords:
    - junior
    - internship
  
  required_keywords: []
  
  preferred_companies:
    - Playtech
    - Wise
    - Bolt
  
  blocked_companies: []
  
  preferred_locations:
    - Helsinki
    - Tallinn
    - remote
  
  remote_bonus: 15
  days_threshold_fresh: 7
  days_threshold_old: 30

state_file: job_sources/state.json
candidates_dir: job_sources/candidates
scan_interval_hours: 24
auto_archive_days: 60
```
```

### 2. State Tracking (`job_sources/state.json`)

```json
{
  "last_scan": "2025-12-01T08:00:00+00:00",
  "total_jobs_seen": 1247,
  "total_candidates": 23,
  "total_applications": 5,
  "new_jobs": [],
  "candidates": ["job_id_1", "job_id_2"],
  "applied": ["job_id_3", "job_id_4"],
  "seen_jobs": {
    "abc123def456": {
      "id": "abc123def456",
      "title": "Senior System Analyst",
      "company": "Tech Corp",
      "location": "Helsinki",
      "url": "https://duunitori.fi/tyopaikat/...",
      "source": "duunitori.fi",
      "discovered_date": "2025-11-28T10:00:00+00:00",
      "status": "candidate",
      "description": "We are looking for..."
    }
  },
  "stats_by_source": {
    "duunitori.fi": 1247
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
