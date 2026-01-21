"""
EthosCrawl: Ethical, AI-Powered Data Collection for the Future

A next-generation web scraping and data collection platform designed for the AI era.
Combines adaptive scraping with cutting-edge AI analysis, privacy-preserving techniques,
and a built-in ethical framework.
"""

__version__ = "0.1.0"
__author__ = "EthosCrawl Team"
__email__ = "hello@ethoscrawl.dev"
__license__ = "AGPL-3.0"

import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PrivacyLevel(Enum):
    """Privacy preservation levels"""
    MINIMAL = "minimal"      # Basic anonymization
    STANDARD = "standard"    # GDPR compliance
    STRICT = "strict"        # Differential privacy
    MAXIMUM = "maximum"      # Federated learning only

class ComplianceStandard(Enum):
    """Supported compliance standards"""
    GDPR = "gdpr"
    CCPA = "ccpa"
    PIPEDA = "pipeda"
    LGPD = "lgpd"
    APA = "apa"

@dataclass
class EthosConfig:
    """Configuration for EthosCrawl"""
    privacy_level: PrivacyLevel = PrivacyLevel.STANDARD
    ethical_standards: List[ComplianceStandard] = None
    ai_enabled: bool = True
    edge_computing: bool = False
    transparency_reports: bool = True
    rate_limit_requests: int = 10  # requests per minute
    user_agent: str = "EthosCrawl/0.1.0 (+https://ethoscrawl.dev)"
    
    def __post_init__(self):
        if self.ethical_standards is None:
            self.ethical_standards = [ComplianceStandard.GDPR]

@dataclass
class ScrapeResult:
    """Result of a scraping operation"""
    data: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    ethical_check: Dict[str, Any]
    privacy_applied: bool
    session_id: str
    timestamp: str

class EthosCrawler:
    """Main EthosCrawl client"""
    
    def __init__(self, config: Optional[EthosConfig] = None):
        self.config = config or EthosConfig()
        self._session_id = None
        self._initialize_components()
        
    def _initialize_components(self):
        """Initialize all components based on configuration"""
        # Import components dynamically to avoid circular imports
        from .core.adaptive_engine import AdaptiveScrapingEngine
        from .core.privacy_layer import PrivacyEngine
        from .core.ethical_framework import EthicalFramework
        
        self.adaptive_engine = AdaptiveScrapingEngine()
        
        # Create PrivacyConfig from privacy_level
        from .core.privacy_layer import PrivacyConfig
        privacy_config = PrivacyConfig(level=self.config.privacy_level)
        self.privacy_engine = PrivacyEngine(privacy_config)
        
        self.ethical_framework = EthicalFramework(
            standards=self.config.ethical_standards
        )
        
        # Initialize AI processor if enabled
        if self.config.ai_enabled:
            try:
                from .integrations.ai_processor import AIContentProcessor
                self.ai_processor = AIContentProcessor()
            except ImportError:
                logger.warning("AI features not installed. Install with 'pip install ethoscrawl[ai]'")
                self.ai_processor = None
                
        # Initialize edge computing if enabled
        if self.config.edge_computing:
            try:
                from .edge.edge_manager import EdgeManager
                self.edge_manager = EdgeManager()
            except ImportError:
                logger.warning("Edge computing features not installed. Install with 'pip install ethoscrawl[edge]'")
                self.edge_manager = None
    
    async def scrape(self, url: str, selectors: List[str], **kwargs) -> ScrapeResult:
        """
        Scrape a URL with ethical considerations
        
        Args:
            url: The URL to scrape
            selectors: CSS/XPath selectors to extract
            **kwargs: Additional options
            
        Returns:
            ScrapeResult with data and metadata
        """
        import uuid
        from datetime import datetime
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        self._session_id = session_id
        
        logger.info(f"Starting scrape session {session_id} for {url}")
        
        # Check ethical compliance
        ethical_check = await self.ethical_framework.check_ethical(
            url=url,
            action="scrape",
            session_id=session_id
        )
        
        if not ethical_check.passed:
            logger.warning(f"Ethical check failed: {ethical_check.violations}")
            # Return empty result with violations
            return ScrapeResult(
                data=[],
                metadata={"url": url, "ethical_check": ethical_check},
                ethical_check=ethical_check.__dict__,
                privacy_applied=False,
                session_id=session_id,
                timestamp=datetime.utcnow().isoformat()
            )
        
        # Perform adaptive scraping
        scrape_result = await self.adaptive_engine.scrape(
            url=url,
            selectors=selectors
        )
        
        # Apply privacy preservation
        if self.config.privacy_level != PrivacyLevel.MINIMAL:
            processed_data = self.privacy_engine.apply_privacy(scrape_result.data)
        else:
            processed_data = scrape_result.data
        
        # Apply AI analysis if enabled
        if self.ai_processor and kwargs.get('analysis_types'):
            analysis_results = await self.ai_processor.analyze_content(
                content=processed_data,
                analysis_types=kwargs['analysis_types']
            )
            metadata = {"analysis": analysis_results}
        else:
            metadata = {}
        
        # Add scraping metadata
        if scrape_result.metadata:
            metadata.update(scrape_result.metadata)
        metadata.update({
            "scraping_success": scrape_result.success,
            "data_points": len(processed_data),
            "adapted": scrape_result.adapted
        })
        
        # Generate transparency report if enabled
        if self.config.transparency_reports:
            from .analytics.transparency_reporter import TransparencyReporter
            reporter = TransparencyReporter()
            transparency_report = await reporter.generate_report(
                session_id=session_id,
                data_sample=processed_data[:3] if processed_data else []
            )
            metadata["transparency_report"] = transparency_report
        
        result = ScrapeResult(
            data=processed_data,
            metadata=metadata,
            ethical_check=ethical_check.__dict__,
            privacy_applied=self.config.privacy_level != PrivacyLevel.MINIMAL,
            session_id=session_id,
            timestamp=datetime.utcnow().isoformat()
        )
        
        logger.info(f"Completed scrape session {session_id}")
        return result
    
    async def monitor(self, url: str, callback, check_interval: int = 300, **kwargs):
        """
        Monitor a URL for changes
        
        Args:
            url: URL to monitor
            callback: Function to call when changes detected
            check_interval: Seconds between checks
            **kwargs: Additional options
        """
        from .core.streaming_engine import RealTimeMonitor
        
        monitor = RealTimeMonitor(
            ethical_framework=self.ethical_framework,
            privacy_engine=self.privacy_engine
        )
        
        await monitor.watch(
            url=url,
            callback=callback,
            check_interval=check_interval,
            **kwargs
        )
    
    async def export(self, data: List[Dict], format: str = "json", **kwargs):
        """
        Export data with privacy preservation
        
        Args:
            data: Data to export
            format: Export format (json, csv, parquet)
            **kwargs: Export options
        """
        from .integrations.exporters import DataExporter
        
        exporter = DataExporter(
            privacy_engine=self.privacy_engine,
            format=format
        )
        
        return await exporter.export(data, **kwargs)

# Create aliases for common imports
__all__ = [
    "EthosCrawler",
    "EthosConfig",
    "ScrapeResult",
    "PrivacyLevel",
    "ComplianceStandard",
    "__version__",
]

# Version info
def version_info() -> Dict[str, str]:
    """Get version information"""
    import sys
    import platform
    
    return {
        "ethoscrawl": __version__,
        "python": sys.version,
        "platform": platform.platform(),
    }

# Quick test function
def test_installation() -> bool:
    """Test if EthosCrawl is properly installed"""
    try:
        import scrapling
        import httpx
        import pydantic
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        return False

if __name__ == "__main__":
    print(f"EthosCrawl v{__version__}")
    print("Ethical, AI-Powered Data Collection for the Future")
    
    if test_installation():
        print("✅ Installation test passed!")
    else:
        print("❌ Installation test failed. Check dependencies.")