"""
Job scraper plugin system.

This module provides a registry for dynamically loading and managing job scrapers.
Each scraper is a plugin that can be enabled/disabled via configuration.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from job_monitor.scrapers.base import BaseScraper


class ScraperRegistry:
    """Central registry for all available scrapers.
    
    The registry maintains a mapping of scraper IDs to scraper classes.
    Scrapers are registered at module import time using the @register decorator
    or explicit register() calls.
    
    Example:
        # Register a scraper
        ScraperRegistry.register(CVeeScraper)
        
        # Get scraper instance
        scraper = ScraperRegistry.get_scraper(
            scraper_id="cvee",
            config={'rate_limit_delay': 2.0}
        )
        
        # List all available scrapers
        scrapers = ScraperRegistry.list_scrapers()
    """
    
    _scrapers: Dict[str, Type[BaseScraper]] = {}
    
    @classmethod
    def register(cls, scraper_class: Type[BaseScraper]) -> None:
        """Register a scraper class.
        
        Args:
            scraper_class: Scraper class that inherits from BaseScraper
        
        Raises:
            ValueError: If scraper_class doesn't inherit from BaseScraper
            ValueError: If scraper with same ID already registered
        
        Example:
            ScraperRegistry.register(CVeeScraper)
        """
        if not issubclass(scraper_class, BaseScraper):
            raise ValueError(
                f"{scraper_class.__name__} must inherit from BaseScraper"
            )
        
        scraper_id = scraper_class.SCRAPER_ID
        if not scraper_id:
            raise ValueError(
                f"{scraper_class.__name__} must define SCRAPER_ID class attribute"
            )
        
        if scraper_id in cls._scrapers:
            existing = cls._scrapers[scraper_id]
            if existing != scraper_class:
                raise ValueError(
                    f"Scraper ID '{scraper_id}' already registered "
                    f"by {existing.__name__}"
                )
        
        cls._scrapers[scraper_id] = scraper_class
    
    @classmethod
    def get_scraper(
        cls,
        scraper_id: str,
        config: Dict[str, Any],
        cookies_file: Optional[Path] = None
    ) -> BaseScraper:
        """Get scraper instance by ID.
        
        Args:
            scraper_id: Scraper identifier (e.g., "cvee", "duunitori")
            config: Scraper-specific configuration dictionary
            cookies_file: Optional path to cookies file
        
        Returns:
            Initialized scraper instance
        
        Raises:
            ValueError: If scraper ID not found in registry
        
        Example:
            scraper = ScraperRegistry.get_scraper(
                scraper_id="cvee",
                config={'rate_limit_delay': 2.0}
            )
            jobs = scraper.search({'keywords': 'python', 'limit': 20})
        """
        if scraper_id not in cls._scrapers:
            available = ', '.join(cls._scrapers.keys()) or 'none'
            raise ValueError(
                f"Unknown scraper: '{scraper_id}'. "
                f"Available scrapers: {available}"
            )
        
        scraper_class = cls._scrapers[scraper_id]
        return scraper_class(config=config, cookies_file=cookies_file)
    
    @classmethod
    def list_scrapers(cls) -> Dict[str, Type[BaseScraper]]:
        """Get all registered scrapers.
        
        Returns:
            Dictionary mapping scraper IDs to scraper classes
        
        Example:
            scrapers = ScraperRegistry.list_scrapers()
            for scraper_id, scraper_class in scrapers.items():
                print(f"{scraper_id}: {scraper_class.DISPLAY_NAME}")
        """
        return cls._scrapers.copy()
    
    @classmethod
    def is_registered(cls, scraper_id: str) -> bool:
        """Check if scraper is registered.
        
        Args:
            scraper_id: Scraper identifier to check
        
        Returns:
            True if scraper is registered, False otherwise
        
        Example:
            if ScraperRegistry.is_registered("cvee"):
                scraper = ScraperRegistry.get_scraper("cvee", {})
        """
        return scraper_id in cls._scrapers
    
    @classmethod
    def get_scraper_info(cls, scraper_id: str) -> Dict[str, Any]:
        """Get metadata about a registered scraper.
        
        Args:
            scraper_id: Scraper identifier
        
        Returns:
            Dictionary with scraper metadata
        
        Raises:
            ValueError: If scraper not found
        
        Example:
            info = ScraperRegistry.get_scraper_info("cvee")
            # {'id': 'cvee', 'name': 'CV.ee', 'requires_cookies': False, ...}
        """
        if scraper_id not in cls._scrapers:
            raise ValueError(f"Unknown scraper: '{scraper_id}'")
        
        scraper_class = cls._scrapers[scraper_id]
        return {
            'id': scraper_class.SCRAPER_ID,
            'name': scraper_class.DISPLAY_NAME,
            'requires_cookies': scraper_class.REQUIRES_COOKIES,
            'requires_auth': scraper_class.REQUIRES_AUTH,
            'base_urls': scraper_class.BASE_URLS,
            'class': scraper_class.__name__,
        }
    
    @classmethod
    def clear(cls) -> None:
        """Clear all registered scrapers.
        
        Primarily for testing purposes.
        """
        cls._scrapers.clear()


# Auto-register scrapers
from job_monitor.scrapers.cvee import CVeeScraper
from job_monitor.scrapers.duunitori import DuunitoriScraper

ScraperRegistry.register(CVeeScraper)
ScraperRegistry.register(DuunitoriScraper)


__all__ = ['BaseScraper', 'ScraperRegistry']
