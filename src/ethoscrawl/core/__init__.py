"""
Core modules for EthosCrawl

This package contains the core functionality for ethical web scraping:
- Adaptive scraping engine
- Privacy preservation layer
- Ethical framework
"""

from .adaptive_engine import AdaptiveScrapingEngine
from .privacy_layer import PrivacyEngine, PrivacyLevel
from .ethical_framework import EthicalFramework, ComplianceStandard, EthicalAction

__all__ = [
    "AdaptiveScrapingEngine",
    "PrivacyEngine",
    "PrivacyLevel",
    "EthicalFramework",
    "ComplianceStandard",
    "EthicalAction",
]