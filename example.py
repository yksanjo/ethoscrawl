#!/usr/bin/env python3
"""
Example usage of EthosCrawl
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ethoscrawl import EthosCrawler, EthosConfig, PrivacyLevel
from ethoscrawl.core.ethical_framework import ComplianceStandard


async def example_scraping():
    """Example of ethical web scraping with EthosCrawl"""
    print("🌐 EthosCrawl - Ethical Web Scraping Example")
    print("=" * 60)
    
    # Configuration for ethical scraping
    config = EthosConfig(
        privacy_level=PrivacyLevel.STRICT,  # Apply strong privacy protection
        ethical_standards=[
            ComplianceStandard.GDPR,        # GDPR compliance
            ComplianceStandard.CCPA,        # California privacy compliance
        ],
        transparency_reports=False,         # Disable for this example
        rate_limit_requests=5               # Be gentle on servers
    )
    
    # Initialize the crawler
    crawler = EthosCrawler(config=config)
    print(f"✅ Crawler initialized with {len(config.ethical_standards)} ethical standards")
    print(f"🔒 Privacy level: {config.privacy_level.value}")
    
    # Define what we want to scrape
    target_url = "https://quotes.toscrape.com/"
    selectors = [
        ".quote",           # Container for each quote
        ".text::text",      # Extract quote text
        ".author::text",    # Extract author name
        ".tags a::text"     # Extract tags
    ]
    
    print(f"\n🎯 Target: {target_url}")
    print(f"🔍 Selectors: {selectors}")
    
    # Perform the scrape
    print("\n⏳ Scraping with ethical considerations...")
    result = await crawler.scrape(url=target_url, selectors=selectors)
    
    # Display results
    print(f"\n✅ Scraping completed!")
    print(f"📊 Session ID: {result.session_id}")
    print(f"📈 Data points collected: {len(result.data)}")
    print(f"🔐 Privacy applied: {result.privacy_applied}")
    print(f"⚖️  Ethical compliance: {result.ethical_check.get('compliance_score', 'N/A')}/1.0")
    
    # Show some sample data
    if result.data:
        print(f"\n📋 Sample quotes (anonymized for privacy):")
        for i, item in enumerate(result.data[:5], 1):
            if isinstance(item, dict):
                text = item.get('text', '')
                # Show anonymized text (privacy engine may have modified it)
                print(f"  {i}. {text[:60]}..." if len(text) > 60 else f"  {i}. {text}")
    
    # Show metadata about the scraping process
    print(f"\n📊 Scraping metadata:")
    print(f"  Success: {result.metadata.get('scraping_success', 'N/A')}")
    print(f"  Adapted selectors: {result.metadata.get('adapted', False)}")
    print(f"  Content length: {result.metadata.get('content_length', 'N/A')} bytes")
    
    return result


async def compare_privacy_levels():
    """Compare different privacy levels"""
    print("\n" + "=" * 60)
    print("🔒 Comparing Privacy Levels")
    print("=" * 60)
    
    target_url = "https://quotes.toscrape.com/"
    selectors = [".quote", ".text::text", ".author::text"]
    
    for level in PrivacyLevel:
        print(f"\n{level.value.upper()} Privacy:")
        
        config = EthosConfig(
            privacy_level=level,
            ethical_standards=[ComplianceStandard.GDPR],
            transparency_reports=False
        )
        
        crawler = EthosCrawler(config=config)
        
        try:
            result = await crawler.scrape(url=target_url, selectors=selectors)
            print(f"  Data points: {len(result.data)}")
            
            if result.data:
                sample = result.data[0]
                if isinstance(sample, dict):
                    text = sample.get('text', '')
                    if text:
                        # Show how text is transformed at different privacy levels
                        print(f"  Sample: {text[:40]}..." if len(text) > 40 else f"  Sample: {text}")
        
        except Exception as e:
            print(f"  Error: {e}")


async def main():
    """Run all examples"""
    print("EthosCrawl Examples")
    print("=" * 60)
    
    # Run main example
    await example_scraping()
    
    # Compare privacy levels
    await compare_privacy_levels()
    
    print("\n" + "=" * 60)
    print("🎉 Examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())