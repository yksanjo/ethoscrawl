#!/usr/bin/env python3
"""
Test the main EthosCrawler
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ethoscrawl import EthosCrawler, EthosConfig, PrivacyLevel
from ethoscrawl.core.ethical_framework import ComplianceStandard


async def test_main_crawler():
    """Test the main crawler"""
    print("Testing EthosCrawler...")
    print("=" * 60)

    # Create configuration
    config = EthosConfig(
        privacy_level=PrivacyLevel.STANDARD,
        ethical_standards=[ComplianceStandard.GDPR],
        transparency_reports=False  # Disable since module doesn't exist
    )
    
    # Initialize crawler with configuration
    crawler = EthosCrawler(config=config)

    # Test scraping a simple website
    url = "https://quotes.toscrape.com/"
    selectors = [".quote", ".text::text", ".author::text"]

    print(f"Scraping: {url}")
    print(f"Selectors: {selectors}")

    try:
        result = await crawler.scrape(url=url, selectors=selectors)

        print(f"\n✅ Scraping completed!")
        print(f"Session ID: {result.session_id}")
        print(f"Data points: {len(result.data)}")
        print(f"Privacy applied: {result.privacy_applied}")
        print(f"Ethical check passed: {result.ethical_check.get('passed', False)}")
        print(f"Compliance score: {result.ethical_check.get('compliance_score', 'N/A')}")

        if result.data:
            print(f"\n📋 Sample data (first 3 items):")
            for i, item in enumerate(result.data[:3], 1):
                if isinstance(item, dict):
                    text = item.get('text', 'No text')
                    print(f"  {i}. {text[:80]}..." if len(text) > 80 else f"  {i}. {text}")

        # Show metadata
        print(f"\n📊 Metadata:")
        for key, value in result.metadata.items():
            if key not in ['ethical_check']:
                print(f"  {key}: {value}")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run test"""
    print("EthosCrawl Main Crawler Test")
    print("=" * 60)

    # Test main crawler
    success = await test_main_crawler()

    print("\n" + "=" * 60)
    if success:
        print("🎉 Test completed successfully!")
    else:
        print("⚠️  Test completed with errors")
    print("=" * 60)

    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)