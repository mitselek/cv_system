# CV System

Comprehensive career management system for professional development and job search.

## Project Structure

This repository contains multiple tools and systems for career management:

### 📊 [Job Monitoring System](job-monitoring/) ⭐ v1.0.0

Automated job discovery and tracking system.

**Features:**

- 🔍 Automated scanning of job portals (Duunitori, LinkedIn, etc.)
- 🎯 Intelligent scoring and ranking
- 📊 State tracking and statistics
- 📝 Application workflow management
- 🤖 CLI for all operations

**Quick Start:**

```bash
cd job-monitoring
pip install -e .
job-monitor scan --config config.yaml
```

[Full Documentation →](job-monitoring/README.md)

---

### 📧 [Email Monitor](email-monitor/)

IMAP-based email monitoring for job alerts (Go).

---

### 🏛️ [Riigihanked](riigihanked/)

Estonian public procurement monitoring (Go + Python).

---

### 📁 [Knowledge Base](knowledge_base/)

Personal professional portfolio and achievements documentation.

---

### 📄 [Applications](applications/)

Registry of submitted job applications with tracking.

---

### 🛠️ [Utilities](utils/)

General-purpose helper scripts for various tasks.

---

## Installation

### Job Monitoring System (Recommended)

```bash
cd job-monitoring
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
job-monitor scan --config config.yaml
```

## Quick Reference

```bash
# Scan for new jobs
job-monitor scan --config config.yaml

# Review candidates
job-monitor review --config config.yaml --category review

# View statistics
job-monitor stats --config config.yaml
```

## Project Status

| Component      | Status         | Version | Tests   |
| -------------- | -------------- | ------- | ------- |
| Job Monitoring | ✅ Production  | v1.0.0  | 100/100 |
| Email Monitor  | 🚧 Development | -       | -       |
| Riigihanked    | 🚧 Development | -       | -       |
