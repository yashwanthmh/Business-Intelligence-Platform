"""
Rate Limiter Module
Manages API request rate limiting to stay within provider limits
"""

import time
import threading
from collections import deque
from typing import Optional


class RateLimiter:
    """
    Token bucket rate limiter for API requests.
    Ensures requests stay within provider limits (requests per minute).
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton pattern to ensure one rate limiter across the app"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Groq free tier limits: 30 requests per minute
        # We'll use 25 to have some buffer
        self.requests_per_minute = 25
        self.window_seconds = 60

        # Track request timestamps
        self.request_times = deque()
        self.lock = threading.Lock()

        self._initialized = True

    def _clean_old_requests(self):
        """Remove requests older than the window"""
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds

        while self.request_times and self.request_times[0] < cutoff_time:
            self.request_times.popleft()

    def get_wait_time(self) -> float:
        """
        Calculate how long to wait before making a request.
        Returns 0 if we can make a request immediately.
        """
        with self.lock:
            self._clean_old_requests()

            if len(self.request_times) < self.requests_per_minute:
                return 0.0

            # Need to wait until the oldest request expires
            oldest_request = self.request_times[0]
            wait_time = (oldest_request + self.window_seconds) - time.time()
            return max(0.0, wait_time)

    def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire permission to make a request.
        Blocks until a slot is available or timeout is reached.

        Args:
            timeout: Maximum time to wait in seconds. None means wait forever.

        Returns:
            True if permission was acquired, False if timeout was reached.
        """
        start_time = time.time()

        while True:
            wait_time = self.get_wait_time()

            if wait_time == 0:
                with self.lock:
                    # Double-check after acquiring lock
                    self._clean_old_requests()
                    if len(self.request_times) < self.requests_per_minute:
                        self.request_times.append(time.time())
                        return True

            # Check timeout
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed + wait_time > timeout:
                    return False

            # Wait before trying again
            if wait_time > 0:
                time.sleep(min(wait_time, 1.0))  # Sleep in 1-second chunks max

    def get_current_usage(self) -> dict:
        """Get current rate limit usage stats"""
        with self.lock:
            self._clean_old_requests()
            return {
                "requests_in_window": len(self.request_times),
                "limit": self.requests_per_minute,
                "available": self.requests_per_minute - len(self.request_times),
                "window_seconds": self.window_seconds
            }


# Global rate limiter instance
rate_limiter = RateLimiter()
