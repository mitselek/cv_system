#!/usr/bin/env python3
"""
Job scraper for Finnish job portals using browser cookies.
Supports: Duunitori, Tyomarkkinatori, LinkedIn
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import HttpUrl

from job_monitor.schemas import JobPosting


class JobScraper:
    def __init__(self, cookies_file: Path):
        """Initialize scraper with cookies from file."""
        self.session = requests.Session()
        self.cookies_file = cookies_file
        self.load_cookies()
    
    def load_cookies(self) -> None:
        """Load cookies from JSON file.
        
        Note: Type ignores below are necessary because:
        1. json.load() returns Any - JSON structure is runtime-determined
        2. Cookie formats vary (list of dicts vs simple dict) from browser exports
        3. requests library has incomplete type stubs (upstream issue)
        
        These are safe runtime operations with proper error handling.
        If debugging cookie issues, check the actual JSON file format first.
        """
        if not self.cookies_file.exists():
            print(f"❌ Cookie file not found: {self.cookies_file}")
            print("\nTo export cookies:")
            print("1. Install browser extension: 'Cookie Editor' or 'EditThisCookie'")
            print("2. Visit the job portal and log in")
            print("3. Export cookies as JSON")
            print(f"4. Save to: {self.cookies_file}")
            sys.exit(1)
        
        # just let me say, that all that ignoring thing looks like workaround hack. I hope to not stumble on these lines in future while debugging some extremely annoying issue.
        with open(self.cookies_file, 'r') as f:
            cookies_data = json.load(f)
        
        # Handle different cookie export formats
        if isinstance(cookies_data, list):
            # Format: [{"name": "...", "value": "...", "domain": "..."}]
            for cookie_item in cookies_data:
                cookie: Dict[str, Any] = cookie_item
                self.session.cookies.set(
                    str(cookie['name']),
                    str(cookie['value']),
                    domain=str(cookie.get('domain', ''))
                )
        else:
            # Format: {"cookie_name": "cookie_value"}
            cookies_dict: Dict[str, Any] = cookies_data
            for name, value in cookies_dict.items():
                self.session.cookies.set(str(name), str(value))
        
        # Set common headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fi;q=0.8',
        })
    
    def _extract_job_details(self, job_url: str, delay: float = 1.5) -> tuple[str | None, dict[str, str | None]]:
        """Fetch full job posting page and extract description and contact info.
        
        Args:
            job_url: Full URL to job posting
            delay: Delay in seconds before fetching (rate limiting)
            
        Returns:
            Tuple of (description, contact_info dict) or (None, empty dict) if extraction fails
        """
        try:
            # Rate limiting - be respectful to the server
            time.sleep(delay)
            
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
    
    def _extract_contact_info(self, soup: BeautifulSoup) -> dict[str, str | None]:
        """
        Extract contact information from job detail page.
        
        Args:
            soup: BeautifulSoup object of the job detail page
            
        Returns:
            Dict with contact_name, contact_email, contact_phone (values may be None)
        """
        contact_info = {
            'contact_name': None,
            'contact_email': None,
            'contact_phone': None
        }
        
        try:
            # Look for email with mailto: links
            email_link = soup.select_one('a[href^="mailto:"]')
            if email_link:
                email = email_link.get('href', '').replace('mailto:', '').strip()
                if email:
                    contact_info['contact_email'] = email
            
            # Look for phone numbers with tel: links
            phone_link = soup.select_one('a[href^="tel:"]')
            if phone_link:
                phone = phone_link.get('href', '').replace('tel:', '').strip()
                if phone:
                    contact_info['contact_phone'] = phone
            
            # Search for email patterns in text if not found
            if not contact_info['contact_email']:
                import re
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                text = soup.get_text()
                emails = re.findall(email_pattern, text)
                if emails:
                    contact_info['contact_email'] = emails[0]
            
            # Search for phone patterns (Finnish numbers)
            if not contact_info['contact_phone']:
                import re
                phone_pattern = r'(?:\+358|0)[\s-]?\d{1,3}[\s-]?\d{3,4}[\s-]?\d{3,4}'
                text = soup.get_text()
                phones = re.findall(phone_pattern, text)
                if phones:
                    contact_info['contact_phone'] = phones[0].strip()
            
            # Look for contact person name (simple text search near contact info)
            if contact_info['contact_email'] or contact_info['contact_phone']:
                # Try to find name near contact info
                text_lines = soup.get_text().split('\n')
                for i, line in enumerate(text_lines):
                    if contact_info['contact_email'] and contact_info['contact_email'] in line:
                        # Check previous lines for a name
                        for j in range(max(0, i-3), i):
                            potential_name = text_lines[j].strip()
                            # Simple heuristic: 2-4 words, each capitalized
                            words = potential_name.split()
                            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                                contact_info['contact_name'] = potential_name
                                break
                        break
        
        except Exception as e:
            print(f"⚠️  Error extracting contact info: {e}")
        
        return contact_info
    
    def search_duunitori(self, keywords: str, location: str = "", limit: int = 20, full_details: bool = False, state_manager: Any = None) -> List[JobPosting]:
        """Search Duunitori for jobs.
        
        Args:
            keywords: Search keywords
            location: Location filter
            limit: Maximum number of results
            full_details: If True, extract full job descriptions (slower)
            state_manager: Optional state manager for description caching
        """
        print(f"\n🔍 Searching Duunitori: {keywords}")
        if location:
            print(f"   Location filter: {location}")
        if full_details:
            print(f"   📄 Full details mode: extracting descriptions (slower)")
        
        url = "https://duunitori.fi/tyopaikat"
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
                job = self._parse_duunitori_job(job_elem)
                if job:
                    jobs.append(job)
            
            # Extract full descriptions if requested
            if full_details and jobs:
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
            
            print(f"✅ Parsed {len(jobs)} jobs successfully")
            return jobs
            
        except Exception as e:
            print(f"❌ Error searching Duunitori: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _parse_duunitori_job(self, elem: Tag) -> Optional[JobPosting]:
        """Parse a Duunitori job element."""
        try:
            # Duunitori structure: .job-box with h3.job-box__title
            title_elem = elem.select_one('.job-box__title, h3')
            location_elem = elem.select_one('.job-box__job-location')
            link_elem = elem.select_one('a.job-box__hover, a[href*="/tyopaikat/tyo/"]')
            posted_elem = elem.select_one('.job-box__job-posted')
            
            if not title_elem or not link_elem:
                return None
            
            # Company is in data-company attribute of the link
            company: str = 'Unknown'
            if link_elem and link_elem.get('data-company'):
                company = str(link_elem.get('data-company'))
            
            url = f"https://duunitori.fi{link_elem['href']}"
            
            return JobPosting(
                url=HttpUrl(url),
                title=str(title_elem.get_text(strip=True)),
                company=company,
                location=str(location_elem.get_text(strip=True)) if location_elem else 'Unknown',
                posted_date=str(posted_elem.get_text(strip=True)) if posted_elem else None,
                discovered_date=datetime.now(),
                description=None,
            )
        except Exception as e:
            print(f"⚠️  Error parsing job: {e}")
            return None
    
    def search_tyomarkkinatori(self, keywords: str) -> List[JobPosting]:
        """Search Tyomarkkinatori for jobs."""
        print(f"\n🔍 Searching Tyomarkkinatori: {keywords}")
        
        # This requires authenticated access to their API or web interface
        url = "https://tyomarkkinatori.fi/henkiloasiakkaat/avoimet-tyopaikat"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # The actual implementation depends on their HTML structure
            # or if they have a JSON API endpoint
            # soup = BeautifulSoup(response.text, 'html.parser')  # Pending implementation
            
            print("⚠️  Tyomarkkinatori scraping needs HTML structure analysis")
            return []
            
        except Exception as e:
            print(f"❌ Error searching Tyomarkkinatori: {e}")
            return []
    
    def search_linkedin(self, keywords: str, location: str = "Finland") -> List[JobPosting]:
        """Search LinkedIn for jobs."""
        print(f"\n🔍 Searching LinkedIn: {keywords} in {location}")
        
        url = "https://www.linkedin.com/jobs/search/"
        params = {
            'keywords': keywords,
            'location': location,
            'f_WT': '2',  # Remote jobs
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            jobs: List[JobPosting] = []
            
            # LinkedIn job cards
            job_elements = soup.select('.job-search-card, .jobs-search-results__list-item')
            
            for job_elem in job_elements[:10]:
                job = self._parse_linkedin_job(job_elem)
                if job:
                    jobs.append(job)
            
            print(f"✅ Found {len(jobs)} jobs on LinkedIn")
            return jobs
            
        except Exception as e:
            print(f"❌ Error searching LinkedIn: {e}")
            return []
    
    def _parse_linkedin_job(self, elem: Tag) -> Optional[JobPosting]:
        """Parse a LinkedIn job element."""
        try:
            title_elem = elem.select_one('.job-search-card__title, h3')
            company_elem = elem.select_one('.job-search-card__company-name, h4')
            location_elem = elem.select_one('.job-search-card__location')
            link_elem = elem.select_one('a')
            
            if not title_elem or not link_elem or not link_elem.get('href'):
                return None
            
            url = str(link_elem['href'])
            
            return JobPosting(
                url=HttpUrl(url),
                title=str(title_elem.get_text(strip=True)),
                company=str(company_elem.get_text(strip=True)) if company_elem else 'Unknown',
                location=str(location_elem.get_text(strip=True)) if location_elem else 'Unknown',
                posted_date=None,
                discovered_date=datetime.now(),
                description=None,
            )
        except Exception as e:
            print(f"⚠️  Error parsing job: {e}")
            return None


def main() -> None:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Search Finnish job portals')
    parser.add_argument('keywords', help='Job search keywords (e.g., "project manager IT")')
    parser.add_argument('--portal', choices=['duunitori', 'tyomarkkinatori', 'linkedin', 'all'],
                        default='duunitori', help='Which portal to search (default: duunitori)')
    parser.add_argument('--location', default='', help='Location filter (e.g., Helsinki, Tallinn)')
    parser.add_argument('--limit', type=int, default=20, help='Maximum number of results (default: 20)')
    parser.add_argument('--cookies', type=Path, 
                        default=Path.home() / '.config' / 'job_scraper_cookies_duunitori.json',
                        help='Path to cookies JSON file')
    parser.add_argument('--output', type=Path, help='Output JSON file for results')
    parser.add_argument('--format', choices=['text', 'json', 'csv'], default='text',
                        help='Output format (default: text)')
    
    args = parser.parse_args()
    
    scraper = JobScraper(args.cookies)
    all_jobs: List[JobPosting] = []
    
    if args.portal in ['duunitori', 'all']:
        all_jobs.extend(scraper.search_duunitori(args.keywords, args.location, args.limit))
    
    if args.portal in ['tyomarkkinatori', 'all']:
        all_jobs.extend(scraper.search_tyomarkkinatori(args.keywords))
    
    if args.portal in ['linkedin', 'all']:
        all_jobs.extend(scraper.search_linkedin(args.keywords, args.location or 'Finland'))
    
    # Display results based on format
    if args.format == 'json':
        jobs_data = [job.model_dump(mode='json') for job in all_jobs]
        print(json.dumps(jobs_data, indent=2, ensure_ascii=False))
    elif args.format == 'csv':
        if all_jobs:
            import csv
            import sys
            jobs_data = [job.model_dump(mode='json') for job in all_jobs]
            writer = csv.DictWriter(sys.stdout, fieldnames=jobs_data[0].keys())
            writer.writeheader()
            writer.writerows(jobs_data)
    else:  # text format
        print(f"\n{'='*80}")
        print(f"📊 TOTAL RESULTS: {len(all_jobs)}")
        print(f"{'='*80}\n")
        
        for i, job in enumerate(all_jobs, 1):
            print(f"{i}. {job.title}")
            print(f"   Company: {job.company}")
            print(f"   Location: {job.location}")
            if job.posted_date:
                print(f"   Posted: {job.posted_date}")
            print(f"   URL: {job.url}")
            print()
    
    # Save to file if requested
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.format == 'csv':
                import csv
                if all_jobs:
                    jobs_data = [job.model_dump(mode='json') for job in all_jobs]
                    writer = csv.DictWriter(f, fieldnames=jobs_data[0].keys())
                    writer.writeheader()
                    writer.writerows(jobs_data)
            else:
                jobs_data = [job.model_dump(mode='json') for job in all_jobs]
                json.dump(jobs_data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Results saved to: {args.output}")


if __name__ == '__main__':
    main()
