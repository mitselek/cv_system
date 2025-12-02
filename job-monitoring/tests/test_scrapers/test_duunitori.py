"""Tests for Duunitori scraper."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from job_monitor.scrapers import ScraperRegistry
from job_monitor.scrapers.duunitori import DuunitoriScraper
from job_monitor.schemas import JobPosting


class TestDuunitoriRegistration:
    """Test that Duunitori scraper is properly registered."""
    
    def test_duunitori_registered(self):
        """Test Duunitori is in registry."""
        assert ScraperRegistry.is_registered("duunitori")
    
    def test_duunitori_metadata(self):
        """Test Duunitori scraper metadata."""
        info = ScraperRegistry.get_scraper_info("duunitori")
        
        assert info['id'] == "duunitori"
        assert info['name'] == "Duunitori"
        assert info['requires_cookies'] is True
        assert info['base_urls'] == ["https://duunitori.fi"]


class TestDuunitoriInitialization:
    """Tests for Duunitori scraper initialization."""
    
    def test_requires_cookies(self):
        """Test that Duunitori requires cookies file."""
        with pytest.raises(ValueError, match="requires cookies file"):
            DuunitoriScraper(config={})
    
    def test_initialization_with_cookies(self, tmp_path):
        """Test initialization with valid cookies file."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('[{"name": "test", "value": "123"}]')
        
        scraper = DuunitoriScraper(config={}, cookies_file=cookies_file)
        
        assert scraper.SCRAPER_ID == "duunitori"
        assert scraper.cookies_file == cookies_file
    
    def test_cookies_missing_file(self, tmp_path):
        """Test error when cookies file doesn't exist."""
        cookies_file = tmp_path / "nonexistent.json"
        
        with pytest.raises(ValueError, match="Cookie file not found"):
            DuunitoriScraper(config={}, cookies_file=cookies_file)
    
    def test_cookies_list_format(self, tmp_path):
        """Test loading cookies in list format."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('''
            [
                {"name": "session", "value": "abc123", "domain": ".duunitori.fi"},
                {"name": "user", "value": "testuser"}
            ]
        ''')
        
        scraper = DuunitoriScraper(config={}, cookies_file=cookies_file)
        
        assert 'session' in scraper.session.cookies
        assert scraper.session.cookies['session'] == 'abc123'
    
    def test_cookies_dict_format(self, tmp_path):
        """Test loading cookies in dict format."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('{"session": "abc123", "user": "testuser"}')
        
        scraper = DuunitoriScraper(config={}, cookies_file=cookies_file)
        
        assert 'session' in scraper.session.cookies
        assert scraper.session.cookies['session'] == 'abc123'
    
    def test_validate_config_valid(self, tmp_path):
        """Test config validation with valid cookies."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('[]')
        
        scraper = DuunitoriScraper(config={}, cookies_file=cookies_file)
        
        assert scraper.validate_config() is True
    
    def test_validate_config_missing_file(self, tmp_path):
        """Test config validation with missing file."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('[]')
        
        scraper = DuunitoriScraper(config={}, cookies_file=cookies_file)
        cookies_file.unlink()  # Delete file
        
        assert scraper.validate_config() is False


class TestDuunitoriSearch:
    """Tests for Duunitori search functionality."""
    
    @pytest.fixture
    def scraper(self, tmp_path):
        """Create scraper instance with mock cookies."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('{"session": "test"}')
        return DuunitoriScraper(config={}, cookies_file=cookies_file)
    
    def test_search_basic_query(self, scraper):
        """Test basic search query structure."""
        mock_response = Mock()
        mock_response.text = '''
            <html><body>
                <div class="job-box">
                    <h3 class="job-box__title">Python Developer</h3>
                    <div class="job-box__job-location">Helsinki</div>
                    <a class="job-box__hover" data-company="TechCorp" href="/tyopaikat/tyo/123">Link</a>
                    <div class="job-box__job-posted">Today</div>
                </div>
            </body></html>
        '''
        mock_response.raise_for_status = Mock()
        
        with patch.object(scraper.session, 'get', return_value=mock_response):
            jobs = scraper.search({'keywords': 'python', 'limit': 10})
        
        assert len(jobs) == 1
        assert jobs[0].title == "Python Developer"
        assert jobs[0].company == "TechCorp"
        assert jobs[0].location == "Helsinki"
        assert jobs[0].source == "Duunitori"
    
    def test_search_with_location(self, scraper):
        """Test search with location filter."""
        with patch.object(scraper.session, 'get') as mock_get:
            mock_get.return_value.text = '<html><body></body></html>'
            mock_get.return_value.raise_for_status = Mock()
            
            scraper.search({'keywords': 'python', 'location': 'Helsinki'})
            
            # Verify location was passed in params
            call_args = mock_get.call_args
            assert call_args[1]['params']['alue'] == 'Helsinki'
    
    def test_search_no_results(self, scraper):
        """Test search with no results."""
        mock_response = Mock()
        mock_response.text = '<html><body></body></html>'
        mock_response.raise_for_status = Mock()
        
        with patch.object(scraper.session, 'get', return_value=mock_response):
            jobs = scraper.search({'keywords': 'nonexistent'})
        
        assert jobs == []
    
    def test_search_limit_respected(self, scraper):
        """Test that result limit is respected."""
        # Create HTML with multiple jobs
        jobs_html = '\n'.join([
            f'''<div class="job-box">
                <h3 class="job-box__title">Job {i}</h3>
                <div class="job-box__job-location">Helsinki</div>
                <a class="job-box__hover" data-company="Company" href="/tyopaikat/tyo/{i}">Link</a>
            </div>'''
            for i in range(10)
        ])
        
        mock_response = Mock()
        mock_response.text = f'<html><body>{jobs_html}</body></html>'
        mock_response.raise_for_status = Mock()
        
        with patch.object(scraper.session, 'get', return_value=mock_response):
            jobs = scraper.search({'keywords': 'python', 'limit': 3})
        
        assert len(jobs) == 3
    
    def test_search_error_handling(self, scraper):
        """Test error handling during search."""
        with patch.object(scraper.session, 'get', side_effect=Exception("Network error")):
            jobs = scraper.search({'keywords': 'python'})
        
        assert jobs == []


class TestDuunitoriParsing:
    """Tests for Duunitori HTML parsing."""
    
    @pytest.fixture
    def scraper(self, tmp_path):
        """Create scraper instance."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('{}')
        return DuunitoriScraper(config={}, cookies_file=cookies_file)
    
    def test_parse_job_complete(self, scraper):
        """Test parsing complete job element."""
        from bs4 import BeautifulSoup
        
        html = '''
            <div class="job-box">
                <h3 class="job-box__title">Senior Python Developer</h3>
                <div class="job-box__job-location">Helsinki, Finland</div>
                <a class="job-box__hover" data-company="Tech Solutions Oy" 
                   href="/tyopaikat/tyo/123456">View job</a>
                <div class="job-box__job-posted">2 days ago</div>
            </div>
        '''
        
        soup = BeautifulSoup(html, 'html.parser')
        elem = soup.select_one('.job-box')
        
        job = scraper._parse_job(elem)
        
        assert job is not None
        assert job.title == "Senior Python Developer"
        assert job.company == "Tech Solutions Oy"
        assert job.location == "Helsinki, Finland"
        assert job.posted_date == "2 days ago"
        assert str(job.url) == "https://duunitori.fi/tyopaikat/tyo/123456"
    
    def test_parse_job_missing_elements(self, scraper):
        """Test parsing job with missing optional elements."""
        from bs4 import BeautifulSoup
        
        html = '''
            <div class="job-box">
                <h3 class="job-box__title">Developer</h3>
                <a class="job-box__hover" href="/tyopaikat/tyo/123">View</a>
            </div>
        '''
        
        soup = BeautifulSoup(html, 'html.parser')
        elem = soup.select_one('.job-box')
        
        job = scraper._parse_job(elem)
        
        assert job is not None
        assert job.title == "Developer"
        assert job.location == "Unknown"
        assert job.company == "Unknown"
    
    def test_parse_job_invalid(self, scraper):
        """Test parsing invalid job element."""
        from bs4 import BeautifulSoup
        
        html = '<div class="job-box"></div>'
        
        soup = BeautifulSoup(html, 'html.parser')
        elem = soup.select_one('.job-box')
        
        job = scraper._parse_job(elem)
        
        assert job is None


class TestDuunitoriFullDetails:
    """Tests for full details extraction."""
    
    @pytest.fixture
    def scraper(self, tmp_path):
        """Create scraper instance."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('{}')
        return DuunitoriScraper(config={}, cookies_file=cookies_file)
    
    def test_extract_job_details(self, scraper):
        """Test extracting job details from page."""
        mock_response = Mock()
        mock_response.text = '''
            <html><body>
                <div class="description--jobentry">
                    Full job description here with requirements and benefits.
                </div>
                <div class="contact-info">
                    <div class="contact-name">Jane Smith</div>
                    <a href="mailto:jane@company.com">jane@company.com</a>
                    <div class="contact-phone">+358 40 123 4567</div>
                </div>
            </body></html>
        '''
        mock_response.raise_for_status = Mock()
        
        with patch.object(scraper.session, 'get', return_value=mock_response):
            description, contact = scraper._extract_job_details("https://duunitori.fi/job/123")
        
        assert "Full job description" in description
        assert contact['contact_name'] == "Jane Smith"
        assert contact['contact_email'] == "jane@company.com"
        assert contact['contact_phone'] == "+358 40 123 4567"
    
    def test_extract_job_details_error(self, scraper):
        """Test error handling in details extraction."""
        with patch.object(scraper.session, 'get', side_effect=Exception("Error")):
            description, contact = scraper._extract_job_details("https://example.com")
        
        assert description is None
        assert contact == {}


class TestDuunitoriFromRegistry:
    """Test Duunitori scraper via registry."""
    
    def test_get_from_registry(self, tmp_path):
        """Test getting Duunitori from registry."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('{}')
        
        scraper = ScraperRegistry.get_scraper(
            "duunitori",
            config={},
            cookies_file=cookies_file
        )
        
        assert isinstance(scraper, DuunitoriScraper)
        assert scraper.SCRAPER_ID == "duunitori"
