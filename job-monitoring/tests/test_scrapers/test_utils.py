"""Tests for scraper utility functions."""

import time
import pytest

from job_monitor.scrapers.utils import (
    rate_limit,
    retry,
    cached,
    build_user_agent,
    safe_get,
    format_salary,
)


class TestRateLimit:
    """Tests for rate_limit decorator."""
    
    def test_rate_limit_delays_calls(self):
        """Test that rate limiter adds delays between calls."""
        call_times = []
        
        @rate_limit(delay=0.1)
        def test_func():
            call_times.append(time.time())
        
        test_func()
        test_func()
        test_func()
        
        # Check that calls were spaced out
        assert len(call_times) == 3
        assert call_times[1] - call_times[0] >= 0.1
        assert call_times[2] - call_times[1] >= 0.1
    
    def test_rate_limit_first_call_immediate(self):
        """Test that first call is not delayed."""
        start_time = time.time()
        
        @rate_limit(delay=1.0)
        def test_func():
            pass
        
        test_func()
        elapsed = time.time() - start_time
        
        assert elapsed < 0.1  # First call should be immediate


class TestRetry:
    """Tests for retry decorator."""
    
    def test_retry_success_first_attempt(self):
        """Test successful call on first attempt."""
        call_count = [0]
        
        @retry(max_attempts=3)
        def test_func():
            call_count[0] += 1
            return "success"
        
        result = test_func()
        
        assert result == "success"
        assert call_count[0] == 1
    
    def test_retry_success_after_failures(self):
        """Test success after some failures."""
        call_count = [0]
        
        @retry(max_attempts=3, backoff=0.01)
        def test_func():
            call_count[0] += 1
            if call_count[0] < 3:
                raise ValueError("Not yet")
            return "success"
        
        result = test_func()
        
        assert result == "success"
        assert call_count[0] == 3
    
    def test_retry_max_attempts_exceeded(self):
        """Test that exception is raised after max attempts."""
        call_count = [0]
        
        @retry(max_attempts=3, backoff=0.01)
        def test_func():
            call_count[0] += 1
            raise ValueError("Always fails")
        
        with pytest.raises(ValueError, match="Always fails"):
            test_func()
        
        assert call_count[0] == 3
    
    def test_retry_specific_exceptions(self):
        """Test retry only catches specified exceptions."""
        @retry(max_attempts=3, backoff=0.01, exceptions=(ValueError,))
        def test_func():
            raise KeyError("Wrong exception")
        
        with pytest.raises(KeyError):
            test_func()


class TestCached:
    """Tests for cached decorator."""
    
    def test_cache_returns_same_result(self):
        """Test that cached function returns cached result."""
        call_count = [0]
        
        @cached()
        def test_func(x):
            call_count[0] += 1
            return x * 2
        
        result1 = test_func(5)
        result2 = test_func(5)
        result3 = test_func(5)
        
        assert result1 == result2 == result3 == 10
        assert call_count[0] == 1  # Called only once
    
    def test_cache_different_args(self):
        """Test that different args create different cache entries."""
        call_count = [0]
        
        @cached()
        def test_func(x):
            call_count[0] += 1
            return x * 2
        
        result1 = test_func(5)
        result2 = test_func(10)
        result3 = test_func(5)
        
        assert result1 == 10
        assert result2 == 20
        assert result3 == 10
        assert call_count[0] == 2  # Called for different args
    
    def test_cache_expiry(self):
        """Test that cache expires after TTL."""
        call_count = [0]
        
        @cached(ttl=0.1)  # 0.1 second TTL
        def test_func():
            call_count[0] += 1
            return time.time()
        
        result1 = test_func()
        time.sleep(0.05)
        result2 = test_func()  # Still cached
        time.sleep(0.1)
        result3 = test_func()  # Cache expired
        
        assert result1 == result2
        assert result3 > result2
        assert call_count[0] == 2
    
    def test_cache_clear(self):
        """Test clearing the cache."""
        call_count = [0]
        
        @cached()
        def test_func(x):
            call_count[0] += 1
            return x * 2
        
        result1 = test_func(5)
        test_func.clear_cache()
        result2 = test_func(5)
        
        assert result1 == result2 == 10
        assert call_count[0] == 2  # Called twice due to cache clear


class TestBuildUserAgent:
    """Tests for build_user_agent function."""
    
    def test_default_user_agent(self):
        """Test default user agent."""
        ua = build_user_agent()
        assert "Mozilla/5.0" in ua
        assert "JobMonitor" in ua
    
    def test_custom_scraper_name(self):
        """Test custom scraper name in user agent."""
        ua = build_user_agent("CV.ee Scraper")
        assert "Mozilla/5.0" in ua
        assert "CV.ee Scraper" in ua


class TestSafeGet:
    """Tests for safe_get function."""
    
    def test_safe_get_simple(self):
        """Test getting simple key."""
        data = {'a': 1}
        assert safe_get(data, 'a') == 1
    
    def test_safe_get_nested(self):
        """Test getting nested keys."""
        data = {'a': {'b': {'c': 42}}}
        assert safe_get(data, 'a', 'b', 'c') == 42
    
    def test_safe_get_missing_key(self):
        """Test missing key returns default."""
        data = {'a': 1}
        assert safe_get(data, 'b', default=0) == 0
    
    def test_safe_get_missing_nested(self):
        """Test missing nested key returns default."""
        data = {'a': {'b': 1}}
        assert safe_get(data, 'a', 'c', 'd', default=None) is None
    
    def test_safe_get_non_dict(self):
        """Test non-dict value returns default."""
        data = {'a': 'not a dict'}
        assert safe_get(data, 'a', 'b', default=0) == 0


class TestFormatSalary:
    """Tests for format_salary function."""
    
    def test_format_salary_range(self):
        """Test formatting salary range."""
        result = format_salary(3000, 5000)
        assert result == "€3000-5000"
    
    def test_format_salary_from_only(self):
        """Test formatting minimum salary only."""
        result = format_salary(3000, None)
        assert result == "€3000+"
    
    def test_format_salary_to_only(self):
        """Test formatting maximum salary only."""
        result = format_salary(None, 5000)
        assert result == "up to €5000"
    
    def test_format_salary_none(self):
        """Test formatting with no salary."""
        result = format_salary(None, None)
        assert result is None
    
    def test_format_salary_custom_currency(self):
        """Test custom currency symbol."""
        result = format_salary(3000, 5000, currency="$")
        assert result == "$3000-5000"
    
    def test_format_salary_float_conversion(self):
        """Test that floats are converted to ints."""
        result = format_salary(3500.75, 5000.99)
        assert result == "€3500-5000"
