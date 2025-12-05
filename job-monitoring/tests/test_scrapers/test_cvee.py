"""Tests for CV.ee scraper implementation."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import requests

from job_monitor.scrapers import ScraperRegistry
from job_monitor.scrapers.cvee import CVeeScraper
from job_monitor.schemas import JobPosting


class TestCVeeRegistration:
    """Test CV.ee scraper registration."""
    
    def test_cvee_registered(self):
        """CV.ee scraper should be registered."""
        assert ScraperRegistry.is_registered("cvee")
    
    def test_cvee_metadata(self):
        """CV.ee scraper should have correct metadata."""
        info = ScraperRegistry.get_scraper_info("cvee")
        
        assert info['id'] == "cvee"
        assert info['name'] == "CV.ee"
        assert info['requires_cookies'] is False
        assert info['requires_auth'] is False
        assert "https://cv.ee" in info['base_urls']
        assert info['class'] == "CVeeScraper"


class TestCVeeInitialization:
    """Test CV.ee scraper initialization."""
    
    def test_initialization_no_cookies(self):
        """CV.ee should initialize without cookies."""
        scraper = CVeeScraper(config={})
        
        assert scraper is not None
        assert hasattr(scraper, 'session')
        assert scraper.session.headers['Accept'] == 'application/json'
    
    def test_validate_config(self):
        """CV.ee should always validate config (no requirements)."""
        scraper = CVeeScraper(config={})
        
        assert scraper.validate_config() is True


class TestCVeeSearch:
    """Test CV.ee search functionality."""
    
    @patch('requests.Session.get')
    def test_search_basic_query(self, mock_get):
        """Should handle basic search query."""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'vacancies': [
                {
                    'id': 12345,
                    'positionTitle': 'Python Developer',
                    'employerName': 'TechCorp',
                    'slug': 'python-developer-techcorp',
                    'townId': [1],
                    'publishDate': '2025-01-01',
                    'positionContent': 'Great Python job',
                }
            ],
            'total': 1
        }
        mock_get.return_value = mock_response
        
        scraper = CVeeScraper(config={})
        
        # Mock locations cache before search
        scraper._locations_cache = {1: {'id': 1, 'name': 'Tallinn', 'type': 'city'}}
        results = scraper.search({'keywords': 'python'})
        
        assert len(results) == 1
        assert isinstance(results[0], JobPosting)
        assert results[0].title == 'Python Developer'
        assert results[0].company == 'TechCorp'
        assert results[0].location == 'Tallinn'
        assert results[0].source == 'cvee'
        assert str(results[0].url) == 'https://cv.ee/et/vacancy/12345'
    
    @patch('requests.Session.get')
    def test_search_with_location(self, mock_get):
        """Should resolve location name to ID."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'vacancies': [
                {
                    'id': 123,
                    'positionTitle': 'Developer',
                    'employerName': 'TestCo',
                    'slug': 'dev-test',
                    'townId': [2],
                    'publishDate': '2025-01-01',
                }
            ],
            'total': 1
        }
        mock_get.return_value = mock_response
        
        scraper = CVeeScraper(config={})
        
        # Mock locations
        scraper._locations_cache = {
            1: {'id': 1, 'name': 'Tallinn', 'type': 'city'},
            2: {'id': 2, 'name': 'Tartu', 'type': 'city'},
        }
        
        results = scraper.search({'keywords': 'python', 'location': 'Tartu'})
        
        assert len(results) == 1
        assert results[0].location == 'Tartu'
        
        # Check that API was called with location_ids parameter
        call_args = mock_get.call_args
        assert 'location_ids' in call_args[1]['params']
        assert call_args[1]['params']['location_ids'] == [2]
    
    @patch('requests.Session.get')
    def test_search_no_results(self, mock_get):
        """Should handle empty results."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'vacancies': [], 'total': 0}
        mock_get.return_value = mock_response
        
        scraper = CVeeScraper(config={})
        results = scraper.search({'keywords': 'nonexistent-job'})
        
        assert len(results) == 0
    
    @patch('requests.Session.get')
    def test_search_limit_respected(self, mock_get):
        """Should respect limit parameter."""
        # Create 5 mock vacancies (API respects limit parameter)
        vacancies = [
            {
                'id': i + 1,  # Start from 1 to avoid empty URL
                'positionTitle': f'Job {i}',
                'employerName': 'Company',
                'slug': f'job-{i}',
                'townId': [1],
                'publishDate': '2025-01-01',
            }
            for i in range(5)
        ]
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'vacancies': vacancies, 'total': 10}
        mock_get.return_value = mock_response
        
        scraper = CVeeScraper(config={})
        
        scraper._locations_cache = {1: {'id': 1, 'name': 'Tallinn', 'type': 'city'}}
        results = scraper.search({'keywords': 'test', 'limit': 5})
        
        assert len(results) == 5
    
    @patch('requests.Session.get')
    def test_search_error_handling(self, mock_get):
        """Should handle API errors gracefully."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        scraper = CVeeScraper(config={})
        results = scraper.search({'keywords': 'test'})
        
        assert len(results) == 0


class TestCVeeParsing:
    """Test CV.ee job parsing."""
    
    @patch('requests.Session.get')
    def test_parse_job_complete(self, mock_get):
        """Should parse complete job data."""
        vacancy = {
            'id': 999,
            'positionTitle': 'Senior Python Developer',
            'employerName': 'EstTech OÜ',
            'slug': 'senior-python-developer',
            'townId': [1, 2],
            'publishDate': '2025-01-01T10:00:00',
            'positionContent': 'We are looking for...',
            'salaryFrom': 2000,
            'salaryTo': 3500,
        }
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'vacancies': [vacancy], 'total': 1}
        mock_get.return_value = mock_response
        
        scraper = CVeeScraper(config={})
        
        scraper._locations_cache = {
            1: {'id': 1, 'name': 'Tallinn', 'type': 'city'},
            2: {'id': 2, 'name': 'Tartu', 'type': 'city'},
        }
        
        results = scraper.search({'keywords': 'python'})
        
        assert len(results) == 1
        job = results[0]
        
        assert job.id == '999'
        assert job.title == 'Senior Python Developer'
        assert job.company == 'EstTech OÜ'
        assert job.location == 'Tallinn, Tartu'
        assert job.posted_date == '2025-01-01T10:00:00'
        assert job.description == 'We are looking for...'
        assert job.source == 'cvee'
        assert str(job.url) == 'https://cv.ee/et/vacancy/999'
    
    @patch('requests.Session.get')
    def test_parse_job_missing_optional(self, mock_get):
        """Should handle missing optional fields."""
        vacancy = {
            'id': 888,
            'positionTitle': 'Developer',
            'employerName': 'Company',
            'slug': 'dev',
            'townId': [],
        }
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'vacancies': [vacancy], 'total': 1}
        mock_get.return_value = mock_response
        
        scraper = CVeeScraper(config={})
        results = scraper.search({'keywords': 'test'})
        
        assert len(results) == 1
        job = results[0]
        
        assert job.id == '888'
        assert job.title == 'Developer'
        assert job.location == 'Unknown'
        assert job.posted_date == ''
        assert job.description is None


class TestCVeeLocationResolution:
    """Test CV.ee location resolution."""
    
    @patch('requests.Session.get')
    def test_location_caching(self, mock_get):
        """Should cache location data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {'id': 1, 'name': 'Tallinn', 'type': 'city'},
                {'id': 2, 'name': 'Tartu', 'type': 'city'},
            ]
        }
        mock_get.return_value = mock_response
        
        scraper = CVeeScraper(config={})
        
        # Call _get_locations twice
        locations1 = scraper._get_locations()
        locations2 = scraper._get_locations()
        
        # Should cache results
        assert locations1 is locations2
        assert len(locations1) == 2
        
        # API should be called only once
        assert mock_get.call_count == 1
    
    @patch('requests.Session.get')
    def test_location_resolution_multiple(self, mock_get):
        """Should resolve multiple location IDs."""
        scraper = CVeeScraper(config={})
        
        scraper._locations_cache = {
            1: {'id': 1, 'name': 'Tallinn', 'type': 'city'},
            2: {'id': 2, 'name': 'Tartu', 'type': 'city'},
            3: {'id': 3, 'name': 'Pärnu', 'type': 'city'},
        }
        
        result = scraper._resolve_location([1, 2, 3])
        
        assert result == 'Tallinn, Tartu, Pärnu'
    
    @patch('requests.Session.get')
    def test_location_resolution_unknown(self, mock_get):
        """Should handle unknown location IDs."""
        scraper = CVeeScraper(config={})
        
        scraper._locations_cache = {
            1: {'id': 1, 'name': 'Tallinn', 'type': 'city'},
        }
        
        result = scraper._resolve_location([999])
        
        assert result == 'Unknown'


class TestCVeeSalaryParsing:
    """Test CV.ee salary parsing."""
    
    def test_salary_range(self):
        """Should format salary range."""
        scraper = CVeeScraper(config={})
        
        vacancy = {
            'salary_from': 2000,
            'salary_to': 3000,
            'salary_currency': 'EUR',
            'salary_period': 'month',
        }
        
        result = scraper._parse_salary(vacancy)
        assert result == '2000-3000 EUR/month'
    
    def test_salary_from_only(self):
        """Should format minimum salary only."""
        scraper = CVeeScraper(config={})
        
        vacancy = {
            'salary_from': 2000,
            'salary_currency': 'EUR',
            'salary_period': 'month',
        }
        
        result = scraper._parse_salary(vacancy)
        assert result == 'From 2000 EUR/month'
    
    def test_salary_to_only(self):
        """Should format maximum salary only."""
        scraper = CVeeScraper(config={})
        
        vacancy = {
            'salary_to': 3000,
            'salary_currency': 'EUR',
            'salary_period': 'month',
        }
        
        result = scraper._parse_salary(vacancy)
        assert result == 'Up to 3000 EUR/month'
    
    def test_salary_none(self):
        """Should handle missing salary."""
        scraper = CVeeScraper(config={})
        
        vacancy = {}
        
        result = scraper._parse_salary(vacancy)
        assert result is None


class TestCVeeFromRegistry:
    """Test CV.ee scraper access from registry."""
    
    def test_get_from_registry(self):
        """Should be accessible from registry."""
        scraper = ScraperRegistry.get_scraper("cvee", config={})
        
        assert isinstance(scraper, CVeeScraper)
        assert scraper.SCRAPER_ID == "cvee"
        assert scraper.DISPLAY_NAME == "CV.ee"
