# CV System

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
# Clone repository
git clone https://github.com/mitselek/cv_system.git
cd cv_system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# or
pip install -e .
```

### Initial Setup

1. **Create configuration file:**

```bash
python scripts/job_monitor.py init
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
# Run daily scan
python scripts/job_monitor.py scan

# Review today's candidates
python scripts/job_monitor.py review --category high

# Check statistics
python scripts/job_monitor.py stats
```

### Managing Jobs

```bash
# Mark job as candidate
python scripts/job_monitor.py mark <job_id> candidate

# Mark as applied after submission  
python scripts/job_monitor.py mark <job_id> applied

# Mark as rejected
python scripts/job_monitor.py mark <job_id> rejected
```

### Cleanup

```bash
# Archive old jobs (>60 days)
python scripts/job_monitor.py cleanup --days 60
```

## Directory Structure

```
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

| Command | Description |
|---------|-------------|
| `scan` | Scan job portals and save candidates |
| `scan --dry-run` | Test scan without saving |
| `scan --force` | Force full rescan |
| `review` | Display candidates with filters |
| `review --category high` | Show high-priority jobs only |
| `review --min-score 70` | Filter by minimum score |
| `stats` | Show monitoring statistics |
| `mark <id> <status>` | Update job status |
| `cleanup --days N` | Archive jobs older than N days |
| `init` | Create configuration template |

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

```
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
