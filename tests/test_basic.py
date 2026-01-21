"""
Basic tests for EthosCrawl.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from ethoscrawl import EthosCrawler, EthosConfig, PrivacyLevel
from ethoscrawl.core.ethical_framework import EthicalFramework, ComplianceStandard


class TestEthosCrawler:
    """Test the main EthosCrawler class."""
    
    def test_initialization(self):
        """Test that EthosCrawler initializes correctly."""
        crawler = EthosCrawler()
        assert crawler is not None
        assert crawler.config is not None
        
    def test_config_initialization(self):
        """Test EthosConfig initialization."""
        config = EthosConfig(
            privacy_level=PrivacyLevel.STRICT,
            ethical_standards=[ComplianceStandard.GDPR],
            requests_per_second=1
        )
        assert config.privacy_level == PrivacyLevel.STRICT
        assert ComplianceStandard.GDPR in config.ethical_standards
        assert config.requests_per_second == 1
        
    def test_privacy_levels(self):
        """Test that privacy levels are accessible."""
        levels = list(PrivacyLevel)
        assert len(levels) == 4  # MINIMAL, STANDARD, STRICT, MAXIMUM
        assert PrivacyLevel.MINIMAL.value == "minimal"
        assert PrivacyLevel.STANDARD.value == "standard"
        assert PrivacyLevel.STRICT.value == "strict"
        assert PrivacyLevel.MAXIMUM.value == "maximum"


class TestEthicalFramework:
    """Test the EthicalFramework class."""
    
    def test_initialization(self):
        """Test EthicalFramework initialization."""
        framework = EthicalFramework()
        assert framework is not None
        
    def test_with_standards(self):
        """Test initialization with specific standards."""
        framework = EthicalFramework(standards=[ComplianceStandard.GDPR, ComplianceStandard.CCPA])
        assert len(framework.standards) == 2
        assert ComplianceStandard.GDPR in framework.standards
        assert ComplianceStandard.CCPA in framework.standards
        
    def test_compliance_standards(self):
        """Test compliance standard values."""
        standards = list(ComplianceStandard)
        assert len(standards) >= 3  # GDPR, CCPA, ROBOTS_TXT at minimum
        assert ComplianceStandard.GDPR.value == "gdpr"
        assert ComplianceStandard.CCPA.value == "ccpa"
        assert ComplianceStandard.ROBOTS_TXT.value == "robots_txt"


@pytest.mark.asyncio
class TestAsyncOperations:
    """Test asynchronous operations."""
    
    async def test_async_scrape_mock(self):
        """Test async scraping with mock."""
        with patch('ethoscrawl.EthosCrawler._scrape_implementation') as mock_scrape:
            mock_scrape.return_value = {
                'data': [{'test': 'data'}],
                'metadata': {'success': True}
            }
            
            crawler = EthosCrawler()
            result = await crawler.scrape(
                url="https://example.com",
                selectors=[".content::text"]
            )
            
            assert result is not None
            assert 'data' in result
            assert 'metadata' in result
            
    async def test_ethical_check_mock(self):
        """Test async ethical check with mock."""
        with patch('ethoscrawl.core.ethical_framework.EthicalFramework._check_implementation') as mock_check:
            mock_check.return_value = {
                'passed': True,
                'compliance_score': 0.9,
                'violations': []
            }
            
            framework = EthicalFramework()
            result = await framework.check_ethical(
                url="https://example.com",
                action="scrape"
            )
            
            assert result.passed is True
            assert result.compliance_score == 0.9
            assert len(result.violations) == 0


class TestCLI:
    """Test CLI functionality."""
    
    def test_cli_import(self):
        """Test that CLI module can be imported."""
        from ethoscrawl import cli
        assert cli is not None
        
    def test_cli_main_exists(self):
        """Test that CLI main function exists."""
        from ethoscrawl.cli import main
        assert callable(main)


def test_import_all():
    """Test that all main modules can be imported."""
    # Core modules
    from ethoscrawl.core import ethical_framework, privacy_layer, adaptive_engine
    assert ethical_framework is not None
    assert privacy_layer is not None
    assert adaptive_engine is not None
    
    # Main package
    from ethoscrawl import simple_crawler
    assert simple_crawler is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])