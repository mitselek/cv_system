"""Tests for scraper registry and base functionality."""

import pytest
from pathlib import Path
from typing import Any, Dict, List

from job_monitor.scrapers import BaseScraper, ScraperRegistry
from job_monitor.schemas import JobPosting


class MockScraper(BaseScraper):
    """Mock scraper for testing."""
    
    SCRAPER_ID = "mock"
    DISPLAY_NAME = "Mock Scraper"
    REQUIRES_COOKIES = False
    REQUIRES_AUTH = False
    BASE_URLS = ["https://example.com"]
    
    def _setup(self) -> None:
        self.setup_called = True
    
    def search(self, query: Dict[str, Any]) -> List[JobPosting]:
        return []
    
    def validate_config(self) -> bool:
        return True


class CookieRequiringScraper(BaseScraper):
    """Mock scraper that requires cookies."""
    
    SCRAPER_ID = "cookies_required"
    DISPLAY_NAME = "Cookie Scraper"
    REQUIRES_COOKIES = True
    BASE_URLS = ["https://example.com"]
    
    def _setup(self) -> None:
        pass
    
    def search(self, query: Dict[str, Any]) -> List[JobPosting]:
        return []
    
    def validate_config(self) -> bool:
        return self.cookies_file is not None and self.cookies_file.exists()


class TestBaseScraper:
    """Tests for BaseScraper abstract class."""
    
    def test_scraper_requires_id(self):
        """Test that scrapers must define SCRAPER_ID."""
        class NoIDScraper(BaseScraper):
            DISPLAY_NAME = "Test"
            def _setup(self) -> None: pass
            def search(self, query: Dict[str, Any]) -> List[JobPosting]: return []
            def validate_config(self) -> bool: return True
        
        with pytest.raises(ValueError, match="must define SCRAPER_ID"):
            NoIDScraper(config={})
    
    def test_scraper_requires_display_name(self):
        """Test that scrapers must define DISPLAY_NAME."""
        class NoNameScraper(BaseScraper):
            SCRAPER_ID = "test"
            def _setup(self) -> None: pass
            def search(self, query: Dict[str, Any]) -> List[JobPosting]: return []
            def validate_config(self) -> bool: return True
        
        with pytest.raises(ValueError, match="must define DISPLAY_NAME"):
            NoNameScraper(config={})
    
    def test_scraper_initialization(self):
        """Test basic scraper initialization."""
        scraper = MockScraper(config={'test': 'value'})
        
        assert scraper.SCRAPER_ID == "mock"
        assert scraper.DISPLAY_NAME == "Mock Scraper"
        assert scraper.config == {'test': 'value'}
        assert scraper.cookies_file is None
        assert scraper.setup_called is True
    
    def test_scraper_with_cookies_file(self, tmp_path):
        """Test scraper initialization with cookies file."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('[]')
        
        scraper = MockScraper(config={}, cookies_file=cookies_file)
        assert scraper.cookies_file == cookies_file
    
    def test_cookies_required_without_file(self):
        """Test that cookie-requiring scraper fails without file."""
        with pytest.raises(ValueError, match="requires cookies file"):
            CookieRequiringScraper(config={})
    
    def test_cookies_required_with_file(self, tmp_path):
        """Test cookie-requiring scraper with file."""
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('[]')
        
        scraper = CookieRequiringScraper(config={}, cookies_file=cookies_file)
        assert scraper.cookies_file == cookies_file
        assert scraper.validate_config() is True
    
    def test_get_rate_limit_delay_default(self):
        """Test default rate limit delay."""
        scraper = MockScraper(config={})
        assert scraper.get_rate_limit_delay() == 1.5
    
    def test_get_rate_limit_delay_custom(self):
        """Test custom rate limit delay from config."""
        scraper = MockScraper(config={'rate_limit_delay': 3.0})
        assert scraper.get_rate_limit_delay() == 3.0
    
    def test_scraper_repr(self):
        """Test scraper string representation."""
        scraper = MockScraper(config={})
        repr_str = repr(scraper)
        assert "MockScraper" in repr_str
        assert "mock" in repr_str
        assert "Mock Scraper" in repr_str


class TestScraperRegistry:
    """Tests for ScraperRegistry."""
    
    def setup_method(self):
        """Clear registry before each test."""
        ScraperRegistry.clear()
    
    def test_register_scraper(self):
        """Test registering a scraper."""
        ScraperRegistry.register(MockScraper)
        assert ScraperRegistry.is_registered("mock")
    
    def test_register_non_base_scraper(self):
        """Test that non-BaseScraper classes cannot be registered."""
        class NotAScraper:
            pass
        
        with pytest.raises(ValueError, match="must inherit from BaseScraper"):
            ScraperRegistry.register(NotAScraper)  # type: ignore
    
    def test_register_scraper_without_id(self):
        """Test that scrapers without ID cannot be registered."""
        class NoIDScraper(BaseScraper):
            DISPLAY_NAME = "Test"
            def _setup(self) -> None: pass
            def search(self, query: Dict[str, Any]) -> List[JobPosting]: return []
            def validate_config(self) -> bool: return True
        
        with pytest.raises(ValueError, match="must define SCRAPER_ID"):
            ScraperRegistry.register(NoIDScraper)
    
    def test_register_duplicate_scraper_same_class(self):
        """Test registering same scraper twice (should not error)."""
        ScraperRegistry.register(MockScraper)
        ScraperRegistry.register(MockScraper)  # Should not raise
        assert ScraperRegistry.is_registered("mock")
    
    def test_register_duplicate_scraper_different_class(self):
        """Test registering different scraper with same ID."""
        ScraperRegistry.register(MockScraper)
        
        class AnotherMockScraper(BaseScraper):
            SCRAPER_ID = "mock"  # Same ID
            DISPLAY_NAME = "Another Mock"
            def _setup(self) -> None: pass
            def search(self, query: Dict[str, Any]) -> List[JobPosting]: return []
            def validate_config(self) -> bool: return True
        
        with pytest.raises(ValueError, match="already registered"):
            ScraperRegistry.register(AnotherMockScraper)
    
    def test_get_scraper(self):
        """Test getting scraper instance."""
        ScraperRegistry.register(MockScraper)
        
        scraper = ScraperRegistry.get_scraper("mock", config={'test': 'value'})
        
        assert isinstance(scraper, MockScraper)
        assert scraper.config == {'test': 'value'}
    
    def test_get_unknown_scraper(self):
        """Test getting unknown scraper raises error."""
        with pytest.raises(ValueError, match="Unknown scraper: 'unknown'"):
            ScraperRegistry.get_scraper("unknown", config={})
    
    def test_get_scraper_with_cookies(self, tmp_path):
        """Test getting scraper with cookies file."""
        ScraperRegistry.register(CookieRequiringScraper)
        
        cookies_file = tmp_path / "cookies.json"
        cookies_file.write_text('[]')
        
        scraper = ScraperRegistry.get_scraper(
            "cookies_required",
            config={},
            cookies_file=cookies_file
        )
        
        assert scraper.cookies_file == cookies_file
    
    def test_list_scrapers_empty(self):
        """Test listing scrapers when none registered."""
        scrapers = ScraperRegistry.list_scrapers()
        assert scrapers == {}
    
    def test_list_scrapers(self):
        """Test listing registered scrapers."""
        ScraperRegistry.register(MockScraper)
        ScraperRegistry.register(CookieRequiringScraper)
        
        scrapers = ScraperRegistry.list_scrapers()
        
        assert len(scrapers) == 2
        assert "mock" in scrapers
        assert "cookies_required" in scrapers
        assert scrapers["mock"] == MockScraper
        assert scrapers["cookies_required"] == CookieRequiringScraper
    
    def test_is_registered(self):
        """Test checking if scraper is registered."""
        assert not ScraperRegistry.is_registered("mock")
        
        ScraperRegistry.register(MockScraper)
        
        assert ScraperRegistry.is_registered("mock")
        assert not ScraperRegistry.is_registered("unknown")
    
    def test_get_scraper_info(self):
        """Test getting scraper metadata."""
        ScraperRegistry.register(MockScraper)
        
        info = ScraperRegistry.get_scraper_info("mock")
        
        assert info['id'] == "mock"
        assert info['name'] == "Mock Scraper"
        assert info['requires_cookies'] is False
        assert info['requires_auth'] is False
        assert info['base_urls'] == ["https://example.com"]
        assert info['class'] == "MockScraper"
    
    def test_get_scraper_info_unknown(self):
        """Test getting info for unknown scraper."""
        with pytest.raises(ValueError, match="Unknown scraper"):
            ScraperRegistry.get_scraper_info("unknown")
    
    def test_clear_registry(self):
        """Test clearing the registry."""
        ScraperRegistry.register(MockScraper)
        assert ScraperRegistry.is_registered("mock")
        
        ScraperRegistry.clear()
        assert not ScraperRegistry.is_registered("mock")
        assert ScraperRegistry.list_scrapers() == {}
