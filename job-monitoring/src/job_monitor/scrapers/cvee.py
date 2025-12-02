"""
CV.ee job scraper implementation.

Uses the CV.ee REST API with Elasticsearch backend.
API documentation: docs/cvee-api-*.md
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
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
        self._locations_cache: Optional[Dict[int, Dict[str, Any]]] = None
        self._categories_cache: Optional[Dict[int, str]] = None
        
        logger.info("CV.ee scraper initialized")
    
    @cached(ttl=86400)  # Cache locations for 24 hours
    def _get_locations(self) -> Dict[int, Dict[str, Any]]:
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
    def _get_categories(self) -> Dict[int, str]:
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
    
    def _resolve_location(self, location_ids: List[int]) -> str:
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
    
    def _parse_salary(self, vacancy: Dict[str, Any]) -> Optional[str]:
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
    
    def _parse_job(self, vacancy: Dict[str, Any]) -> JobPosting:
        """Parse a single vacancy from CV.ee API response.
        
        Args:
            vacancy: Raw vacancy data from API
        
        Returns:
            JobPosting object
        """
        # Extract basic fields
        job_id = vacancy.get('id', '')
        title = vacancy.get('title', 'Unknown Title')
        company = vacancy.get('company_name', 'Unknown Company')
        
        # Resolve location from IDs
        location_ids = vacancy.get('location_ids', [])
        location = self._resolve_location(location_ids)
        
        # Build URL
        slug = vacancy.get('slug', '')
        url = urljoin(self.BASE_URL, f"/vacancies/{slug}") if slug else ""
        
        # Extract dates
        published_date = vacancy.get('published_at', '')
        
        # Parse salary
        salary = self._parse_salary(vacancy)
        
        # Get description
        description = vacancy.get('description', '').strip()
        
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
    def search(self, query: Dict[str, Any]) -> List[JobPosting]:
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
        
        # Build query parameters
        params: Dict[str, Any] = {
            'page': query.get('page', 1),
            'page_size': min(query.get('page_size', 20), 100),
        }
        
        if keywords:
            params['keywords'] = keywords
        
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
            
            # Extract vacancies from response
            vacancies = data.get('data', {}).get('vacancies', [])
            
            if not vacancies:
                logger.warning(f"No results found for query: {keywords}")
                return []
            
            # Parse and standardize jobs
            jobs = [self._parse_job(v) for v in vacancies[:limit]]
            
            logger.info(f"Found {len(jobs)} jobs on CV.ee")
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
