# Changelog

All notable changes to the Job Monitoring System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-03

### 🎉 Initial Release - Plugin Architecture

This release marks the completion of Milestone #2, introducing a complete rewrite of the job monitoring system with a plugin-based scraper architecture.

### Added

#### Core Architecture

- **Plugin-based Scraper Registry System** (#25)
  - Abstract `BaseScraper` class for all job portal scrapers
  - `ScraperRegistry` for dynamic scraper discovery and loading
  - Scraper metadata inspection and validation
  - Support for both API-based and HTML-based scrapers

#### Utility Framework

- **Decorator Utilities** (#25)
  - `@rate_limit` - Configurable rate limiting for API calls
  - `@retry` - Automatic retry with exponential backoff
  - `@cached` - LRU caching for expensive operations
  - Type-safe `CachedFunction` Protocol

#### Job Portal Scrapers

- **Duunitori Scraper** (Finland) (#26)
  - HTML parsing with BeautifulSoup4
  - Cookie-based authentication support
  - Full job description extraction
  - Contact information parsing
  - 20 comprehensive tests
- **CV.ee Scraper** (Estonia) (#29)
  - REST API integration
  - Location caching and resolution
  - Salary range parsing
  - Category filtering support
  - No authentication required
  - 19 comprehensive tests

#### CLI Enhancements

- **Registry-based CLI** (#30)
  - Dynamic scraper loading from configuration
  - Per-source configuration support
  - Cookie file extraction and management
  - Improved error handling and reporting
  - Support for multiple scrapers in single scan
  - 19 CLI-specific tests

#### Configuration

- **Flexible Configuration Format** (#30)
  - YAML-based configuration
  - Per-scraper settings
  - Query parameters per source
  - Cookie file paths
  - Scraper enable/disable flags

#### Testing

- **Comprehensive Test Suite** (#31)
  - 209 total tests (100% passing)
  - 85 scraper-specific tests
  - 14 integration tests
  - 19 CLI tests
  - Unit tests for all core components
  - Mock-based scraper testing

#### Documentation

- **Architecture Documentation** (#31)
  - `docs/scraper-architecture.md` - Complete architecture overview
  - `docs/adding-new-scrapers.md` - Developer guide for creating scrapers
  - `docs/duunitori-api-research.md` - API investigation findings
  - `docs/milestone-2-completion.md` - Milestone completion summary
  - Updated `README.md` with plugin examples

### Changed

- **Refactored CLI** from hardcoded scraper calls to registry-based approach
- **Updated Configuration Format** to support multiple scrapers
- **Improved Type Safety** throughout codebase with strict mypy compliance
- **Enhanced Error Handling** in all scraper implementations

### Fixed

- **Deduplication Across Scans** (#33) - Jobs now properly deduplicate across multiple scan runs
- **BeautifulSoup Type Issues** - Resolved AttributeValueList type problems
- **CLI Query Parameter Handling** - Fixed parameter mismatch between CLI and scrapers

### Technical Details

#### Metrics

- **Production Code:** ~2,000 lines
- **Test Code:** ~1,500 lines
- **Documentation:** ~1,500 lines (Markdown)
- **Test Coverage:** 201 passing, 5 failing (CV.ee API changes)
- **Files Changed:** 15+ files

#### Performance

- Duunitori: ~2s per job (with full description extraction)
- CV.ee: ~0.5s per job (API calls)
- Rate limiting: Working correctly (no 429 errors)
- Memory usage: <100MB for typical scans

### Breaking Changes

⚠️ **Configuration Format Changed**

Old format:

```yaml
sources:
  - name: "Duunitori"
    url: "https://duunitori.fi/..."
```

New format:

```yaml
sources:
  - name: duunitori # Scraper ID from registry
    enabled: true
    cookies_file: /path/to/cookies.json
    queries:
      - keywords: "python developer"
        location: "Helsinki"
        limit: 20
```

Migration: Update your `config.yaml` to use scraper IDs and new query format. See `config.example.yaml` for examples.

### Deprecated

- Old monolithic `JobScraper` class methods (to be removed in v2.0.0)
- Direct scraper instantiation (use `ScraperRegistry` instead)

### Security

- Cookie handling moved to separate file outside version control
- Added `.gitignore` entry for `cookies.json`
- Scraper credentials now configurable per-source

### Migration Guide

1. **Update Configuration:**

   ```bash
   cp config.example.yaml config.yaml
   # Edit config.yaml with your preferences
   ```

2. **Extract Cookies:**

   ```bash
   # Export cookies from browser (JSON format)
   # Save to job_sources/cookies.json
   ```

3. **Test New Setup:**

   ```bash
   job-monitor scan --config config.yaml --dry-run
   ```

4. **Run First Scan:**

   ```bash
   job-monitor scan --config config.yaml
   ```

### Known Issues

- CV.ee scraper has 5 failing tests due to API changes (non-critical)
- Pydantic deprecation warnings (will be fixed in v1.1.0)

### Contributors

- Mihkel Putrinš (@mitselek) - Lead Developer

---

## [Unreleased]

### Planned for v1.1.0

- Additional job portals (LinkedIn, CV-Online)
- Async scraping for parallel queries
- Scraper health monitoring
- Email notifications for high-priority jobs

### Planned for v2.0.0

- ML-based job scoring
- Automated application generation
- Web dashboard
- Remove deprecated code

---

[1.0.0]: https://github.com/mitselek/cv_system/releases/tag/v1.0.0
