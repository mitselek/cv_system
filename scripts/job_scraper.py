#!/usr/bin/env python3
"""
Job scraper for Finnish job portals using browser cookies.
Supports: Duunitori, Tyomarkkinatori, LinkedIn
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import HttpUrl

from schemas import JobPosting


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
    
    def search_duunitori(self, keywords: str, location: str = "", limit: int = 20) -> List[JobPosting]:
        """Search Duunitori for jobs."""
        print(f"\n🔍 Searching Duunitori: {keywords}")
        if location:
            print(f"   Location filter: {location}")
        
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
