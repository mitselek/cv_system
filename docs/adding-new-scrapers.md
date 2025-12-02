# Adding New Scrapers to the Job Monitoring System

**Date:** December 2, 2025  
**Version:** 1.0  
**Audience:** Developers extending the scraper registry

## Overview

The job monitoring system uses a plugin architecture that makes adding new job portal scrapers straightforward. This guide walks you through creating a new scraper from scratch.

## Prerequisites

- Python 3.12+
- Understanding of the target job portal's structure (HTML/API)
- Basic knowledge of web scraping or API integration

## Step-by-Step Guide

### Step 1: Create the Scraper File

Create a new file in `job-monitoring/src/job_monitor/scrapers/` named after your portal:

```bash
cd job-monitoring/src/job_monitor/scrapers/
touch myportal.py
```

### Step 2: Implement the BaseScraper Interface

```python
# myportal.py
from typing import Any, Dict, List
from datetime import datetime
from pathlib import Path
import requests
from pydantic import HttpUrl

from job_monitor.schemas import JobPosting
from job_monitor.scrapers.base import BaseScraper
from job_monitor.scrapers.utils import rate_limit, retry


class MyPortalScraper(BaseScraper):
    """MyPortal job scraper implementation."""
    
    # Required class attributes
    SCRAPER_ID = "myportal"           # Used in config files
    DISPLAY_NAME = "MyPortal"         # Human-readable name
    REQUIRES_COOKIES = False           # True if needs authentication
    REQUIRES_AUTH = False              # True if needs API keys
    BASE_URLS = ["https://myportal.com"]
    
    def _setup(self) -> None:
        """Initialize scraper (HTTP session, cookies, etc.)."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self._build_user_agent(),
            'Accept': 'application/json',
        })
        
        # Load cookies if required
        if self.REQUIRES_COOKIES and self.cookies_file:
            self._load_cookies()
    
    def validate_config(self) -> bool:
        """Validate scraper-specific configuration."""
        # Check required config keys
        if self.REQUIRES_COOKIES and not self.cookies_file:
            return False
        if self.cookies_file and not self.cookies_file.exists():
            return False
        return True
    
    @rate_limit(delay=1.5)  # Respect rate limits
    @retry(max_attempts=3)   # Retry on failures
    def search(self, query: Dict[str, Any]) -> List[JobPosting]:
        """
        Search for jobs matching the query.
        
        Args:
            query: Dictionary with search parameters
                - keywords: str - Search terms
                - location: str - Location filter
                - limit: int - Max results (default: 20)
                
        Returns:
            List of JobPosting objects
        """
        # Extract query parameters
        keywords = query.get('keywords', '')
        location = query.get('location', '')
        limit = query.get('limit', 20)
        
        # Build API/search request
        response = self.session.get(
            f"{self.BASE_URLS[0]}/api/jobs",
            params={
                'q': keywords,
                'location': location,
                'limit': limit
            }
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Parse results
        jobs = []
        for item in data.get('jobs', []):
            job = self._parse_job(item)
            if job:
                jobs.append(job)
        
        return jobs
    
    def _parse_job(self, data: Dict[str, Any]) -> JobPosting:
        """Convert portal-specific data to JobPosting."""
        return JobPosting(
            url=HttpUrl(data['url']),
            title=data['title'],
            company=data.get('company', 'Unknown'),
            location=data.get('location', ''),
            posted_date=data.get('posted_date'),
            discovered_date=datetime.now(),
            description=data.get('description'),
            salary=self._parse_salary(data.get('salary')),
            remote=data.get('remote', False),
            source=self.DISPLAY_NAME
        )
    
    def _parse_salary(self, salary_data: Any) -> str | None:
        """Parse salary information."""
        if not salary_data:
            return None
        # Implement portal-specific salary parsing
        return f"€{salary_data['min']}-{salary_data['max']}"
```

### Step 3: Register the Scraper

Add your scraper to the registry in `scrapers/__init__.py`:

```python
# __init__.py
from job_monitor.scrapers.myportal import MyPortalScraper

# At the end of the file, register it
ScraperRegistry.register(MyPortalScraper)
```

### Step 4: Create Tests

Create `tests/test_scrapers/test_myportal.py`:

```python
"""Tests for MyPortal scraper."""
import pytest
from unittest.mock import Mock, patch

from job_monitor.scrapers import ScraperRegistry


class TestMyPortalRegistration:
    """Test MyPortal scraper registration."""
    
    def test_myportal_registered(self):
        """Test MyPortal is in registry."""
        assert ScraperRegistry.is_registered('myportal')
    
    def test_myportal_metadata(self):
        """Test MyPortal metadata."""
        info = ScraperRegistry.get_scraper_info('myportal')
        assert info['name'] == 'MyPortal'
        assert info['requires_cookies'] is False


class TestMyPortalSearch:
    """Test MyPortal search functionality."""
    
    @patch('requests.Session.get')
    def test_search_basic_query(self, mock_get):
        """Test basic search."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'jobs': [{
                'url': 'https://myportal.com/job/123',
                'title': 'Python Developer',
                'company': 'Tech Corp',
                'location': 'City',
            }]
        }
        mock_get.return_value = mock_response
        
        scraper = ScraperRegistry.get_scraper('myportal', config={})
        jobs = scraper.search({'keywords': 'python', 'limit': 5})
        
        assert len(jobs) > 0
        assert jobs[0].title == 'Python Developer'


# Add more test classes as needed
```

### Step 5: Update Configuration

Add your scraper to `config.example.yaml`:

```yaml
sources:
  - name: myportal
    enabled: true
    queries:
      - keywords: "python developer"
        location: "City"
        limit: 20
```

### Step 6: Run Tests

```bash
# Test your specific scraper
pytest tests/test_scrapers/test_myportal.py -v

# Run all tests to ensure nothing broke
pytest tests/ -v

# Check test coverage
pytest tests/ --cov=job_monitor.scrapers.myportal --cov-report=html
```

### Step 7: Document Your Scraper

Add documentation to your scraper file:

```python
class MyPortalScraper(BaseScraper):
    """
    MyPortal job scraper.
    
    Portal Details:
        - URL: https://myportal.com
        - Type: REST API / HTML scraping
        - Authentication: None / Cookies required
        - Rate Limit: X requests per minute
    
    Supported Query Parameters:
        - keywords (str): Search terms
        - location (str): City or region
        - limit (int): Max results (1-100)
        - category (str, optional): Job category
    
    Example:
        scraper = ScraperRegistry.get_scraper('myportal', config={})
        jobs = scraper.search({
            'keywords': 'python developer',
            'location': 'Helsinki',
            'limit': 20
        })
    
    Notes:
        - Results are cached for 1 hour
        - Salary information may not always be available
        - Remote jobs marked with location "Remote"
    """
```

## Examples by Portal Type

### REST API Portal (like CV.ee)

```python
class APIPortalScraper(BaseScraper):
    SCRAPER_ID = "apiportal"
    REQUIRES_COOKIES = False
    
    def search(self, query):
        response = self.session.get(
            f"{self.BASE_URLS[0]}/api/v1/jobs",
            params={'q': query.get('keywords')}
        )
        return [self._parse_job(j) for j in response.json()['results']]
```

### HTML Scraping Portal (like Duunitori)

```python
from bs4 import BeautifulSoup

class HTMLPortalScraper(BaseScraper):
    SCRAPER_ID = "htmlportal"
    REQUIRES_COOKIES = True
    
    def search(self, query):
        response = self.session.get(
            f"{self.BASE_URLS[0]}/search",
            params={'q': query.get('keywords')}
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        
        jobs = []
        for card in soup.select('.job-card'):
            job = self._parse_card(card)
            if job:
                jobs.append(job)
        return jobs
    
    def _parse_card(self, card):
        return JobPosting(
            url=HttpUrl(card.select_one('a')['href']),
            title=card.select_one('.title').text.strip(),
            company=card.select_one('.company').text.strip(),
            # ... more parsing
        )
```

## Best Practices

### 1. Respect Rate Limits

Always use the `@rate_limit` decorator:

```python
@rate_limit(delay=2.0)  # 2 seconds between requests
def search(self, query):
    ...
```

### 2. Handle Errors Gracefully

```python
try:
    response = self.session.get(url)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"⚠️  Error scraping {self.DISPLAY_NAME}: {e}")
    return []
```

### 3. Cache Static Data

```python
from job_monitor.scrapers.utils import cached

@cached(ttl=3600)  # Cache for 1 hour
def _get_categories(self):
    """Fetch and cache category list."""
    response = self.session.get(f"{self.BASE_URLS[0]}/api/categories")
    return response.json()
```

### 4. Validate Input

```python
def search(self, query):
    keywords = query.get('keywords', '').strip()
    if not keywords:
        print("⚠️  No keywords provided")
        return []
    
    limit = min(query.get('limit', 20), 100)  # Cap at 100
    ...
```

### 5. Log Progress

```python
def search(self, query):
    print(f"\n🔍 Searching {self.DISPLAY_NAME}: {query.get('keywords')}")
    
    jobs = self._fetch_jobs(query)
    
    print(f"✅ Found {len(jobs)} jobs from {self.DISPLAY_NAME}")
    return jobs
```

## Common Issues

### Issue: Cookies Not Working

**Solution:** Check cookie format and expiration:

```python
def _load_cookies(self):
    with open(self.cookies_file, 'r') as f:
        cookies = json.load(f)
    
    for cookie in cookies:
        # Verify required fields
        if 'name' not in cookie or 'value' not in cookie:
            raise ValueError(f"Invalid cookie format in {self.cookies_file}")
        
        self.session.cookies.set(
            name=cookie['name'],
            value=cookie['value'],
            domain=cookie.get('domain', ''),
            path=cookie.get('path', '/')
        )
```

### Issue: Rate Limiting Errors

**Solution:** Increase delay or implement backoff:

```python
@rate_limit(delay=3.0)  # Increase from 1.5 to 3.0
@retry(max_attempts=5, backoff=2.0)  # More retries with backoff
def search(self, query):
    ...
```

### Issue: Parsing Errors

**Solution:** Add defensive parsing:

```python
def _parse_job(self, data):
    try:
        return JobPosting(
            url=HttpUrl(data['url']),
            title=data.get('title', 'Unknown Title'),
            company=data.get('company', 'Unknown Company'),
            # ... with defaults
        )
    except Exception as e:
        print(f"⚠️  Error parsing job: {e}")
        return None  # Skip invalid jobs
```

## Testing Checklist

Before submitting your scraper:

- [ ] Scraper is registered in `__init__.py`
- [ ] All class attributes defined (SCRAPER_ID, DISPLAY_NAME, etc.)
- [ ] `_setup()` initializes session/cookies correctly
- [ ] `validate_config()` checks required configuration
- [ ] `search()` handles all query parameters
- [ ] Error handling for network failures
- [ ] Rate limiting configured appropriately
- [ ] Unit tests cover main functionality
- [ ] Integration test with live API (optional, mark with `@pytest.mark.integration`)
- [ ] Documentation added to class docstring
- [ ] Config example added to `config.example.yaml`

## Reference

- **Base Scraper:** `job_monitor/scrapers/base.py`
- **CV.ee Example:** `job_monitor/scrapers/cvee.py`
- **Duunitori Example:** `job_monitor/scrapers/duunitori.py`
- **Utilities:** `job_monitor/scrapers/utils.py`
- **Tests:** `tests/test_scrapers/`

## Support

For questions or issues:
1. Check existing scraper implementations
2. Review test files for examples
3. Check architecture documentation: `docs/scraper-architecture.md`

---

**Last Updated:** December 2, 2025  
**Maintainer:** Michele Keil
