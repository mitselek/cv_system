#!/usr/bin/env python3
"""Tests for job description extraction feature."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from job_monitor.scraper import JobScraper


class TestDescriptionExtraction(unittest.TestCase):
    """Test description extraction from job portals."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock cookies file
        self.mock_cookies = Path("/tmp/test_cookies.json")
        self.mock_cookies.write_text('{"test": "cookie"}')
        
    def tearDown(self):
        """Clean up test fixtures."""
        if self.mock_cookies.exists():
            self.mock_cookies.unlink()
    
    @patch('job_monitor.scraper.requests.Session')
    def test_extract_job_details_success(self, mock_session_class):
        """Test successful description extraction."""
        # Mock HTML response with description
        mock_html = """
        <html>
            <div class="description--jobentry">
                <strong>Your Impact</strong><br />
                As a business analyst, you will join a client service team.
                You'll work with data analysis, system design, and agile methodologies.
            </div>
        </html>
        """
        
        # Setup mocks
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        # Test extraction
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test", delay=0)
        
        # Assertions
        self.assertIsNotNone(description)
        self.assertIn("business analyst", description)
        self.assertIn("data analysis", description)
        self.assertIn("agile", description)
        self.assertIsInstance(contact_info, dict)
        mock_session.get.assert_called_once()
    
    @patch('job_monitor.scraper.requests.Session')
    def test_extract_job_details_no_description(self, mock_session_class):
        """Test extraction when description element is missing."""
        mock_html = "<html><body>No description here</body></html>"
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test", delay=0)
        
        self.assertIsNone(description)
        self.assertIsInstance(contact_info, dict)
    
    @patch('job_monitor.scraper.requests.Session')
    def test_extract_job_details_network_error(self, mock_session_class):
        """Test extraction handles network errors gracefully."""
        mock_session = MagicMock()
        mock_session.get.side_effect = Exception("Network error")
        mock_session_class.return_value = mock_session
        
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test", delay=0)
        
        self.assertIsNone(description)
        self.assertEqual(contact_info, {})
        self.assertEqual(contact_info, {})
    
    @patch('job_monitor.scraper.time.sleep')
    @patch('job_monitor.scraper.requests.Session')
    def test_extract_respects_rate_limiting(self, mock_session_class, mock_sleep):
        """Test that extraction respects rate limiting delay."""
        mock_html = '<div class="description--jobentry">Test</div>'
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        scraper._extract_job_details("https://duunitori.fi/test", delay=2.5)
        
        # Should have called sleep with delay parameter
        mock_sleep.assert_called_once_with(2.5)
    
    @patch('job_monitor.scraper.requests.Session')
    def test_search_duunitori_with_full_details(self, mock_session_class):
        """Test search with full_details flag extracts descriptions."""
        # Mock search results page
        search_html = """
        <html>
            <div class="job-box">
                <h3 class="job-box__title">Business Analyst</h3>
                <div class="job-box__job-location">Helsinki</div>
                <a class="job-box__hover" href="/tyopaikat/tyo/test-123" data-company="TestCorp"></a>
            </div>
        </html>
        """
        
        # Mock job details page
        details_html = """
        <html>
            <div class="description--jobentry">
                Great opportunity for business analyst with Python, SQL, and agile experience.
            </div>
        </html>
        """
        
        mock_session = MagicMock()
        
        # First call: search results
        # Subsequent calls: job details
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
        
        # Search with full_details=True
        jobs = scraper.search_duunitori("business analyst", full_details=True, limit=1)
        
        # Assertions
        self.assertEqual(len(jobs), 1)
        self.assertIsNotNone(jobs[0].description)
        self.assertIn("Python", jobs[0].description)
        self.assertIn("agile", jobs[0].description)
        
        # Should have made 2 requests: search + details
        self.assertEqual(mock_session.get.call_count, 2)
    
    @patch('job_monitor.scraper.requests.Session')
    def test_search_duunitori_without_full_details(self, mock_session_class):
        """Test search without full_details flag skips description extraction."""
        search_html = """
        <html>
            <div class="job-box">
                <h3 class="job-box__title">Business Analyst</h3>
                <div class="job-box__job-location">Helsinki</div>
                <a class="job-box__hover" href="/tyopaikat/tyo/test-123" data-company="TestCorp"></a>
            </div>
        </html>
        """
        
        mock_session = MagicMock()
        search_response = Mock()
        search_response.text = search_html
        search_response.raise_for_status = Mock()
        mock_session.get.return_value = search_response
        mock_session_class.return_value = mock_session
        
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        # Search with full_details=False (default)
        jobs = scraper.search_duunitori("business analyst", full_details=False, limit=1)
        
        # Assertions
        self.assertEqual(len(jobs), 1)
        self.assertIsNone(jobs[0].description)
        
        # Should have made only 1 request: search
        self.assertEqual(mock_session.get.call_count, 1)


if __name__ == '__main__':
    unittest.main()
