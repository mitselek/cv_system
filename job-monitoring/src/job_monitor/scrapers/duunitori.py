"""
Duunitori job scraper.

Scrapes Finnish job portal Duunitori (https://duunitori.fi) using HTML parsing.
Requires authentication cookies for full access.
"""

import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import HttpUrl

from job_monitor.schemas import JobPosting
from job_monitor.scrapers.base import BaseScraper
from job_monitor.scrapers.utils import build_user_agent


class DuunitoriScraper(BaseScraper):
    """Duunitori job scraper using HTML parsing with cookies.
    
    Duunitori is a Finnish job portal that requires authentication cookies
    for full access to job listings. This scraper:
    - Parses HTML job listings
    - Optionally fetches full job descriptions
    - Caches descriptions to avoid redundant requests
    - Extracts contact information
    
    Configuration:
        rate_limit_delay: float - Delay between requests (default: 1.5)
        full_details: bool - Fetch full descriptions (default: False)
    
    Example:
        scraper = DuunitoriScraper(
            config={'full_details': True, 'rate_limit_delay': 2.0},
            cookies_file=Path('cookies/duunitori.json')
        )
        
        jobs = scraper.search({
            'keywords': 'python developer',
            'location': 'Helsinki',
            'limit': 20
        })
    """
    
    SCRAPER_ID = "duunitori"
    DISPLAY_NAME = "Duunitori"
    REQUIRES_COOKIES = True
    REQUIRES_AUTH = False
    BASE_URLS = ["https://duunitori.fi"]
    
    def _setup(self) -> None:
        """Setup HTTP session and load cookies."""
        self.session = requests.Session()
        
        # Load cookies
        if self.cookies_file:
            self._load_cookies()
        
        # Set headers
        self.session.headers.update({
            'User-Agent': build_user_agent(self.DISPLAY_NAME),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fi;q=0.8',
        })
    
    def _load_cookies(self) -> None:
        """Load cookies from JSON file.
        
        Supports two formats:
        1. List format: [{"name": "...", "value": "...", "domain": "..."}]
        2. Dict format: {"cookie_name": "cookie_value"}
        """
        if not self.cookies_file or not self.cookies_file.exists():
            raise ValueError(
                f"Cookie file not found: {self.cookies_file}\n"
                "To export cookies:\n"
                "1. Install browser extension: 'Cookie Editor' or 'EditThisCookie'\n"
                "2. Visit duunitori.fi and log in\n"
                "3. Export cookies as JSON\n"
                f"4. Save to: {self.cookies_file}"
            )
        
        with open(self.cookies_file, 'r') as f:
            cookies_data = json.load(f)
        
        # Handle different cookie export formats
        if isinstance(cookies_data, list):
            # Format: [{"name": "...", "value": "...", "domain": "..."}]
            for cookie in cookies_data:
                self.session.cookies.set(
                    str(cookie['name']),
                    str(cookie['value']),
                    domain=str(cookie.get('domain', ''))
                )
        else:
            # Format: {"cookie_name": "cookie_value"}
            for name, value in cookies_data.items():
                self.session.cookies.set(str(name), str(value))
    
    def validate_config(self) -> bool:
        """Validate Duunitori configuration.
        
        Returns:
            True if cookies file exists and is readable
        """
        if not self.cookies_file:
            return False
        if not self.cookies_file.exists():
            return False
        try:
            with open(self.cookies_file, 'r') as f:
                json.load(f)
            return True
        except (json.JSONDecodeError, IOError):
            return False
    
    def search(self, query: Dict[str, Any]) -> List[JobPosting]:
        """Search Duunitori for jobs.
        
        Query parameters:
            keywords: str - Search terms (required)
            location: str - Location filter (optional)
            limit: int - Max results (default: 20)
            full_details: bool - Fetch full descriptions (default: from config)
            state_manager: Any - Optional state manager for caching descriptions
        
        Returns:
            List of JobPosting objects
        
        Example:
            jobs = scraper.search({
                'keywords': 'python developer',
                'location': 'Helsinki',
                'limit': 20,
                'full_details': True
            })
        """
        keywords = query.get('keywords', '')
        location = query.get('location', '')
        limit = query.get('limit', 20)
        full_details = query.get('full_details', self.config.get('full_details', False))
        state_manager = query.get('state_manager')
        
        print(f"\n🔍 Searching {self.DISPLAY_NAME}: {keywords}")
        if location:
            print(f"   Location filter: {location}")
        if full_details:
            print(f"   📄 Full details mode: extracting descriptions (slower)")
        
        url = f"{self.BASE_URLS[0]}/tyopaikat"
        params = {
            'haku': keywords,
            'order_by': 'published',
        }
        if location:
            params['alue'] = location
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs: List[JobPosting] = []
            
            # Duunitori uses .job-box for job listings
            job_elements = soup.select('.job-box')
            
            print(f"   Found {len(job_elements)} job listings")
            
            for job_elem in job_elements[:limit]:
                job = self._parse_job(job_elem)
                if job:
                    # Set source
                    job.source = self.DISPLAY_NAME
                    jobs.append(job)
            
            # Extract full descriptions if requested
            if full_details and jobs:
                self._extract_full_details(jobs, state_manager)
            
            print(f"✅ Parsed {len(jobs)} jobs successfully")
            return jobs
            
        except Exception as e:
            print(f"❌ Error searching {self.DISPLAY_NAME}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _parse_job(self, elem: Tag) -> Optional[JobPosting]:
        """Parse a Duunitori job element from HTML.
        
        Args:
            elem: BeautifulSoup Tag element representing a job listing
        
        Returns:
            JobPosting object or None if parsing fails
        """
        try:
            # Duunitori structure: .job-box with h3.job-box__title
            title_elem = elem.select_one('.job-box__title, h3')
            location_elem = elem.select_one('.job-box__job-location')
            link_elem = elem.select_one('a.job-box__hover, a[href*="/tyopaikat/tyo/"]')
            posted_elem = elem.select_one('.job-box__job-posted')
            
            if not title_elem or not link_elem:
                return None
            
            # Company is in data-company attribute of the link
            company = 'Unknown'
            if link_elem and link_elem.get('data-company'):
                company = str(link_elem.get('data-company'))
            
            url = f"{self.BASE_URLS[0]}{link_elem['href']}"
            
            return JobPosting(
                url=HttpUrl(url),
                title=str(title_elem.get_text(strip=True)),
                company=company,
                location=str(location_elem.get_text(strip=True)) if location_elem else 'Unknown',
                posted_date=str(posted_elem.get_text(strip=True)) if posted_elem else None,
                discovered_date=datetime.now(),
                description=None,
                source=self.DISPLAY_NAME
            )
        except Exception as e:
            print(f"⚠️  Error parsing job: {e}")
            return None
    
    def _extract_full_details(
        self,
        jobs: List[JobPosting],
        state_manager: Any = None
    ) -> None:
        """Extract full job descriptions and contact info.
        
        Modifies jobs in-place to add descriptions and contact information.
        Uses state_manager cache if available to avoid redundant requests.
        
        Args:
            jobs: List of JobPosting objects to enrich
            state_manager: Optional state manager for caching
        """
        # Check cache for existing descriptions
        jobs_needing_details = []
        cached_count = 0
        
        for job in jobs:
            if state_manager:
                cached_job = state_manager.get_job(job.id)
                if cached_job and cached_job.description:
                    job.description = cached_job.description
                    cached_count += 1
                    continue
            jobs_needing_details.append(job)
        
        if cached_count > 0:
            print(f"   💾 Using cached descriptions for {cached_count} jobs")
        
        if jobs_needing_details:
            print(f"   📥 Extracting descriptions for {len(jobs_needing_details)} jobs...")
            for i, job in enumerate(jobs_needing_details, 1):
                print(f"      [{i}/{len(jobs_needing_details)}] {job.title[:50]}...")
                
                # Rate limiting
                delay = self.get_rate_limit_delay()
                time.sleep(delay)
                
                description, contact_info = self._extract_job_details(str(job.url))
                
                if description:
                    job.description = description
                
                # Update contact information
                if contact_info.get('contact_name'):
                    job.contact_name = contact_info['contact_name']
                if contact_info.get('contact_email'):
                    job.contact_email = contact_info['contact_email']
                if contact_info.get('contact_phone'):
                    job.contact_phone = contact_info['contact_phone']
            
            print(f"   ✅ Extracted {sum(1 for j in jobs_needing_details if j.description)} descriptions")
    
    def fetch_job_details(self, job_url: str) -> Dict[str, Any]:
        """Fetch full job details for CLI enrichment.
        
        Public interface for CLI to call when fetching job descriptions.
        
        Args:
            job_url: Full URL to job posting
        
        Returns:
            Dictionary with 'description' and contact info keys
        """
        description, contact_info = self._extract_job_details(job_url)
        return {
            'description': description,
            **contact_info
        }
    
    def _extract_job_details(self, job_url: str) -> Tuple[Optional[str], Dict[str, Optional[str]]]:
        """Fetch full job posting page and extract description and contact info.
        
        Args:
            job_url: Full URL to job posting
        
        Returns:
            Tuple of (description, contact_info dict)
            contact_info contains: contact_name, contact_email, contact_phone
        """
        try:
            response = self.session.get(job_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract description
            description = None
            desc_elem = soup.select_one('.description--jobentry, .description')
            if desc_elem:
                description = desc_elem.get_text(separator=' ', strip=True)
            
            # Extract contact information
            contact_info = self._extract_contact_info(soup)
            
            return description, contact_info
            
        except Exception as e:
            print(f"⚠️  Error extracting details from {job_url}: {e}")
            return None, {}
    
    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        """Extract contact information from job posting page.
        
        Args:
            soup: BeautifulSoup object of job posting page
        
        Returns:
            Dictionary with contact_name, contact_email, contact_phone
        """
        contact_info: Dict[str, Optional[str]] = {
            'contact_name': None,
            'contact_email': None,
            'contact_phone': None,
        }
        
        try:
            # 1. Try structured contact section first (anywhere on page)
            contact_section = soup.select_one('.contact-info, .job-contact')
            if contact_section:
                # Extract name
                name_elem = contact_section.select_one('.contact-name, .name')
                if name_elem:
                    contact_info['contact_name'] = name_elem.get_text(strip=True)
                
                # Extract email
                email_elem = contact_section.select_one('a[href^="mailto:"]')
                if email_elem:
                    href = email_elem.get('href', '')
                    email = str(href).replace('mailto:', '') if href else ''
                    if email:
                        contact_info['contact_email'] = email
                
                # Extract phone
                phone_elem = contact_section.select_one('.contact-phone, .phone, a[href^="tel:"]')
                if phone_elem:
                    phone = phone_elem.get_text(strip=True)
                    if phone:
                        contact_info['contact_phone'] = phone
            
            # 2. Fallback: Search in description section or whole page
            desc_elem = soup.select_one('.description--jobentry, .description')
            search_area = desc_elem if desc_elem else soup
            
            # Extract email from mailto links if not found yet
            if not contact_info['contact_email']:
                email_link = search_area.select_one('a[href^="mailto:"]')
                if email_link:
                    href = email_link.get('href', '')
                    email = str(href).replace('mailto:', '').strip()
                    if email:
                        contact_info['contact_email'] = email
            
            # Extract phone from tel links if not found yet
            if not contact_info['contact_phone']:
                phone_link = search_area.select_one('a[href^="tel:"]')
                if phone_link:
                    href = phone_link.get('href', '')
                    phone = str(href).replace('tel:', '').strip()
                    # Remove common phone number formatting
                    phone = re.sub(r'[\s\-\(\)]', '', phone)
                    if phone:
                        contact_info['contact_phone'] = phone
            
            # 3. Fallback: Regex extraction from text content
            text_content = search_area.get_text()
            
            # Extract email from text if not found yet
            if not contact_info['contact_email']:
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_content)
                if email_match:
                    contact_info['contact_email'] = email_match.group()
            
            # Extract phone from text if not found yet (Finnish format: 040, 050, +358, etc.)
            if not contact_info['contact_phone']:
                # Try Finnish mobile format first
                phone_match = re.search(r'\b(?:\+358|0)(?:40|50|45|44)\s*\d{3}\s*\d{4}\b', text_content)
                if phone_match:
                    phone = phone_match.group()
                    # Normalize: remove spaces
                    phone = re.sub(r'\s+', '', phone)
                    contact_info['contact_phone'] = phone
            
            # 4. Try to extract contact name (heuristic: find capitalized words near email)
            if contact_info['contact_email'] and not contact_info['contact_name']:
                # Look for patterns like "Contact: FirstName LastName" or "FirstName LastName\nEmail:"
                name_pattern = r'(?:Contact|Yhteyshenkilö|Yhteydet|Contact Person)[\s:]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'
                name_match = re.search(name_pattern, text_content)
                if name_match:
                    contact_info['contact_name'] = name_match.group(1).strip()
        
        except Exception as e:
            print(f"⚠️  Error extracting contact info: {e}")
        
        return contact_info
