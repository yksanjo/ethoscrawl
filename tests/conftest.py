"""
Pytest configuration and fixtures for EthosCrawl tests.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from ethoscrawl import EthosCrawler, EthosConfig
from ethoscrawl.core.ethical_framework import EthicalFramework


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_response():
    """Create a mock HTTP response."""
    mock = MagicMock()
    mock.status_code = 200
    mock.text = """
    <html>
        <body>
            <div class="content">Test Content 1</div>
            <div class="content">Test Content 2</div>
            <div class="content">Test Content 3</div>
        </body>
    </html>
    """
    mock.headers = {'Content-Type': 'text/html'}
    return mock


@pytest.fixture
def basic_config():
    """Create a basic EthosConfig for testing."""
    return EthosConfig(
        privacy_level="standard",
        ethical_standards=["gdpr"],
        requests_per_second=1,
        timeout=10
    )


@pytest.fixture
def crawler(basic_config):
    """Create an EthosCrawler instance for testing."""
    return EthosCrawler(config=basic_config)


@pytest.fixture
def ethical_framework():
    """Create an EthicalFramework instance for testing."""
    return EthicalFramework(standards=["gdpr", "robots_txt"])


@pytest.fixture
def mock_website_content():
    """Mock website content for testing."""
    return {
        "simple": """
        <html>
            <body>
                <h1>Test Page</h1>
                <div class="article">
                    <h2>Article 1</h2>
                    <p>Content 1</p>
                </div>
                <div class="article">
                    <h2>Article 2</h2>
                    <p>Content 2</p>
                </div>
            </body>
        </html>
        """,
        "with_data": """
        <html>
            <body>
                <table>
                    <tr><td>Name</td><td>Age</td><td>Email</td></tr>
                    <tr><td>John Doe</td><td>30</td><td>john@example.com</td></tr>
                    <tr><td>Jane Smith</td><td>25</td><td>jane@example.com</td></tr>
                </table>
            </body>
        </html>
        """
    }


@pytest.fixture
def test_urls():
    """Test URLs for different scenarios."""
    return {
        "public": "https://httpbin.org/html",
        "quotes": "https://quotes.toscrape.com/",
        "books": "https://books.toscrape.com/",
        "test": "https://example.com"
    }


@pytest.fixture
def mock_async_client():
    """Mock async HTTP client."""
    mock = AsyncMock()
    
    # Mock successful response
    successful_response = MagicMock()
    successful_response.status = 200
    successful_response.text.return_value = "<html><body>Test</body></html>"
    
    # Mock error response
    error_response = MagicMock()
    error_response.status = 404
    
    mock.get.return_value = successful_response
    return mock


@pytest.fixture
def privacy_test_data():
    """Test data for privacy layer tests."""
    return [
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "ip_address": "192.168.1.100",
            "location": "New York, NY",
            "age": 30
        },
        {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "ip_address": "10.0.0.50",
            "location": "Los Angeles, CA",
            "age": 25
        }
    ]


@pytest.fixture
def rate_limit_test_cases():
    """Test cases for rate limiting."""
    return [
        {"rate": 1, "requests": 5, "expected_min_time": 4},  # 1 req/sec, 5 requests = ~4 seconds min
        {"rate": 2, "requests": 10, "expected_min_time": 4.5},  # 2 req/sec, 10 requests = ~4.5 seconds min
        {"rate": 0.5, "requests": 3, "expected_min_time": 4},  # 0.5 req/sec, 3 requests = ~4 seconds min
    ]


# Markers for different test types
def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "network: marks tests that require network access"
    )
    config.addinivalue_line(
        "markers", "privacy: marks tests for privacy features"
    )
    config.addinivalue_line(
        "markers", "ethics: marks tests for ethical framework"
    )
    config.addinivalue_line(
        "markers", "async_test: marks tests that use async/await"
    )


# Skip network tests by default unless explicitly requested
def pytest_collection_modifyitems(config, items):
    """Skip network tests unless --network flag is provided."""
    skip_network = pytest.mark.skip(reason="need --network option to run")
    skip_slow = pytest.mark.skip(reason="test is too slow for regular runs")
    
    for item in items:
        if "network" in item.keywords and not config.getoption("--network"):
            item.add_marker(skip_network)
        if "slow" in item.keywords and not config.getoption("--slow"):
            item.add_marker(skip_slow)


# Command line options
def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--network",
        action="store_true",
        default=False,
        help="run tests that require network access"
    )
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="run slow tests"
    )
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests"
    )