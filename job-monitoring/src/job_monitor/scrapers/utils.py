"""
Utility functions for job scrapers.

Common functionality used across multiple scrapers:
- Rate limiting
- Retry logic
- Caching
- HTTP helpers
"""

import functools
import time
from collections.abc import Callable
from typing import Any, Protocol, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


class CachedFunction(Protocol):
    """Protocol for cached function with clear_cache method."""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call the cached function."""
        ...

    def clear_cache(self) -> None:
        """Clear the function's cache."""
        ...


def rate_limit(delay: float = 1.5) -> Callable[[F], F]:
    """Decorator to rate limit function calls.

    Args:
        delay: Minimum delay in seconds between calls

    Example:
        @rate_limit(delay=2.0)
        def make_request(url: str) -> Response:
            return requests.get(url)
    """
    def decorator(func: F) -> F:
        last_called: list[float] = [0.0]

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            elapsed = time.time() - last_called[0]
            if elapsed < delay:
                time.sleep(delay - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result

        return wrapper  # type: ignore
    return decorator


def retry(
    max_attempts: int = 3,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable[[F], F]:
    """Decorator to retry function calls on failure.

    Args:
        max_attempts: Maximum number of attempts
        backoff: Exponential backoff multiplier
        exceptions: Tuple of exceptions to catch and retry

    Example:
        @retry(max_attempts=3, backoff=2.0)
        def fetch_data(url: str) -> dict:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    wait_time = backoff ** attempt
                    print(
                        f"⚠️  Attempt {attempt}/{max_attempts} failed: {e}. "
                        f"Retrying in {wait_time:.1f}s..."
                    )
                    time.sleep(wait_time)
                    attempt += 1
            return None  # Should never reach here

        return wrapper  # type: ignore
    return decorator


def cached(ttl: float | None = None) -> Callable[[Callable[..., Any]], CachedFunction]:
    """Decorator to cache function results.

    Args:
        ttl: Time to live in seconds (None = cache forever)

    Example:
        @cached(ttl=3600)  # Cache for 1 hour
        def get_locations() -> dict:
            return requests.get('/api/locations').json()
    """
    def decorator(func: Callable[..., Any]) -> CachedFunction:
        cache: dict[tuple, tuple[Any, float]] = {}

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create cache key from arguments
            key = (args, tuple(sorted(kwargs.items())))

            # Check if cached and not expired
            if key in cache:
                result, cached_time = cache[key]
                if ttl is None or (time.time() - cached_time) < ttl:
                    return result

            # Call function and cache result
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result

        # Add cache clearing method
        wrapper.clear_cache = cache.clear  # type: ignore

        return wrapper  # type: ignore
    return decorator


def build_user_agent(scraper_name: str = "JobMonitor") -> str:
    """Build a user agent string for HTTP requests.

    Args:
        scraper_name: Name of the scraper

    Returns:
        User agent string

    Example:
        user_agent = build_user_agent("CV.ee Scraper")
    """
    return (
        f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        f"(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 "
        f"({scraper_name})"
    )


def safe_get(data: dict, *keys: str, default: Any = None) -> Any:
    """Safely get nested dictionary value.

    Args:
        data: Dictionary to search
        *keys: Keys to traverse
        default: Default value if not found

    Returns:
        Value at nested key or default

    Example:
        value = safe_get(data, 'job', 'salary', 'from', default=0)
        # Equivalent to: data.get('job', {}).get('salary', {}).get('from', 0)
    """
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, default)
        else:
            return default
    return data


def format_salary(
    salary_from: float | None,
    salary_to: float | None,
    currency: str = "€"
) -> str | None:
    """Format salary range as string.

    Args:
        salary_from: Minimum salary
        salary_to: Maximum salary
        currency: Currency symbol

    Returns:
        Formatted salary string or None

    Example:
        format_salary(3000, 5000)  # "€3000-5000"
        format_salary(3000, None)  # "€3000+"
        format_salary(None, None)  # None
    """
    if salary_from and salary_to:
        return f"{currency}{int(salary_from)}-{int(salary_to)}"
    elif salary_from:
        return f"{currency}{int(salary_from)}+"
    elif salary_to:
        return f"up to {currency}{int(salary_to)}"
    return None


__all__ = [
    'rate_limit',
    'retry',
    'cached',
    'build_user_agent',
    'safe_get',
    'format_salary',
]
