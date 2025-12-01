#!/usr/bin/env python3
"""Tests for description caching to avoid re-fetching."""

import unittest
from unittest.mock import Mock, MagicMock
from pathlib import Path
from job_monitor.scraper import JobScraper
from job_monitor.schemas import JobPosting
from datetime import datetime


class TestDescriptionCaching(unittest.TestCase):
    """Test that descriptions are cached and not re-fetched."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_cookies = Path("/tmp/test_cookies_cache.json")
        self.mock_cookies.write_text('{"test": "cookie"}')
        
    def tearDown(self):
        """Clean up test fixtures."""
        if self.mock_cookies.exists():
            self.mock_cookies.unlink()
    
    def test_cached_descriptions_not_refetched(self):
        """Test that cached descriptions are reused, not re-fetched."""
        from unittest.mock import patch
        
        search_html = """
        <html>
            <div class="job-box">
                <h3 class="job-box__title">Test Job</h3>
                <div class="job-box__job-location">Helsinki</div>
                <a class="job-box__hover" href="/tyopaikat/tyo/test-123" data-company="TestCorp"></a>
            </div>
        </html>
        """
        
        with patch('job_monitor.scraper.requests.Session') as mock_session_class:
            mock_session = MagicMock()
            search_response = Mock()
            search_response.text = search_html
            search_response.raise_for_status = Mock()
            mock_session.get.return_value = search_response
            mock_session_class.return_value = mock_session
            
            scraper = JobScraper(self.mock_cookies)
            scraper.session = mock_session
            
            # Create mock state manager with cached job
            mock_state_manager = Mock()
            cached_job = JobPosting(
                url="https://duunitori.fi/tyopaikat/tyo/test-123",
                title="Test Job",
                company="TestCorp",
                location="Helsinki",
                posted_date=None,
                discovered_date=datetime.now(),
                description="Cached description with Python, SQL, agile keywords"
            )
            # Mock ID generation to match
            cached_job.id = "test-123-id"
            mock_state_manager.get_job.return_value = cached_job
            
            # Search with full_details and state_manager
            jobs = scraper.search_duunitori(
                "test", 
                full_details=True, 
                limit=1,
                state_manager=mock_state_manager
            )
            
            # Should have made only 1 request (search), not 2 (search + details)
            self.assertEqual(mock_session.get.call_count, 1)
            
            # Job should have the cached description
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0].description, "Cached description with Python, SQL, agile keywords")
    
    def test_new_jobs_fetch_descriptions(self):
        """Test that new jobs (not in cache) fetch descriptions."""
        from unittest.mock import patch
        
        search_html = """
        <html>
            <div class="job-box">
                <h3 class="job-box__title">New Job</h3>
                <div class="job-box__job-location">Helsinki</div>
                <a class="job-box__hover" href="/tyopaikat/tyo/new-456" data-company="NewCorp"></a>
            </div>
        </html>
        """
        
        details_html = """
        <html>
            <div class="description--jobentry">
                Fresh job description with Docker, Kubernetes, CI/CD
            </div>
        </html>
        """
        
        with patch('job_monitor.scraper.requests.Session') as mock_session_class:
            mock_session = MagicMock()
            
            search_response = Mock()
            search_response.text = search_html
            search_response.raise_for_status = Mock()
            
            details_response = Mock()
            details_response.text = details_html
            details_response.raise_for_status = Mock()
            
            mock_session.get.side_effect = [search_response, details_response]
            mock_session_class.return_value = mock_session
            
            scraper = JobScraper(self.mock_cookies)
            scraper.session = mock_session
            
            # Mock state manager with no cached job
            mock_state_manager = Mock()
            mock_state_manager.get_job.return_value = None
            
            # Search with full_details and state_manager
            jobs = scraper.search_duunitori(
                "test",
                full_details=True,
                limit=1,
                state_manager=mock_state_manager
            )
            
            # Should have made 2 requests (search + details)
            self.assertEqual(mock_session.get.call_count, 2)
            
            # Job should have the freshly fetched description
            self.assertEqual(len(jobs), 1)
            self.assertIn("Docker", jobs[0].description)
            self.assertIn("Kubernetes", jobs[0].description)
    
    def test_partial_cache_scenario(self):
        """Test mixed scenario: some jobs cached, some new."""
        from unittest.mock import patch
        
        search_html = """
        <html>
            <div class="job-box">
                <h3>Cached Job</h3>
                <div class="job-box__job-location">Helsinki</div>
                <a class="job-box__hover" href="/tyopaikat/tyo/cached-1" data-company="CachedCo"></a>
            </div>
            <div class="job-box">
                <h3>New Job</h3>
                <div class="job-box__job-location">Helsinki</div>
                <a class="job-box__hover" href="/tyopaikat/tyo/new-2" data-company="NewCo"></a>
            </div>
        </html>
        """
        
        details_html = """
        <html>
            <div class="description--jobentry">New job details</div>
        </html>
        """
        
        with patch('job_monitor.scraper.requests.Session') as mock_session_class:
            mock_session = MagicMock()
            
            search_response = Mock()
            search_response.text = search_html
            search_response.raise_for_status = Mock()
            
            details_response = Mock()
            details_response.text = details_html
            details_response.raise_for_status = Mock()
            
            mock_session.get.side_effect = [search_response, details_response]
            mock_session_class.return_value = mock_session
            
            scraper = JobScraper(self.mock_cookies)
            scraper.session = mock_session
            
            # Pre-calculate job IDs based on URL hashing (same logic as JobPosting)
            import hashlib
            cached_url = "https://duunitori.fi/tyopaikat/tyo/cached-1"
            new_url = "https://duunitori.fi/tyopaikat/tyo/new-2"
            cached_id = hashlib.md5(cached_url.encode()).hexdigest()[:16]
            new_id = hashlib.md5(new_url.encode()).hexdigest()[:16]
            
            # Mock state manager: first job cached, second not
            def get_job_side_effect(job_id):
                if job_id == cached_id:
                    return JobPosting(
                        id=cached_id,
                        url="https://duunitori.fi/tyopaikat/tyo/cached-1",
                        title="Cached Job",
                        company="CachedCo",
                        location="Helsinki",
                        posted_date=None,
                        discovered_date=datetime.now(),
                        description="Cached description"
                    )
                return None
            
            mock_state_manager = Mock()
            mock_state_manager.get_job.side_effect = get_job_side_effect
            
            jobs = scraper.search_duunitori(
                "test",
                full_details=True,
                limit=2,
                state_manager=mock_state_manager
            )
            
            # Should make 2 requests: search + 1 details (only for new job)
            self.assertEqual(mock_session.get.call_count, 2)
            self.assertEqual(len(jobs), 2)


if __name__ == '__main__':
    unittest.main()
