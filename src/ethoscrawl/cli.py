#!/usr/bin/env python3
"""
Command Line Interface for EthosCrawl
"""

import asyncio
import json
import sys
import argparse
from typing import List, Optional
from pathlib import Path

from . import EthosCrawler, EthosConfig, PrivacyLevel
from .core.ethical_framework import ComplianceStandard, EthicalAction


async def scrape_command(
    url: str,
    selectors: List[str],
    privacy_level: str = "standard",
    output: Optional[str] = None,
    standards: List[str] = None,
    **kwargs
):
    """Execute scrape command"""
    # Parse privacy level
    try:
        privacy = PrivacyLevel(privacy_level.lower())
    except ValueError:
        print(f"Error: Invalid privacy level '{privacy_level}'")
        print(f"Available levels: {[l.value for l in PrivacyLevel]}")
        return 1
    
    # Parse compliance standards
    compliance_standards = []
    if standards:
        for std in standards:
            try:
                compliance_standards.append(ComplianceStandard(std.lower()))
            except ValueError:
                print(f"Warning: Invalid standard '{std}', skipping")
    
    # Create configuration
    config = EthosConfig(
        privacy_level=privacy,
        ethical_standards=compliance_standards or [ComplianceStandard.GDPR],
        transparency_reports=False  # Disable for CLI for now
    )
    
    # Initialize crawler
    crawler = EthosCrawler(config=config)
    
    print(f"🌐 Scraping: {url}")
    print(f"🔍 Selectors: {selectors}")
    print(f"🔒 Privacy level: {privacy.value}")
    print(f"⚖️  Standards: {[s.value for s in config.ethical_standards]}")
    print("\n⏳ Starting ethical scrape...")
    
    try:
        # Perform scrape
        result = await crawler.scrape(url=url, selectors=selectors)
        
        print(f"\n✅ Scrape completed!")
        print(f"📊 Session ID: {result.session_id}")
        print(f"📈 Data points: {len(result.data)}")
        print(f"🔐 Privacy applied: {result.privacy_applied}")
        print(f"⚖️  Compliance score: {result.ethical_check.get('compliance_score', 'N/A')}/1.0")
        
        # Save output if requested
        if output:
            output_path = Path(output)
            if output_path.suffix == '.json':
                # Convert to serializable format
                result_dict = {
                    "data": result.data,
                    "metadata": result.metadata,
                    "ethical_check": result.ethical_check,
                    "privacy_applied": result.privacy_applied,
                    "session_id": result.session_id,
                    "timestamp": result.timestamp
                }
                with open(output_path, 'w') as f:
                    json.dump(result_dict, f, indent=2, default=str)
                print(f"💾 Results saved to: {output_path}")
            else:
                # Save as text
                with open(output_path, 'w') as f:
                    f.write(f"EthosCrawl Results\n")
                    f.write(f"=================\n\n")
                    f.write(f"URL: {url}\n")
                    f.write(f"Session ID: {result.session_id}\n")
                    f.write(f"Data points: {len(result.data)}\n")
                    f.write(f"Privacy applied: {result.privacy_applied}\n\n")
                    
                    if result.data:
                        f.write("Data:\n")
                        f.write("-----\n")
                        for i, item in enumerate(result.data, 1):
                            if isinstance(item, dict):
                                text = item.get('text', '')
                                if text:
                                    f.write(f"{i}. {text}\n")
                print(f"💾 Results saved to: {output_path}")
        
        # Show sample data
        if result.data:
            print(f"\n📋 Sample data (first 3 items):")
            for i, item in enumerate(result.data[:3], 1):
                if isinstance(item, dict):
                    text = item.get('text', '')
                    if text:
                        print(f"  {i}. {text[:80]}..." if len(text) > 80 else f"  {i}. {text}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        return 1


async def check_command(url: str, standards: List[str] = None, **kwargs):
    """Check ethical compliance of a URL"""
    from .core.ethical_framework import EthicalFramework
    
    # Parse compliance standards
    compliance_standards = []
    if standards:
        for std in standards:
            try:
                compliance_standards.append(ComplianceStandard(std.lower()))
            except ValueError:
                print(f"Warning: Invalid standard '{std}', skipping")
    
    if not compliance_standards:
        compliance_standards = [ComplianceStandard.GDPR]
    
    # Initialize framework
    framework = EthicalFramework(standards=compliance_standards)
    
    print(f"🔍 Checking ethical compliance for: {url}")
    print(f"⚖️  Standards: {[s.value for s in compliance_standards]}")
    
    try:
        check = await framework.check_ethical(
            url=url,
            action=EthicalAction.SCRAPE
        )
        
        print(f"\n📊 Results:")
        print(f"  Passed: {'✅' if check.passed else '❌'}")
        print(f"  Compliance score: {check.compliance_score}/1.0")
        print(f"  Warnings: {len(check.warnings)}")
        print(f"  Violations: {len(check.violations)}")
        
        if check.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in check.warnings:
                print(f"  - {warning}")
        
        if check.violations:
            print(f"\n❌ Violations:")
            for violation in check.violations:
                print(f"  - {violation}")
        
        if check.passed:
            print(f"\n✅ This URL appears to be ethically scrapeable")
        else:
            print(f"\n❌ This URL has ethical violations that should be addressed")
        
        return 0 if check.passed else 1
        
    except Exception as e:
        print(f"\n❌ Error during compliance check: {e}")
        return 1


async def demo_command(**kwargs):
    """Run a demo of EthosCrawl"""
    print("🚀 EthosCrawl Demo")
    print("=" * 60)
    
    # Use quotes.toscrape.com for demo
    url = "https://quotes.toscrape.com/"
    selectors = [".quote", ".text::text", ".author::text"]
    
    print(f"Demo URL: {url}")
    print(f"Selectors: {selectors}")
    print("\n" + "=" * 60)
    
    # Run scrape command
    return await scrape_command(
        url=url,
        selectors=selectors,
        privacy_level="strict",
        standards=["gdpr"]
    )


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="EthosCrawl - Ethical Web Scraping Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s scrape https://example.com --selectors ".title::text" ".content::text"
  %(prog)s scrape https://example.com --privacy-level strict --output results.json
  %(prog)s check https://example.com --standards gdpr ccpa
  %(prog)s demo
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape a website ethically")
    scrape_parser.add_argument("url", help="URL to scrape")
    scrape_parser.add_argument("--selectors", nargs="+", required=True,
                             help="CSS selectors to extract (e.g., '.title::text')")
    scrape_parser.add_argument("--privacy-level", default="standard",
                             choices=[l.value for l in PrivacyLevel],
                             help="Privacy level to apply")
    scrape_parser.add_argument("--output", "-o", help="Output file path")
    scrape_parser.add_argument("--standards", nargs="+",
                             choices=[s.value for s in ComplianceStandard],
                             help="Compliance standards to enforce")
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check ethical compliance")
    check_parser.add_argument("url", help="URL to check")
    check_parser.add_argument("--standards", nargs="+",
                            choices=[s.value for s in ComplianceStandard],
                            help="Compliance standards to check")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run a demo of EthosCrawl")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    if args.command == "scrape":
        return asyncio.run(scrape_command(**vars(args)))
    elif args.command == "check":
        return asyncio.run(check_command(**vars(args)))
    elif args.command == "demo":
        return asyncio.run(demo_command(**vars(args)))
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())