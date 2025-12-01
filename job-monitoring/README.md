# Job Monitoring System

Automated job monitoring and application tracking system for managing job search workflows.

## Overview

This system provides automated monitoring of job portals, intelligent scoring of opportunities, and streamlined application management.

**Key Features:**

- 🔍 **Automated Job Monitoring** - Continuous scanning of multiple job portals
- 🎯 **Intelligent Scoring** - Keyword-based ranking of job matches
- 📊 **State Tracking** - Historical view of all discovered opportunities
- 📝 **Application Management** - Organized tracking of applications
- 🤖 **CLI Tools** - Command-line interface for all operations

## Quick Start

### Installation

```bash
# Navigate to job-monitoring directory
cd job-monitoring

# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Initial Setup

1. **Create configuration file:**

   ```bash
   job-monitor init
   ```

2. **Customize configuration:**

   Edit `config.yaml` to add your preferences:

   - Job search keywords
   - Preferred companies and locations
   - Scoring weights
   - Enabled job portals

3. **Add authentication cookies:**

   Export cookies from job portals and save to `job_sources/cookies.json`.

4. **Test the setup:**

   ```bash
   python scripts/job_monitor.py scan --dry-run
   ```

## Usage

### Daily Job Monitoring

```bash
# Run quick scan (titles and metadata only, fast)
job-monitor scan --config config.yaml

# Run detailed scan (extracts full job descriptions, slower but better scoring)
job-monitor scan --config config.yaml --full-details

# Review today's candidates
job-monitor review --category high

# Check statistics
job-monitor stats
```

**Note on `--full-details` flag:**

- Extracts full job descriptions from portal pages
- Enables better keyword matching and higher scores (70-90 points vs 50-60)
- Takes ~1.5 seconds per job (respectful rate limiting)
- Typical scan: ~50-100 jobs = 1-3 minutes total
- Recommended for weekly comprehensive scans
- Quick scans (without flag) are faster for daily monitoring

### Managing Jobs

```bash
# Mark job as candidate
job-monitor mark <job_id> candidate

# Mark as applied after submission
job-monitor mark <job_id> applied

# Mark as rejected
job-monitor mark <job_id> rejected
```

### Command Line Options

#### Scan Command

```bash
job-monitor scan [OPTIONS]

Options:
  --config PATH        Configuration file (default: config.example.yaml)
  --dry-run           Run without saving state or candidates
  --force             Force rescan of all sources
  --full-details      Extract full job descriptions (slower, ~1.5s per job)
  --help              Show help message
```

**Performance Notes:**

- **Quick scan** (default): 50-100 jobs in ~10-20 seconds
- **Full details scan**: 50-100 jobs in ~75-150 seconds (1.5s per job)
- Rate limiting: 1.5 second delay between description fetches
- Respectful to job portals: prevents rate limiting or blocking

#### Review Command

```bash
job-monitor review [OPTIONS]

Options:
  --config PATH       Configuration file
  --category TEXT     Filter by: high, review, low, all (default: all)
  --min-score FLOAT   Minimum score threshold
  --source TEXT       Filter by source
  --date TEXT         Filter by date (YYYY-MM-DD)
  --help              Show help message
```

### Cleanup

```bash
# Archive old jobs (>60 days)
python scripts/job_monitor.py cleanup --days 60
```

## Scoring System

Jobs are scored based on multiple criteria:

- **Keyword Matches** (+10 points each): Technical skills, methodologies, domain terms
- **Preferred Company** (+15 points): Companies you've specified in config
- **Preferred Location** (+10 points): Your target locations
- **Remote Work** (+5 points): Remote or hybrid positions
- **Freshness** (+10 points if <7 days, -10 if >30 days)

**Scoring Categories:**

- **High Priority** (70+ points): Excellent matches - apply immediately
- **Review** (40-69 points): Good matches - review carefully
- **Low Priority** (<40 points): Weak matches - archive

**Impact of Description Extraction:**

Without `--full-details`:

- Keyword matches limited to title + company + location
- Typical score: 30-60 points
- Rarely reaches "High Priority"

With `--full-details`:

- Keyword matches include full job description
- Typical score: 50-90 points
- 5-10 jobs reach "High Priority" per scan
- Much better automatic prioritization

**Recommendation:** Use `--full-details` for weekly comprehensive scans, quick scans for daily monitoring.

```text
cv_system/
├── scripts/                # Core monitoring and scoring logic
│   ├── job_monitor.py     # Main CLI orchestrator
│   ├── job_scorer.py      # Scoring algorithm
│   ├── job_scraper.py     # Portal scrapers
│   ├── config_manager.py  # Configuration handling
│   ├── state_manager.py   # State persistence
│   └── ...
│
├── job_sources/           # Monitored jobs and state
│   ├── candidates/        # Daily candidate directories
│   ├── state.json        # Monitoring history
│   └── cookies.json      # Authentication cookies
│
├── applications/          # Application tracking
│   └── Company_Name/
│       └── Position_Title/
│
├── knowledge_base/        # Your profile and experience
│   ├── achievements/
│   ├── experiences/
│   ├── skills/
│   └── ...
│
└── docs/                  # Documentation
    ├── job_monitoring_architecture.md
    ├── job_monitoring_workflows.md
    └── ...
```

## CLI Commands

| Command                  | Description                          |
| ------------------------ | ------------------------------------ |
| `scan`                   | Scan job portals and save candidates |
| `scan --dry-run`         | Test scan without saving             |
| `scan --force`           | Force full rescan                    |
| `review`                 | Display candidates with filters      |
| `review --category high` | Show high-priority jobs only         |
| `review --min-score 70`  | Filter by minimum score              |
| `stats`                  | Show monitoring statistics           |
| `mark <id> <status>`     | Update job status                    |
| `cleanup --days N`       | Archive jobs older than N days       |
| `init`                   | Create configuration template        |

## Scoring System

Jobs are automatically scored based on:

- **Keywords** in title and description (+10 points each)
- **Company** match with preferred list (+5 points)
- **Location** match with preferences (+5 points)
- **Remote work** available (+15 points)
- **Recency** - newer jobs score higher (+5 for <7 days)
- **Negative keywords** reduce score (-5 points each)

**Categories:**

- **High Priority** (≥70): Excellent matches, review immediately
- **Review** (40-69): Worth considering
- **Low Priority** (<40): Poor matches

## Development

### Running Tests

```bash
# All tests
pytest scripts/

# With coverage
pytest scripts/ --cov=scripts --cov-report=html

# Specific test file
pytest scripts/test_job_scorer.py -v
```

### Type Checking

```bash
# Strict type checking
mypy scripts/ --strict
```

### Linting

```bash
# Check code style
ruff check scripts/
```

## Documentation

- **[Workflows Guide](docs/job_monitoring_workflows.md)** - Common usage patterns
- **[Architecture](docs/job_monitoring_architecture.md)** - System design
- **[Job Sources](job_sources/README.md)** - Directory structure
- **[Implementation Plan](docs/job_monitoring_implementation_plan.md)** - Technical specs
- **[Execution Plan](docs/job_monitoring_execution_plan.md)** - Development timeline

## Testing

**Test Coverage:** 90 tests, >80% coverage on critical modules

```text
Critical Modules:
- schemas.py: 100%
- deduplicator.py: 100%
- job_to_application.py: 97%
- digest_generator.py: 95%
- state_manager.py: 93%
- job_scorer.py: 89%
```

## Project Status

**Current Version:** 1.0.0

**Completed:**

- ✅ Phase 1: Type System & Foundation
- ✅ Phase 2: Core Logic & State Management
- ✅ Phase 3: User Interface & Integration
- ✅ Phase 4: Testing & Documentation

**Roadmap:**

- v1.1: Additional job portals (LinkedIn, CV-Online)
- v1.2: Email notifications for high-priority jobs
- v2.0: ML-based job scoring
- v2.0: Automated application generation

## License

MIT License - see LICENSE file for details

## Author

Mihkel Rego - [GitHub](https://github.com/mitselek)

## Contributing

This is a personal project, but suggestions and improvements are welcome via GitHub issues.
