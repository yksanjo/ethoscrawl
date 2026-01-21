#!/usr/bin/env python3
"""
Test the core EthosCrawl modules
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import asyncio
import json
from ethoscrawl.core.adaptive_engine import AdaptiveScrapingEngine
from ethoscrawl.core.privacy_layer import PrivacyEngine, PrivacyLevel, PrivacyConfig
# from ethoscrawl.core.ethical_framework import EthicalFramework, ComplianceStandard, EthicalAction

async def test_adaptive_engine():
    """Test the adaptive scraping engine"""
    print("Testing AdaptiveScrapingEngine...")
    
    engine = AdaptiveScrapingEngine()
    
    # Test scraping a simple website
    result = await engine.scrape(
        url="https://quotes.toscrape.com/",
        selectors=[".quote", ".text::text", ".author::text"]
    )
    
    print(f"Success: {result.success}")
    print(f"Data points: {len(result.data)}")
    
    if result.data:
        print("\nSample data:")
        for i, item in enumerate(result.data[:3], 1):
            print(f"  {i}. {item.get('text', 'No text')}")
    
    stats = engine.get_stats()
    print(f"\nEngine stats: {stats}")
    
    return result.success

def test_privacy_engine():
    """Test the privacy engine"""
    print("\nTesting PrivacyEngine...")
    
    # Sample data with PII
    sample_data = {
        "user": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-123-4567",
            "age": 35,
            "salary": 75000.50
        },
        "metadata": {
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0"
        }
    }
    
    print("Original data:")
    print(json.dumps(sample_data, indent=2))
    
    # Test different privacy levels
    for level in PrivacyLevel:
        print(f"\n--- {level.value.upper()} Privacy ---")
        config = PrivacyConfig(level=level)
        engine = PrivacyEngine(config)
        
        anonymized = engine.apply_privacy(sample_data)
        print(json.dumps(anonymized, indent=2))
        
        report = engine.get_privacy_report(sample_data, anonymized)
        print(f"Privacy report: {report}")
    
    return True

# async def test_ethical_framework():
#     """Test the ethical framework"""
#     print("\nTesting EthicalFramework...")
    
#     framework = EthicalFramework(
#         standards=[ComplianceStandard.GDPR, ComplianceStandard.CCPA],
#         respect_robots_txt=True
#     )
    
#     # Test ethical check
#     result = await framework.check_ethical(
#         url="https://example.com",
#         action=EthicalAction.SCRAPE,
#         data_types=["contact_info", "demographics"]
#     )
    
#     print(f"Ethical check passed: {result.passed}")
#     print(f"Compliance score: {result.compliance_score}")
    
#     if result.warnings:
#         print("\nWarnings:")
#         for warning in result.warnings:
#             print(f"  - {warning}")
    
#     if result.recommendations:
#         print("\nRecommendations:")
#         for rec in result.recommendations:
#             print(f"  - {rec}")
    
#     return result.passed

async def main():
    """Run all tests"""
    print("=" * 60)
    print("EthosCrawl Core Modules Test")
    print("=" * 60)
    
    results = []
    
    # Test adaptive engine
    try:
        adaptive_result = await test_adaptive_engine()
        results.append(("Adaptive Engine", adaptive_result))
    except Exception as e:
        print(f"Adaptive Engine test failed: {e}")
        results.append(("Adaptive Engine", False))
    
    # Test privacy engine
    try:
        privacy_result = test_privacy_engine()
        results.append(("Privacy Engine", privacy_result))
    except Exception as e:
        print(f"Privacy Engine test failed: {e}")
        results.append(("Privacy Engine", False))
    
    # # Test ethical framework
    # try:
    #     ethical_result = await test_ethical_framework()
    #     results.append(("Ethical Framework", ethical_result))
    # except Exception as e:
    #     print(f"Ethical Framework test failed: {e}")
    #     results.append(("Ethical Framework", False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    all_passed = all(passed for _, passed in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)