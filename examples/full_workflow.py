#!/usr/bin/env python3
"""
EthosCrawl Full Workflow Example

This example demonstrates a complete ethical web scraping workflow:
1. Ethical compliance checking
2. Adaptive web scraping
3. Privacy-preserving data processing
4. Results export and reporting
"""

import asyncio
import json
from datetime import datetime
from ethoscrawl import EthosCrawler, EthosConfig, PrivacyLevel, ComplianceStandard
from ethoscrawl.core.ethical_framework import EthicalAction


async def ethical_scraping_workflow():
    """
    Complete ethical scraping workflow example
    """
    print("🚀 EthosCrawl Full Workflow Example")
    print("=" * 60)
    
    # Step 1: Configure EthosCrawl with strict ethical settings
    print("\n1. Configuring EthosCrawl with ethical settings...")
    
    config = EthosConfig(
        privacy_level=PrivacyLevel.STRICT,
        ethical_standards=[ComplianceStandard.GDPR, ComplianceStandard.CCPA],
        ai_enabled=False,  # Disable AI for this example
        transparency_reports=True,
        rate_limit_requests=5,  # Be conservative
        user_agent="EthosCrawl-Example/1.0 (+https://ethoscrawl.dev/examples)"
    )
    
    # Step 2: Initialize the crawler
    print("2. Initializing EthosCrawler...")
    crawler = EthosCrawler(config)
    
    # Step 3: Define target and selectors
    target_url = "https://quotes.toscrape.com/"
    selectors = [
        ".quote",           # Container for each quote
        ".text::text",      # Quote text
        ".author::text",    # Author name
        ".tags .tag::text"  # Tags
    ]
    
    print(f"\n3. Target: {target_url}")
    print(f"   Selectors: {selectors}")
    
    # Step 4: Perform ethical check
    print("\n4. Performing ethical compliance check...")
    
    ethical_result = await crawler.ethical_framework.check_ethical(
        url=target_url,
        action=EthicalAction.SCRAPE,
        data_types=["quotes", "authors", "tags"]
    )
    
    print(f"   ✅ Ethical check: {'PASSED' if ethical_result.passed else 'FAILED'}")
    print(f"   📊 Compliance score: {ethical_result.compliance_score:.2f}/1.0")
    
    if not ethical_result.passed:
        print("\n❌ Cannot proceed - ethical violations detected:")
        for violation in ethical_result.violations:
            print(f"   - {violation}")
        return
    
    if ethical_result.warnings:
        print("\n⚠️  Ethical warnings:")
        for warning in ethical_result.warnings:
            print(f"   - {warning}")
    
    # Step 5: Perform adaptive scraping
    print("\n5. Performing adaptive web scraping...")
    
    try:
        scrape_result = await crawler.scrape(
            url=target_url,
            selectors=selectors,
            max_retries=2,
            timeout=30
        )
        
        print(f"   ✅ Scraping completed successfully!")
        print(f"   📈 Data points collected: {len(scrape_result.data)}")
        print(f"   🆔 Session ID: {scrape_result.session_id}")
        print(f"   🛡️ Privacy applied: {scrape_result.privacy_applied}")
        
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        return
    
    # Step 6: Display sample data
    print("\n6. Sample data (first 5 items):")
    
    if scrape_result.data:
        for i, item in enumerate(scrape_result.data[:5], 1):
            print(f"\n   Item {i}:")
            if isinstance(item, dict):
                for key, value in item.items():
                    if key == 'text' and value:
                        print(f"     {key}: {value[:80]}..." if len(value) > 80 else f"     {key}: {value}")
                    elif key == 'html':
                        print(f"     {key}: [HTML content]")
                    else:
                        print(f"     {key}: {value}")
            else:
                print(f"     {item}")
    else:
        print("   No data collected")
    
    # Step 7: Apply additional privacy if needed
    print("\n7. Applying additional privacy preservation...")
    
    # The data is already privacy-preserved from scraping, but we can apply more
    if scrape_result.data:
        privacy_engine = crawler.privacy_engine
        enhanced_privacy_data = privacy_engine.apply_privacy(scrape_result.data)
        
        privacy_report = privacy_engine.get_privacy_report(
            scrape_result.data,
            enhanced_privacy_data
        )
        
        print(f"   🔒 Privacy level: {privacy_report['privacy_level']}")
        print(f"   📊 Transformations applied: {privacy_report['transformations_applied']}")
    
    # Step 8: Export results
    print("\n8. Exporting results...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"ethoscrawl_results_{timestamp}.json"
    
    export_data = {
        "metadata": {
            "url": target_url,
            "session_id": scrape_result.session_id,
            "timestamp": scrape_result.timestamp,
            "data_points": len(scrape_result.data),
            "ethical_check": {
                "passed": ethical_result.passed,
                "compliance_score": ethical_result.compliance_score,
                "warnings": ethical_result.warnings,
                "recommendations": ethical_result.recommendations
            }
        },
        "data": scrape_result.data,
        "privacy_report": privacy_report if 'privacy_report' in locals() else None
    }
    
    with open(output_filename, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"   💾 Results saved to: {output_filename}")
    
    # Step 9: Generate summary report
    print("\n9. Workflow Summary:")
    print("=" * 40)
    
    print(f"""
    📊 Summary Report
    -----------------
    Target URL: {target_url}
    Session ID: {scrape_result.session_id}
    Data Collected: {len(scrape_result.data)} items
    Ethical Compliance: {ethical_result.compliance_score:.2f}/1.0
    Privacy Level: {config.privacy_level.value}
    Output File: {output_filename}
    
    ✅ Workflow completed successfully!
    
    Next steps:
    1. Review the generated JSON file
    2. Check ethical compliance report
    3. Process data for your specific use case
    4. Consider data retention policies
    
    Remember: Always respect website terms of service
    and consider the ethical implications of data collection.
    """)
    
    return export_data


async def multiple_sites_example():
    """
    Example of scraping multiple sites with different ethical considerations
    """
    print("\n" + "=" * 60)
    print("🌐 Multiple Sites Scraping Example")
    print("=" * 60)
    
    sites = [
        {
            "name": "Public Quotes Site",
            "url": "https://quotes.toscrape.com/",
            "selectors": [".quote", ".text::text", ".author::text"],
            "data_types": ["quotes", "authors"],
            "privacy_level": PrivacyLevel.STANDARD
        },
        {
            "name": "News Site (Example)",
            "url": "https://httpbin.org/html",  # Using httpbin as example
            "selectors": ["h1", "p"],
            "data_types": ["headlines", "articles"],
            "privacy_level": PrivacyLevel.STRICT
        }
    ]
    
    config = EthosConfig(
        ethical_standards=[ComplianceStandard.GDPR],
        rate_limit_requests=3
    )
    
    crawler = EthosCrawler(config)
    
    results = []
    
    for site in sites:
        print(f"\n📄 Scraping: {site['name']}")
        print(f"   URL: {site['url']}")
        
        # Ethical check
        ethical_result = await crawler.ethical_framework.check_ethical(
            url=site['url'],
            action=EthicalAction.SCRAPE,
            data_types=site['data_types']
        )
        
        if not ethical_result.passed:
            print(f"   ❌ Skipping - ethical violations")
            continue
        
        # Update privacy level for this site
        crawler.config.privacy_level = site['privacy_level']
        
        # Scrape
        try:
            result = await crawler.scrape(
                url=site['url'],
                selectors=site['selectors']
            )
            
            print(f"   ✅ Collected {len(result.data)} items")
            print(f"   🔒 Privacy: {site['privacy_level'].value}")
            
            results.append({
                "site": site['name'],
                "data_count": len(result.data),
                "privacy_level": site['privacy_level'].value,
                "ethical_score": ethical_result.compliance_score
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Summary
    print("\n📊 Multiple Sites Summary:")
    for result in results:
        print(f"   {result['site']}: {result['data_count']} items, "
              f"Privacy: {result['privacy_level']}, "
              f"Ethical Score: {result['ethical_score']:.2f}")


async def main():
    """
    Run all examples
    """
    print("EthosCrawl Examples")
    print("=" * 60)
    
    # Run full workflow example
    await ethical_scraping_workflow()
    
    # Run multiple sites example
    await multiple_sites_example()
    
    print("\n" + "=" * 60)
    print("🎉 Examples completed!")
    print("=" * 60)
    print("\nLearn more at: https://github.com/ethoscrawl/ethoscrawl")
    print("Join our community to help shape the future of ethical data collection! 🚀")


if __name__ == "__main__":
    asyncio.run(main())