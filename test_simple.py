#!/usr/bin/env python3
"""
Test the simplified EthosCrawler
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ethoscrawl.simple_crawler import SimpleEthosCrawler, PrivacyLevel
from ethoscrawl.core.ethical_framework import ComplianceStandard


async def test_simple_crawler():
    """Test the simplified crawler"""
    print("Testing SimpleEthosCrawler...")
    print("=" * 60)
    
    # Initialize crawler with strict privacy and GDPR compliance
    crawler = SimpleEthosCrawler(
        privacy_level=PrivacyLevel.STRICT,
        ethical_standards=[ComplianceStandard.GDPR]
    )
    
    # Test scraping a simple website
    url = "https://quotes.toscrape.com/"
    selectors = [".quote", ".text::text", ".author::text"]
    
    print(f"Scraping: {url}")
    print(f"Selectors: {selectors}")
    print(f"Privacy level: {crawler.privacy_level.value}")
    print(f"Ethical standards: {[s.value for s in crawler.ethical_standards]}")
    
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
                else:
                    print(f"  {i}. {str(item)[:80]}...")
        
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


async def test_privacy_levels():
    """Test different privacy levels"""
    print("\n" + "=" * 60)
    print("Testing Different Privacy Levels")
    print("=" * 60)
    
    url = "https://quotes.toscrape.com/"
    selectors = [".quote", ".text::text", ".author::text"]
    
    for privacy_level in PrivacyLevel:
        print(f"\n🔒 Privacy Level: {privacy_level.value}")
        
        crawler = SimpleEthosCrawler(
            privacy_level=privacy_level,
            ethical_standards=[ComplianceStandard.GDPR]
        )
        
        try:
            result = await crawler.scrape(url=url, selectors=selectors)
            print(f"  Data points: {len(result.data)}")
            print(f"  Privacy applied: {result.privacy_applied}")
            
            # Show sample of anonymized data
            if result.data and privacy_level != PrivacyLevel.MINIMAL:
                sample = result.data[0] if result.data else {}
                if isinstance(sample, dict):
                    text = sample.get('text', '')
                    if text:
                        print(f"  Sample text: {text[:50]}..." if len(text) > 50 else f"  Sample text: {text}")
            
        except Exception as e:
            print(f"  Error: {e}")


async def main():
    """Run all tests"""
    print("EthosCrawl Simple Crawler Test")
    print("=" * 60)
    
    # Test simple crawler
    success = await test_simple_crawler()
    
    # Test different privacy levels
    await test_privacy_levels()
    
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