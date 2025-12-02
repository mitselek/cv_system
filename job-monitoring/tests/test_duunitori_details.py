#!/usr/bin/env python3
"""Tests for Duunitori scraper's detail extraction functionality.

Tests cover:
- Full job description extraction
- Contact information extraction (email, phone, name)
- Caching mechanism to avoid redundant requests
"""

import unittest
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from unittest.mock import Mock, MagicMock, patch

from job_monitor.schemas import JobPosting
from job_monitor.scrapers.duunitori import DuunitoriScraper


class TestDuunitoriDetailExtraction(unittest.TestCase):
    """Test description and contact info extraction from Duunitori."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cookies_file = Path("/tmp/test_cookies_duunitori.json")
        self.cookies_file.write_text('{"test": "cookie"}')
        self.config: Dict[str, Any] = {}
        
    def tearDown(self):
        """Clean up test fixtures."""
        if self.cookies_file.exists():
            self.cookies_file.unlink()
    
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_extract_job_details_with_description(self, mock_session_class):
        """Test successful description extraction."""
        mock_html = """
        <html>
            <div class="description--jobentry">
                <strong>Your Impact</strong><br />
                As a business analyst, you will work with Python, SQL, 
                and agile methodologies in our Helsinki office.
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test")
        
        self.assertIsNotNone(description)
        self.assertIn("business analyst", description)
        self.assertIn("Python", description)
        self.assertIn("SQL", description)
        self.assertIsInstance(contact_info, dict)
    
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_extract_job_details_no_description(self, mock_session_class):
        """Test extraction when description element is missing."""
        mock_html = "<html><body>No description here</body></html>"
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test")
        
        self.assertIsNone(description)
        self.assertIsInstance(contact_info, dict)
    
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_extract_job_details_network_error(self, mock_session_class):
        """Test extraction handles network errors gracefully."""
        mock_session = MagicMock()
        mock_session.get.side_effect = Exception("Network error")
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test")
        
        self.assertIsNone(description)
        self.assertEqual(contact_info, {})


class TestDuunitoriContactExtraction(unittest.TestCase):
    """Test contact information extraction from Duunitori job postings."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cookies_file = Path("/tmp/test_cookies_contact.json")
        self.cookies_file.write_text('{"test": "cookie"}')
        self.config: Dict[str, Any] = {}
        
    def tearDown(self):
        """Clean up test fixtures."""
        if self.cookies_file.exists():
            self.cookies_file.unlink()
    
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_extract_contact_email_from_mailto(self, mock_session_class):
        """Test extraction of email from mailto: link."""
        mock_html = """
        <html>
            <div class="description--jobentry">
                <p>Contact us at <a href="mailto:jobs@example.com">jobs@example.com</a></p>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test")
        
        self.assertEqual(contact_info['contact_email'], 'jobs@example.com')
    
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_extract_phone_from_tel(self, mock_session_class):
        """Test extraction of phone from tel: link."""
        mock_html = """
        <html>
            <div class="description--jobentry">
                <p>Call us: <a href="tel:+358401234567">+358 40 123 4567</a></p>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test")
        
        self.assertEqual(contact_info['contact_phone'], '+358401234567')
    
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_extract_email_from_text(self, mock_session_class):
        """Test extraction of email from plain text."""
        mock_html = """
        <html>
            <div class="description--jobentry">
                <p>Send your application to recruiting@company.fi</p>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test")
        
        self.assertEqual(contact_info['contact_email'], 'recruiting@company.fi')
    
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_extract_finnish_phone_from_text(self, mock_session_class):
        """Test extraction of Finnish phone number from text."""
        mock_html = """
        <html>
            <div class="description--jobentry">
                <p>For more info, call 040 123 4567</p>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test")
        
        self.assertIsNotNone(contact_info['contact_phone'])
        self.assertIn('040', contact_info['contact_phone'] or '')
    
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_no_contact_info_available(self, mock_session_class):
        """Test when no contact information is available."""
        mock_html = """
        <html>
            <div class="description--jobentry">
                <p>We are hiring for various positions.</p>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test")
        
        self.assertIsNone(contact_info['contact_email'])
        self.assertIsNone(contact_info['contact_phone'])
        self.assertIsNone(contact_info['contact_name'])
    
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_extract_contact_name_near_email(self, mock_session_class):
        """Test extraction of contact person name near email."""
        mock_html = """
        <html>
            <div class="description--jobentry">
                <p>Contact Person</p>
                <p>Maria Virtanen</p>
                <p>HR Manager</p>
                <p>Email: maria.virtanen@company.fi</p>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test")
        
        self.assertEqual(contact_info['contact_email'], 'maria.virtanen@company.fi')
        # Name extraction is heuristic, so just check if something was found
        self.assertIsNotNone(contact_info['contact_name'])


class TestDuunitoriCaching(unittest.TestCase):
    """Test description caching to avoid redundant requests."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cookies_file = Path("/tmp/test_cookies_cache.json")
        self.cookies_file.write_text('{"test": "cookie"}')
        self.config: Dict[str, Any] = {}
        
    def tearDown(self):
        """Clean up test fixtures."""
        if self.cookies_file.exists():
            self.cookies_file.unlink()
    
    @patch('job_monitor.scrapers.duunitori.time.sleep')
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_cached_descriptions_not_refetched(self, mock_session_class, mock_sleep):
        """Test that cached descriptions are reused, not re-fetched."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        # Create jobs that need details
        job1 = JobPosting(
            url="https://duunitori.fi/tyopaikat/tyo/test-123",
            title="Test Job 1",
            company="TestCorp",
            location="Helsinki",
            posted_date=None,
            discovered_date=datetime.now(),
            source="Duunitori"
        )
        
        job2 = JobPosting(
            url="https://duunitori.fi/tyopaikat/tyo/test-456",
            title="Test Job 2",
            company="TestCorp",
            location="Helsinki",
            posted_date=None,
            discovered_date=datetime.now(),
            source="Duunitori"
        )
        
        jobs = [job1, job2]
        
        # Mock state manager with cached description for job1
        mock_state_manager = Mock()
        cached_job1 = JobPosting(
            url="https://duunitori.fi/tyopaikat/tyo/test-123",
            title="Test Job 1",
            company="TestCorp",
            location="Helsinki",
            posted_date=None,
            discovered_date=datetime.now(),
            description="Cached description with Python, SQL keywords",
            source="Duunitori"
        )
        
        def get_job_side_effect(job_id):
            if job_id == job1.id:
                return cached_job1
            return None
        
        mock_state_manager.get_job.side_effect = get_job_side_effect
        
        # Mock the details fetch for job2
        mock_html = '<div class="description--jobentry">Fresh description</div>'
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        mock_session.get.return_value = mock_response
        
        # Extract full details
        scraper._extract_full_details(jobs, mock_state_manager)
        
        # Job1 should have cached description
        self.assertEqual(job1.description, "Cached description with Python, SQL keywords")
        
        # Job2 should have fresh description
        self.assertEqual(job2.description, "Fresh description")
        
        # Should only make 1 HTTP request (for job2), not 2
        self.assertEqual(mock_session.get.call_count, 1)
    
    @patch('job_monitor.scrapers.duunitori.time.sleep')
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_no_cache_fetches_all_descriptions(self, mock_session_class, mock_sleep):
        """Test that without cache, all descriptions are fetched."""
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        # Create jobs
        job1 = JobPosting(
            url="https://duunitori.fi/tyopaikat/tyo/test-123",
            title="Test Job 1",
            company="TestCorp",
            location="Helsinki",
            posted_date=None,
            discovered_date=datetime.now(),
            source="Duunitori"
        )
        
        job2 = JobPosting(
            url="https://duunitori.fi/tyopaikat/tyo/test-456",
            title="Test Job 2",
            company="TestCorp",
            location="Helsinki",
            posted_date=None,
            discovered_date=datetime.now(),
            source="Duunitori"
        )
        
        jobs = [job1, job2]
        
        # Mock state manager with no cached jobs
        mock_state_manager = Mock()
        mock_state_manager.get_job.return_value = None
        
        # Mock details fetch
        mock_html = '<div class="description--jobentry">Description</div>'
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        mock_session.get.return_value = mock_response
        
        # Extract full details
        scraper._extract_full_details(jobs, mock_state_manager)
        
        # Both jobs should have descriptions
        self.assertIsNotNone(job1.description)
        self.assertIsNotNone(job2.description)
        
        # Should make 2 HTTP requests (one for each job)
        self.assertEqual(mock_session.get.call_count, 2)
    
    @patch('job_monitor.scrapers.duunitori.time.sleep')
    @patch('job_monitor.scrapers.duunitori.requests.Session')
    def test_extract_full_details_updates_contact_info(self, mock_session_class, mock_sleep):
        """Test that _extract_full_details updates contact information."""
        mock_html = """
        <html>
            <div class="description--jobentry">
                <p>Description text</p>
                <p>Email: contact@example.com</p>
                <p>Phone: 040 123 4567</p>
            </div>
        </html>
        """
        
        mock_response = Mock()
        mock_response.text = mock_html
        mock_response.raise_for_status = Mock()
        
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        scraper = DuunitoriScraper(self.config, self.cookies_file)
        scraper.session = mock_session
        
        # Create job
        job = JobPosting(
            url="https://duunitori.fi/tyopaikat/tyo/test-123",
            title="Test Job",
            company="TestCorp",
            location="Helsinki",
            posted_date=None,
            discovered_date=datetime.now(),
            source="Duunitori"
        )
        
        jobs = [job]
        
        # Extract with no cache
        scraper._extract_full_details(jobs, state_manager=None)
        
        # Verify contact info was extracted
        self.assertIsNotNone(job.description)
        self.assertEqual(job.contact_email, 'contact@example.com')
        self.assertIsNotNone(job.contact_phone)


if __name__ == '__main__':
    unittest.main()
