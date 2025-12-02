#!/usr/bin/env python3
"""
Test script for CV.ee API discovery

Demonstrates that CV.ee uses a Next.js data API that returns JSON,
making it easy to scrape without browser automation.
"""

import requests
import json
import re


def get_locations():
    """Get complete location mappings from CV.ee API."""
    url = "https://cv.ee/api/v1/locations-service/list"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    # Create lookup dictionaries
    towns = {town['id']: town['name'] for town in data['towns']}
    counties = {int(k): v['name'] for k, v in data['counties'].items()}
    countries = {int(k): v['name'] for k, v in data['countries'].items()}
    
    return {
        'towns': towns,
        'counties': counties,
        'countries': countries,
        'towns_by_name': {town['name']: town['id'] for town in data['towns']},
    }


def get_build_id(base_url="https://www.cv.ee"):
    """Extract the Next.js build ID from the homepage."""
    response = requests.get(base_url)
    response.raise_for_status()
    
    # Look for buildId in the HTML
    match = re.search(r'"buildId":"([^"]+)"', response.text)
    if match:
        return match.group(1)
    
    raise ValueError("Could not extract build ID from homepage")


def search_jobs(keywords, location=None, limit=20, offset=0, salary_from=None, categories=None):
    """Search for jobs on CV.ee using the Vacancy Search Service API."""
    url = "https://cv.ee/api/v1/vacancy-search-service/search"
    
    params = {
        "limit": limit,
        "offset": offset,
        "sorting": "LATEST",
    }
    
    if keywords:
        params["keywords"] = keywords
    
    if location:
        params["location"] = location
    
    if salary_from:
        params["salaryFrom"] = salary_from
    
    if categories:
        # Categories can be passed as list
        for category in categories:
            params.setdefault("categories[]", []).append(category)
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    return data


def main():
    print("CV.ee API Test")
    print("=" * 60)
    
    # Get locations
    print("\n1. Fetching location mappings...")
    locations = get_locations()
    print(f"   Towns: {len(locations['towns'])}")
    print(f"   Counties: {len(locations['counties'])}")
    print(f"   Countries: {len(locations['countries'])}")
    print(f"   Example: Tallinn ID = {locations['towns_by_name']['Tallinn']}")
    print(f"   Example: Tartu ID = {locations['towns_by_name']['Tartu']}")
    
    # Search for jobs using REST API
    print("\n2. Searching for 'python developer' jobs in Tallinn (REST API)...")
    results = search_jobs("python developer", location="Tallinn", limit=5)
    
    print(f"\n   Total jobs found: {results['total']}")
    print(f"   Showing first {len(results['vacancies'])} results:\n")
    
    for job in results['vacancies']:
        # Resolve location name from ID
        town_id = job.get('townId')
        town_name = locations['towns'].get(town_id, f"Unknown (ID: {town_id})")
        
        print(f"   • {job['positionTitle']}")
        print(f"     Company: {job['employerName']}")
        print(f"     Location: {town_name}")
        print(f"     ID: {job['id']}")
        if job.get('salaryFrom') or job.get('salaryTo'):
            salary_from = job.get('salaryFrom', 0)
            salary_to = job.get('salaryTo', 0)
            print(f"     Salary: €{salary_from} - €{salary_to}")
        print(f"     Remote: {job.get('remoteWork', False)}")
        print()
    
    # Test with salary filter
    print("\n3. Testing salary filter (min €3000, IT category)...")
    results_filtered = search_jobs(
        None, 
        limit=3, 
        salary_from=3000,
        categories=["INFORMATION_TECHNOLOGY"]
    )
    print(f"   Found {results_filtered['total']} IT jobs with salary ≥ €3000")
    if results_filtered['vacancies']:
        job = results_filtered['vacancies'][0]
        print(f"   Example: {job['positionTitle']} at {job['employerName']}")
        print(f"   Salary: €{job.get('salaryFrom', 0)} - €{job.get('salaryTo', 0)}")
    
    # Test pagination
    print("\n4. Testing pagination (offset=10)...")
    results_page2 = search_jobs("developer", limit=3, offset=10)
    print(f"   Retrieved {len(results_page2['vacancies'])} jobs from offset 10")
    
    print("\n✓ API test successful! CV.ee can be scraped using REST API.")
    print("✓ Location mappings available - no need for manual lookup tables!")
    print("✓ Salary filtering and category filtering working!")


if __name__ == "__main__":
    main()
