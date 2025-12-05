"""
CV.ee job scraper implementation.

Uses the CV.ee REST API with Elasticsearch backend.
API documentation: docs/cvee-api-*.md
"""
import json
import logging
import re
from typing import Any
from urllib.parse import urljoin

import requests

from job_monitor.schemas import JobPosting

from .base import BaseScraper
from .utils import cached, rate_limit, retry

logger = logging.getLogger(__name__)


class CVeeScraper(BaseScraper):
    """Scraper for CV.ee job portal using their REST API."""

    # Scraper identification
    SCRAPER_ID = "cvee"
    DISPLAY_NAME = "CV.ee"
    REQUIRES_COOKIES = False
    REQUIRES_AUTH = False
    BASE_URLS = ["https://cv.ee"]

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert text to URL-friendly slug for CV.ee.

        Args:
            text: Text to convert to slug

        Returns:
            URL-friendly slug
        """
        # Convert to lowercase
        text = text.lower()
        # Replace Estonian letters
        text = text.replace('õ', 'o').replace('ä', 'a').replace('ö', 'o').replace('ü', 'u')
        # Remove dots (from OÜ, AS, etc.)
        text = text.replace('.', '')
        # Remove special characters except alphanumeric, spaces, and hyphens
        text = re.sub(r'[^\w\s-]', '', text)
        # Replace spaces with hyphens
        text = re.sub(r'[-\s]+', '-', text)
        # Remove leading/trailing hyphens
        return text.strip('-')

    def fetch_job_details(self, job_id: int) -> dict[str, Any | None]:
        """Fetch full job details by scraping the job page.

        The CV.ee website embeds complete job data in a JSON script tag.
        This method extracts that data, including the full job description
        broken into sections (duties, requirements, benefits, etc.).

        Args:
            job_id: CV.ee vacancy ID

        Returns:
            Dictionary with full job details, or None if fetch fails
        """
        from bs4 import BeautifulSoup

        url = f"{self.BASE_URL}/et/vacancy/{job_id}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the Next.js data script tag
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and script.string.strip().startswith('{'):
                    try:
                        data = json.loads(script.string)

                        # Navigate to the vacancy data
                        if 'props' in data and 'pageProps' in data['props']:
                            redux = data['props']['pageProps']['initialReduxState']

                            if 'publicVacancies' in redux:
                                vacancy = redux['publicVacancies'].get(str(job_id))

                                if vacancy:
                                    # Extract and combine description sections
                                    full_content = []

                                    if 'details' in vacancy and 'standardDetails' in vacancy['details']:
                                        for section in vacancy['details']['standardDetails']:
                                            title = section.get('title', '')
                                            content = section.get('content', '')

                                            if content:
                                                # Parse HTML to get clean text
                                                content_soup = BeautifulSoup(content, 'html.parser')
                                                text = content_soup.get_text(separator='\n', strip=True)

                                                if title:
                                                    full_content.append(f"{title}:\n{text}")
                                                else:
                                                    full_content.append(text)

                                    # Combine all sections
                                    description = '\n\n'.join(full_content)

                                    # Return enriched data
                                    return {
                                        'id': job_id,
                                        'description': description,
                                        'highlights': vacancy.get('highlights', {}),
                                        'employer': vacancy.get('employer', {}),
                                        'raw_data': vacancy,
                                    }
                    except json.JSONDecodeError:
                        continue

            logger.warning(f"No job data found in page for job {job_id}")
            return None

        except Exception as e:
            logger.error(f"Failed to fetch job details for {job_id}: {e}")
            return None

    # API endpoints
    BASE_URL = "https://cv.ee"
    SEARCH_API = "/api/v1/vacancy-search-service/search"
    LOCATIONS_API = "/api/v1/locations-service/list"
    CATEGORIES_API = "/api/v1/vacancies-service/categories"

    def _setup(self) -> None:
        """Initialize CV.ee scraper with session and caches."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'et-EE,et;q=0.9,en;q=0.8',
        })

        # Cache location and category mappings
        self._locations_cache: dict[int, dict[str, Any | None]] = None
        self._categories_cache: dict[int, str | None] = None

        logger.info("CV.ee scraper initialized")

    @cached(ttl=86400)  # Cache locations for 24 hours
    def _get_locations(self) -> dict[int, dict[str, Any]]:
        """Fetch and cache location data from CV.ee API.

        Returns:
            Dictionary mapping location ID to location data:
            {
                1: {"id": 1, "name": "Tallinn", "type": "city"},
                2: {"id": 2, "name": "Tartu", "type": "city"},
                ...
            }
        """
        if self._locations_cache is not None:
            return self._locations_cache

        url = urljoin(self.BASE_URL, self.LOCATIONS_API)

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Build ID -> location mapping
            locations = {}
            for loc in data.get('data', []):
                loc_id = loc.get('id')
                if loc_id:
                    locations[loc_id] = {
                        'id': loc_id,
                        'name': loc.get('name', ''),
                        'type': loc.get('type', 'unknown'),
                    }

            self._locations_cache = locations
            logger.info(f"Cached {len(locations)} locations from CV.ee")
            return locations

        except Exception as e:
            logger.error(f"Failed to fetch CV.ee locations: {e}")
            return {}

    @cached(ttl=86400)  # Cache categories for 24 hours
    def _get_categories(self) -> dict[int, str]:
        """Fetch and cache category data from CV.ee API.

        Returns:
            Dictionary mapping category ID to category name:
            {1: "IT", 2: "Finance", ...}
        """
        if self._categories_cache is not None:
            return self._categories_cache

        url = urljoin(self.BASE_URL, self.CATEGORIES_API)

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Build ID -> name mapping
            categories = {}
            for cat in data.get('data', []):
                cat_id = cat.get('id')
                if cat_id:
                    categories[cat_id] = cat.get('name', '')

            self._categories_cache = categories
            logger.info(f"Cached {len(categories)} categories from CV.ee")
            return categories

        except Exception as e:
            logger.error(f"Failed to fetch CV.ee categories: {e}")
            return {}

    def _resolve_location(self, location_ids: list[int]) -> str:
        """Convert location IDs to readable location string.

        Args:
            location_ids: List of location IDs from API response

        Returns:
            Comma-separated location names, or "Unknown" if none found
        """
        if not location_ids:
            return "Unknown"

        locations = self._get_locations()
        names = [
            locations[loc_id]['name']
            for loc_id in location_ids
            if loc_id in locations
        ]

        return ", ".join(names) if names else "Unknown"

    def _parse_salary(self, vacancy: dict[str, Any]) -> str | None:
        """Extract and format salary information.

        Args:
            vacancy: Vacancy data from API

        Returns:
            Formatted salary string like "2000-3000 EUR/month" or None
        """
        salary_from = vacancy.get('salary_from')
        salary_to = vacancy.get('salary_to')
        currency = vacancy.get('salary_currency', 'EUR')
        period = vacancy.get('salary_period', 'month')

        if not salary_from and not salary_to:
            return None

        if salary_from and salary_to:
            return f"{salary_from}-{salary_to} {currency}/{period}"
        elif salary_from:
            return f"From {salary_from} {currency}/{period}"
        elif salary_to:
            return f"Up to {salary_to} {currency}/{period}"

        return None

    def _parse_job(self, vacancy: dict[str, Any]) -> JobPosting:
        """Parse a single vacancy from CV.ee API response.

        Args:
            vacancy: Raw vacancy data from API

        Returns:
            JobPosting object
        """
        # Extract basic fields - note: API uses positionTitle and employerName
        job_id = vacancy.get('id', '')
        title = vacancy.get('positionTitle', vacancy.get('title', 'Unknown Title'))
        company = vacancy.get('employerName', vacancy.get('company_name', 'Unknown Company'))

        # Resolve location from IDs
        location_ids = vacancy.get('townId', [])
        if isinstance(location_ids, int):
            location_ids = [location_ids]
        location = self._resolve_location(location_ids)

        # Build URL - CV.ee uses /et/vacancy/{id} format
        url = f"{self.BASE_URL}/et/vacancy/{job_id}" if job_id else ""

        # Extract dates - API uses publishDate
        published_date = vacancy.get('publishDate', vacancy.get('published_at', ''))

        # Parse salary - API uses salaryFrom/salaryTo
        salary_from = vacancy.get('salaryFrom')
        salary_to = vacancy.get('salaryTo')
        # NOTE: salary info extracted for future use in scoring/filtering
        if salary_from or salary_to:
            if salary_from and salary_to:
                _ = f"{salary_from}-{salary_to} EUR"
            elif salary_from:
                _ = f"From {salary_from} EUR"
            elif salary_to:
                _ = f"Up to {salary_to} EUR"

        # Get description - API uses positionContent (often empty in search results)
        description = vacancy.get('positionContent') or vacancy.get('description') or ''
        description = description.strip() if description else None

        # Build standardized JobPosting object
        job_data = {
            'id': str(job_id),
            'title': title,
            'company': company,
            'location': location,
            'url': url,
            'posted_date': published_date,
            'source': 'cvee',
            'description': description if description else None,
        }

        return JobPosting(**job_data)

    @retry(max_attempts=3, backoff=2.0)
    @rate_limit(delay=1.5)
    def search(self, query: dict[str, Any]) -> list[JobPosting]:
        """Search for jobs on CV.ee using their API.

        Args:
            query: Query parameters dictionary with fields:
                - keywords: Search term (job title, keywords, etc.)
                - location: Location name (will be resolved to ID)
                - limit: Maximum number of results to return (default: 100)
                - category: Category ID or name
                - salary_from: Minimum salary
                - salary_to: Maximum salary
                - employment_type: Full-time, part-time, etc.
                - page: Page number (default: 1)
                - page_size: Results per page (default: 20, max: 100)

        Returns:
            List of JobPosting objects
        """
        url = urljoin(self.BASE_URL, self.SEARCH_API)

        # Extract query parameters
        keywords = query.get('keywords')
        location_name = query.get('location')
        limit = query.get('limit', 100)

        # Build query parameters using CV.ee's actual API format
        params: dict[str, Any] = {
            'limit': min(limit, 100),
            'offset': query.get('offset', 0),
            'sorting': 'RELEVANCE',
            'showHidden': True,
        }

        # Keywords must be passed as array parameter (keywords[])
        if keywords:
            params['keywords[]'] = keywords

        # Resolve location name to ID if provided
        if location_name:
            locations = self._get_locations()
            location_id = None

            # Search for location by name (case-insensitive)
            location_lower = location_name.lower()
            for loc_id, loc_data in locations.items():
                if loc_data['name'].lower() == location_lower:
                    location_id = loc_id
                    break

            if location_id:
                params['location_ids'] = [location_id]
            else:
                logger.warning(f"Location '{location_name}' not found in CV.ee database")

        # Add optional filters
        if 'category' in query:
            # If category is a string, try to resolve it to ID
            category = query['category']
            if isinstance(category, str):
                categories = self._get_categories()
                category_lower = category.lower()
                for cat_id, cat_name in categories.items():
                    if cat_name.lower() == category_lower:
                        params['category_id'] = cat_id
                        break
            else:
                params['category_id'] = category

        if 'salary_from' in query:
            params['salary_from'] = query['salary_from']

        if 'salary_to' in query:
            params['salary_to'] = query['salary_to']

        if 'employment_type' in query:
            params['employment_type'] = query['employment_type']

        # Make API request
        try:
            logger.debug(f"CV.ee API request: {url} with params {params}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Extract vacancies from response - API returns vacancies at top level
            vacancies = data.get('vacancies', [])
            total = data.get('total', 0)

            if not vacancies:
                logger.warning(f"No results found for query: {keywords}")
                return []

            # Parse and standardize jobs (limit already applied in params)
            jobs = [self._parse_job(v) for v in vacancies]

            logger.info(f"Found {len(jobs)} jobs on CV.ee (total available: {total})")
            return jobs

        except requests.exceptions.RequestException as e:
            logger.error(f"CV.ee API request failed: {e}")
            return []
        except (KeyError, ValueError) as e:
            logger.error(f"Failed to parse CV.ee response: {e}")
            return []

    def validate_config(self) -> bool:
        """Validate scraper configuration.

        CV.ee doesn't require cookies or special configuration.

        Returns:
            Always True (no validation needed)
        """
        return True
