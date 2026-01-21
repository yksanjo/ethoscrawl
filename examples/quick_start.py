#!/usr/bin/env python3
"""
Quick Start Example for EthosCrawl

This example shows the basic usage of EthosCrawl for ethical web scraping.
"""

import asyncio
import sys
import os

# Add parent directory to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ethoscrawl import EthosCrawler, EthosConfig, PrivacyLevel
from ethoscrawl.core.ethical_framework import ComplianceStandard


async def quick_demo():
    """Quick demonstration of EthosCrawl's core features"""
    print("🚀 EthosCrawl Quick Start")
    print("=" * 60)
    
    # 1. Basic Configuration
    print("\n1️⃣  Configuring EthosCrawl")
    print("-" * 40)
    
    config = EthosConfig(
        privacy_level=PrivacyLevel.STANDARD,
        ethical_standards=[ComplianceStandard.GDPR],
        transparency_reports=False  # Disable for quick demo
    )
    
    print(f"   Privacy level: {config.privacy_level.value}")
    print(f"   Ethical standards: {[s.value for s in config.ethical_standards]}")
    
    # 2. Initialize Crawler
    print("\n2️⃣  Initializing Crawler")
    print("-" * 40)
    
    crawler = EthosCrawler(config=config)
    print("   ✅ Crawler ready!")
    
    # 3. Define what to scrape
    print("\n3️⃣  Setting up scraping parameters")
    print("-" * 40)
    
    # Using a public quotes website for demonstration
    url = "https://quotes.toscrape.com/"
    selectors = [
        ".quote",           # Container for each quote
        ".text::text",      # Quote text
        ".author::text",    # Author name
        ".tags a::text"     # Tags
    ]
    
    print(f"   URL: {url}")
    print(f"   Selectors: {selectors}")
    
    # 4. Perform the scrape
    print("\n4️⃣  Scraping with ethical considerations...")
    print("-" * 40)
    
    try:
        result = await crawler.scrape(url=url, selectors=selectors)
        
        print("   ✅ Scraping completed successfully!")
        print(f"   Session ID: {result.session_id}")
        print(f"   Data points collected: {len(result.data)}")
        print(f"   Privacy applied: {result.privacy_applied}")
        print(f"   Ethical compliance score: {result.ethical_check.get('compliance_score', 'N/A')}/1.0")
        
        # 5. Display results
        print("\n5️⃣  Sample Results")
        print("-" * 40)
        
        if result.data:
            print(f"   First 3 items:")
            for i, item in enumerate(result.data[:3], 1):
                if isinstance(item, dict):
                    text = item.get('text', 'No text')
                    author = item.get('author', 'Unknown')
                    print(f"   {i}. \"{text[:50]}...\" - {author}")
        else:
            print("   No data collected (might be due to privacy settings)")
        
        # 6. Show metadata
        print("\n6️⃣  Scraping Metadata")
        print("-" * 40)
        
        metadata = result.metadata
        print(f"   Success: {metadata.get('scraping_success', 'N/A')}")
        print(f"   Adapted selectors: {metadata.get('adapted', False)}")
        print(f"   Content length: {metadata.get('content_length', 'N/A')} bytes")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        return False


async def compare_privacy_levels():
    """Compare different privacy levels"""
    print("\n" + "=" * 60)
    print("🔒 Comparing Privacy Levels")
    print("=" * 60)
    
    url = "https://quotes.toscrape.com/"
    selectors = [".quote", ".text::text"]
    
    for level in PrivacyLevel:
        print(f"\n{level.value.upper()}:")
        
        config = EthosConfig(
            privacy_level=level,
            ethical_standards=[ComplianceStandard.GDPR],
            transparency_reports=False
        )
        
        crawler = EthosCrawler(config=config)
        
        try:
            result = await crawler.scrape(url=url, selectors=selectors)
            print(f"  Data points: {len(result.data)}")
            print(f"  Privacy applied: {result.privacy_applied}")
            
            if result.data:
                sample = result.data[0]
                if isinstance(sample, dict):
                    text = sample.get('text', '')
                    if text:
                        # Show how text looks at different privacy levels
                        display_text = text[:40] + "..." if len(text) > 40 else text
                        print(f"  Sample: \"{display_text}\"")
        
        except Exception as e:
            print(f"  Error: {e}")


async def ethical_compliance_check():
    """Demonstrate ethical compliance checking"""
    print("\n" + "=" * 60)
    print("⚖️  Ethical Compliance Check")
    print("=" * 60)
    
    from ethoscrawl.core.ethical_framework import EthicalFramework, EthicalAction
    
    framework = EthicalFramework(standards=[ComplianceStandard.GDPR])
    
    test_urls = [
        "https://quotes.toscrape.com/",  # Public, scrape-friendly
        "https://example.com/",           # Generic example
        "https://twitter.com/",           # Social media (typically restricted)
    ]
    
    for url in test_urls:
        print(f"\nChecking: {url}")
        
        try:
            check = await framework.check_ethical(
                url=url,
                action=EthicalAction.SCRAPE
            )
            
            status = "✅ PASS" if check.passed else "❌ FAIL"
            print(f"  Result: {status}")
            print(f"  Compliance score: {check.compliance_score}/1.0")
            
            if check.warnings:
                print(f"  Warnings: {len(check.warnings)}")
            
            if check.violations:
                print(f"  Violations: {len(check.violations)}")
                for violation in check.violations[:2]:  # Show first 2
                    print(f"    - {violation}")
        
        except Exception as e:
            print(f"  Error: {e}")


async def main():
    """Run all examples"""
    print("EthosCrawl Examples")
    print("=" * 60)
    
    # Run quick demo
    success = await quick_demo()
    
    if success:
        # Compare privacy levels
        await compare_privacy_levels()
        
        # Show ethical compliance checking
        await ethical_compliance_check()
        
        print("\n" + "=" * 60)
        print("🎉 Quick Start Completed Successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Read the documentation for advanced features")
        print("2. Check out more examples in the examples/ directory")
        print("3. Join our community for support and updates")
        print("4. Consider contributing to the project")
    else:
        print("\n" + "=" * 60)
        print("⚠️  Quick Start encountered errors")
        print("=" * 60)
        print("\nTroubleshooting tips:")
        print("1. Make sure you have an internet connection")
        print("2. Check if https://quotes.toscrape.com/ is accessible")
        print("3. Verify installation: pip install ethoscrawl")
        print("4. Check the error message above for details")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())