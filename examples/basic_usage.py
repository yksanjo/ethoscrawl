#!/usr/bin/env python3
"""
Basic usage example for EthosCrawl

This example shows how to use EthosCrawl for ethical web scraping
with privacy preservation and AI-powered analysis.
"""

import asyncio
import json
from datetime import datetime
from ethoscrawl import EthosCrawler, EthosConfig, PrivacyLevel, ComplianceStandard

async def main():
    """Main example function"""
    
    print("🚀 EthosCrawl Basic Usage Example")
    print("=" * 50)
    
    # 1. Configure EthosCrawl with ethical settings
    config = EthosConfig(
        privacy_level=PrivacyLevel.STRICT,
        ethical_standards=[ComplianceStandard.GDPR, ComplianceStandard.CCPA],
        ai_enabled=True,
        transparency_reports=True,
        rate_limit_requests=5  # Be conservative with requests
    )
    
    # 2. Initialize the crawler
    crawler = EthosCrawler(config)
    print("✅ EthosCrawler initialized with ethical configuration")
    
    # 3. Define the URL and selectors
    # Using a public test website for demonstration
    url = "https://quotes.toscrape.com/"
    selectors = [
        ".quote",  # Container for each quote
        ".text::text",  # Quote text
        ".author::text",  # Author name
        ".tags .tag::text"  # Tags
    ]
    
    print(f"\n📄 Scraping: {url}")
    print(f"🔍 Selectors: {selectors}")
    
    # 4. Perform ethical scraping with AI analysis
    try:
        results = await crawler.scrape(
            url=url,
            selectors=selectors,
            analysis_types=["sentiment", "entities"]  # AI analysis types
        )
        
        print(f"\n✅ Scraping completed successfully!")
        print(f"📊 Session ID: {results.session_id}")
        print(f"📈 Data points collected: {len(results.data)}")
        print(f"🛡️ Privacy applied: {results.privacy_applied}")
        print(f"⚖️ Ethical check passed: {results.ethical_check.get('passed', False)}")
        
        # 5. Display sample data
        if results.data:
            print("\n📋 Sample data (first 3 items):")
            for i, item in enumerate(results.data[:3], 1):
                print(f"\nItem {i}:")
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"  {item}")
        
        # 6. Display AI analysis results if available
        if results.metadata.get('analysis'):
            print("\n🤖 AI Analysis Results:")
            analysis = results.metadata['analysis']
            for key, value in analysis.items():
                print(f"  {key}: {value}")
        
        # 7. Display ethical check details
        if not results.ethical_check.get('passed', True):
            print("\n⚠️ Ethical Check Warnings:")
            for warning in results.ethical_check.get('warnings', []):
                print(f"  - {warning}")
        
        # 8. Export data with privacy preservation
        print("\n💾 Exporting data...")
        exported = await crawler.export(
            data=results.data,
            format="json",
            filename=f"ethoscrawl_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            anonymize=True
        )
        
        print(f"✅ Data exported to: {exported.get('filename', 'output.json')}")
        
        # 9. Generate a simple report
        print("\n📊 Summary Report:")
        print(f"   Total items: {len(results.data)}")
        print(f"   Session duration: {results.metadata.get('duration', 'N/A')}")
        print(f"   Compliance score: {results.ethical_check.get('compliance_score', 'N/A')}")
        print(f"   Privacy level: {config.privacy_level.value}")
        
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")
        import traceback
        traceback.print_exc()

async def monitor_example():
    """Example of real-time monitoring"""
    print("\n" + "=" * 50)
    print("🔄 Real-time Monitoring Example")
    print("=" * 50)
    
    config = EthosConfig(
        privacy_level=PrivacyLevel.STANDARD,
        ethical_standards=[ComplianceStandard.GDPR]
    )
    
    crawler = EthosCrawler(config)
    
    # Define callback for when changes are detected
    async def handle_change(data, metadata):
        print(f"\n🔔 Change detected at {metadata.get('timestamp')}")
        print(f"   Changes: {len(data.get('changes', []))} items")
        print(f"   URL: {metadata.get('url')}")
        
        # Process the changes (e.g., send notification, update database)
        # This is where you'd add your business logic
        
    # Start monitoring (commented out for safety in example)
    # Uncomment to actually run monitoring
    
    # print("Starting monitoring...")
    # print("Press Ctrl+C to stop")
    # 
    # try:
    #     await crawler.monitor(
    #         url="https://news.ycombinator.com/",
    #         callback=handle_change,
    #         check_interval=300,  # Check every 5 minutes
    #         selectors=[".athing"]  # Monitor hacker news items
    #     )
    # except KeyboardInterrupt:
    #     print("\nMonitoring stopped by user")

async def ethical_check_example():
    """Example of standalone ethical checking"""
    print("\n" + "=" * 50)
    print("⚖️ Ethical Check Example")
    print("=" * 50)
    
    from ethoscrawl.core.ethical_framework import EthicalFramework
    
    framework = EthicalFramework(standards=[ComplianceStandard.GDPR, ComplianceStandard.CCPA])
    
    # Check if scraping is ethically permissible
    test_urls = [
        "https://example.com",
        "https://github.com",
        "https://news.ycombinator.com"
    ]
    
    for url in test_urls:
        print(f"\nChecking: {url}")
        result = await framework.check_ethical(
            url=url,
            action="scrape",
            session_id="test_session"
        )
        
        if result.passed:
            print(f"  ✅ Allowed: {result.recommendations[0] if result.recommendations else 'No issues found'}")
        else:
            print(f"  ❌ Blocked: {', '.join(result.violations)}")

if __name__ == "__main__":
    # Run all examples
    asyncio.run(main())
    
    # Uncomment to run additional examples
    # asyncio.run(monitor_example())
    # asyncio.run(ethical_check_example())
    
    print("\n" + "=" * 50)
    print("🎉 Example completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Check the generated JSON file for your data")
    print("2. Review the ethical check results")
    print("3. Modify the example for your specific use case")
    print("4. Join our community at https://discord.gg/ethoscrawl")
    print("\nHappy ethical scraping! 🕷️✨")