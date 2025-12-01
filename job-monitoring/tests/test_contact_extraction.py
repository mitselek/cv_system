#!/usr/bin/env python3
"""Tests for contact information extraction."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from job_monitor.scraper import JobScraper


class TestContactExtraction(unittest.TestCase):
    """Test contact information extraction from job portals."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_cookies = Path("/tmp/test_cookies.json")
        self.mock_cookies.write_text('{"test": "cookie"}')
        
    def tearDown(self):
        """Clean up test fixtures."""
        if self.mock_cookies.exists():
            self.mock_cookies.unlink()
    
    @patch('job_monitor.scraper.requests.Session')
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
        
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test", delay=0)
        
        self.assertEqual(contact_info['contact_email'], 'jobs@example.com')
    
    @patch('job_monitor.scraper.requests.Session')
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
        
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test", delay=0)
        
        self.assertEqual(contact_info['contact_phone'], '+358401234567')
    
    @patch('job_monitor.scraper.requests.Session')
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
        
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test", delay=0)
        
        self.assertEqual(contact_info['contact_email'], 'recruiting@company.fi')
    
    @patch('job_monitor.scraper.requests.Session')
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
        
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test", delay=0)
        
        self.assertIsNotNone(contact_info['contact_phone'])
        self.assertIn('040', contact_info['contact_phone'] or '')
    
    @patch('job_monitor.scraper.requests.Session')
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
        
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test", delay=0)
        
        self.assertIsNone(contact_info['contact_email'])
        self.assertIsNone(contact_info['contact_phone'])
        self.assertIsNone(contact_info['contact_name'])
    
    @patch('job_monitor.scraper.requests.Session')
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
        
        scraper = JobScraper(self.mock_cookies)
        scraper.session = mock_session
        
        description, contact_info = scraper._extract_job_details("https://duunitori.fi/test", delay=0)
        
        self.assertEqual(contact_info['contact_email'], 'maria.virtanen@company.fi')
        # Name extraction is heuristic, so just check if something was found
        self.assertIsNotNone(contact_info['contact_name'])


if __name__ == '__main__':
    unittest.main()
