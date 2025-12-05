"""
Abstract base class for all job scrapers.

This module defines the interface that all job portal scrapers must implement.
Each scraper is a self-contained plugin that handles its own authentication,
rate limiting, and data parsing.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from job_monitor.schemas import JobPosting


class BaseScraper(ABC):
    """Abstract base class for all job scrapers.

    Each scraper implementation must:
    1. Define class-level metadata (SCRAPER_ID, DISPLAY_NAME, etc.)
    2. Implement _setup() for initialization (sessions, cookies, etc.)
    3. Implement search() to execute job searches
    4. Implement validate_config() to check configuration validity

    Example:
        class CVeeScraper(BaseScraper):
            SCRAPER_ID = "cvee"
            DISPLAY_NAME = "CV.ee"
            REQUIRES_COOKIES = False

            def _setup(self) -> None:
                self.session = requests.Session()

            def search(self, query: dict[str, Any]) -> list[JobPosting]:
                # Implementation here
                pass

            def validate_config(self) -> bool:
                return True
    """

    # Class-level metadata - must be defined by subclasses
    SCRAPER_ID: str = ""  # e.g., "cvee", "duunitori"
    DISPLAY_NAME: str = ""  # e.g., "CV.ee", "Duunitori"
    REQUIRES_COOKIES: bool = False
    REQUIRES_AUTH: bool = False
    BASE_URLS: list[str] = []  # e.g., ["https://cv.ee"]

    def __init__(
        self,
        config: dict[str, Any],
        cookies_file: Path | None = None
    ) -> None:
        """Initialize scraper with configuration.

        Args:
            config: Scraper-specific configuration dictionary
            cookies_file: Optional path to cookies JSON file

        Raises:
            ValueError: If required configuration is missing
        """
        if not self.SCRAPER_ID:
            raise ValueError(f"{self.__class__.__name__} must define SCRAPER_ID")
        if not self.DISPLAY_NAME:
            raise ValueError(f"{self.__class__.__name__} must define DISPLAY_NAME")

        self.config = config
        self.cookies_file = cookies_file

        # Validate cookies requirement
        if self.REQUIRES_COOKIES and not cookies_file:
            raise ValueError(
                f"{self.DISPLAY_NAME} requires cookies file but none provided"
            )

        # Initialize scraper
        self._setup()

    @abstractmethod
    def _setup(self) -> None:
        """Setup scraper (sessions, load cookies, initialize clients, etc.).

        Called during __init__. Implement scraper-specific initialization here.

        Example:
            def _setup(self) -> None:
                self.session = requests.Session()
                if self.cookies_file:
                    self._load_cookies()
                self.session.headers.update({...})
        """
        pass

    @abstractmethod
    def search(self, query: dict[str, Any]) -> list[JobPosting]:
        """Search for jobs with given query parameters.

        Args:
            query: Query parameters (keywords, location, limit, etc.)
                   Structure varies by scraper implementation.
                   Common fields:
                   - keywords: str - Search terms
                   - location: str - Location filter
                   - limit: int - Max results to return
                   - offset: int - Pagination offset

        Returns:
            List of JobPosting objects

        Raises:
            Exception: If search fails (should be caught by caller)

        Example:
            def search(self, query: dict[str, Any]) -> list[JobPosting]:
                keywords = query.get('keywords', '')
                limit = query.get('limit', 20)

                response = self.session.get(self.BASE_URLS[0], params={
                    'q': keywords,
                    'limit': limit
                })

                return self._parse_results(response.json())
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate scraper-specific configuration.

        Returns:
            True if configuration is valid, False otherwise

        Example:
            def validate_config(self) -> bool:
                if self.REQUIRES_COOKIES:
                    if not self.cookies_file or not self.cookies_file.exists():
                        return False
                return True
        """
        pass

    def get_rate_limit_delay(self) -> float:
        """Get delay between requests in seconds.

        Returns:
            Delay in seconds (default: 1.5)

        Can be overridden in config:
            config = {'rate_limit_delay': 2.0}
        """
        return self.config.get('rate_limit_delay', 1.5)

    def __repr__(self) -> str:
        """String representation of scraper."""
        return f"{self.__class__.__name__}(id={self.SCRAPER_ID}, name={self.DISPLAY_NAME})"
