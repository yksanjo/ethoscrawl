# Quick Start Guide

Get started with EthosCrawl in minutes. This guide will walk you through the basics of ethical web scraping.

## Your First Scrape

### 1. Basic Scraping

```python
import asyncio
from ethoscrawl import EthosCrawler

async def main():
    # Create a crawler with default settings
    crawler = EthosCrawler()
    
    # Scrape a website
    result = await crawler.scrape(
        url="https://quotes.toscrape.com/",
        selectors=[".quote", ".text::text", ".author::text"]
    )
    
    # Print results
    print(f"Collected {len(result.data)} quotes")
    for quote in result.data[:3]:
        print(f"  - {quote.get('text', 'N/A')} — {quote.get('author', 'Unknown')}")

# Run the async function
asyncio.run(main())
```

### 2. With Privacy Settings

```python
from ethoscrawl import EthosCrawler, PrivacyLevel

async def scrape_with_privacy():
    # Create crawler with strict privacy
    crawler = EthosCrawler(privacy_level=PrivacyLevel.STRICT)
    
    result = await crawler.scrape(
        url="https://news.example.com",
        selectors=[".article", ".title::text", ".summary::text"]
    )
    
    print(f"Data collected with {PrivacyLevel.STRICT.value} privacy")
    print(f"Privacy applied: {result.privacy_applied}")
```

### 3. Ethical Compliance Check

```python
from ethoscrawl.core.ethical_framework import EthicalFramework, ComplianceStandard

async def check_ethics():
    framework = EthicalFramework(standards=[ComplianceStandard.GDPR])
    
    check = await framework.check_ethical(
        url="https://example.com",
        action="scrape"
    )
    
    if check.passed:
        print("✅ Ethical to scrape")
    else:
        print("❌ Ethical issues found")
        for issue in check.violations:
            print(f"  - {issue}")
```

## CLI Quick Start

### Basic Commands

```bash
# Check version
ethoscrawl --version

# Get help
ethoscrawl --help

# Scrape a website
ethoscrawl scrape https://example.com --selectors ".title::text" ".content::text"

# With privacy settings
ethoscrawl scrape https://example.com --privacy-level strict --output data.json

# Check ethical compliance
ethoscrawl check https://example.com --standards gdpr ccpa

# Generate transparency report
ethoscrawl report https://example.com --format html
```

### Example Workflow

```bash
# 1. Check if scraping is ethical
ethoscrawl check https://news.example.com --standards gdpr

# 2. Scrape with privacy
ethoscrawl scrape https://news.example.com \
  --selectors ".article h2::text" ".article p::text" \
  --privacy-level standard \
  --output news_data.json \
  --limit 10

# 3. View report
ethoscrawl report --input news_data.json --format markdown
```

## Common Use Cases

### Use Case 1: Academic Research

```python
from ethoscrawl import EthosCrawler, PrivacyLevel
from ethoscrawl.core.ethical_framework import ComplianceStandard

async def academic_research():
    # Academic research often requires strict ethics
    crawler = EthosCrawler(
        privacy_level=PrivacyLevel.STRICT,
        ethical_standards=[ComplianceStandard.GDPR],
        rate_limit=2  # Be extra respectful
    )
    
    # Scrape research papers or articles
    results = []
    urls = [
        "https://arxiv.org/list/cs.AI/recent",
        "https://academic.example.com/papers"
    ]
    
    for url in urls:
        result = await crawler.scrape(
            url=url,
            selectors=[".paper", ".title::text", ".authors::text", ".abstract::text"]
        )
        results.append(result)
    
    return results
```

### Use Case 2: Business Intelligence

```python
async def business_intelligence():
    # Business use might prioritize data quality over maximum privacy
    crawler = EthosCrawler(
        privacy_level=PrivacyLevel.STANDARD,
        ethical_standards=[ComplianceStandard.ROBOTS_TXT],
        transparency_reports=True
    )
    
    # Monitor competitor websites
    result = await crawler.scrape(
        url="https://competitor.example.com/products",
        selectors=[".product", ".name::text", ".price::text", ".description::text"],
        max_pages=3  # Limit to first 3 pages
    )
    
    # Generate business insights
    print(f"Found {len(result.data)} products")
    print(f"Average price: ${sum(float(p.get('price', 0)) for p in result.data) / len(result.data):.2f}")
    
    return result
```

### Use Case 3: Personal Data Collection

```python
async def personal_use():
    # Personal use with maximum privacy
    crawler = EthosCrawler(
        privacy_level=PrivacyLevel.MAXIMUM,
        ethical_standards=[ComplianceStandard.GDPR, ComplianceStandard.CCPA],
        user_agent="Personal Research Bot/1.0"
    )
    
    # Collect data for personal analysis
    result = await crawler.scrape(
        url="https://personal.example.com/data",
        selectors=[".item", ".content::text"],
        respect_robots=True
    )
    
    # Data is heavily anonymized
    print("Data collected with maximum privacy protection")
    print(f"Original data points: {result.metadata.get('original_count', 0)}")
    print(f"After anonymization: {len(result.data)}")
    
    return result
```

## Configuration Examples

### Basic Configuration

```python
from ethoscrawl import EthosConfig

config = EthosConfig(
    # Privacy settings
    privacy_level="standard",  # or PrivacyLevel.STANDARD
    
    # Ethical standards
    ethical_standards=["gdpr", "ccpa", "robots_txt"],
    
    # Rate limiting
    requests_per_second=1,
    concurrent_requests=2,
    
    # Output
    save_transparency_reports=True,
    report_format="json"
)

crawler = EthosCrawler(config=config)
```

### Advanced Configuration

```python
config = EthosConfig(
    # Privacy engine settings
    privacy_engine={
        "anonymize_ip": True,
        "remove_pii": True,
        "hash_identifiers": True,
        "generalize_locations": True
    },
    
    # Ethical framework settings
    ethical_framework={
        "strict_mode": False,
        "require_explicit_consent": False,
        "respect_opt_out": True
    },
    
    # Adaptive engine settings
    adaptive_engine={
        "learn_patterns": True,
        "cache_responses": True,
        "retry_failed": True,
        "max_retries": 3
    },
    
    # Network settings
    network={
        "timeout": 30,
        "user_agent": "EthosCrawl/1.0",
        "proxy": None,  # or "http://proxy.example.com:8080"
        "verify_ssl": True
    }
)
```

## Best Practices for Quick Start

### 1. Start Simple
```python
# Start with minimal configuration
crawler = EthosCrawler()
result = await crawler.scrape(url="https://example.com", selectors=[".content::text"])
```

### 2. Add Privacy Gradually
```python
# Add privacy after basic scraping works
crawler = EthosCrawler(privacy_level=PrivacyLevel.STANDARD)
```

### 3. Check Ethics
```python
# Always check ethical compliance
framework = EthicalFramework()
check = await framework.check_ethical(url="https://example.com", action="scrape")
```

### 4. Use Rate Limiting
```python
# Be respectful to websites
crawler = EthosCrawler(requests_per_second=1)
```

### 5. Save Reports
```python
# Keep transparency reports
crawler = EthosCrawler(transparency_reports=True)
```

## Troubleshooting

### Common Issues

1. **No data returned**
   ```python
   # Check selectors
   result = await crawler.scrape(
       url="https://example.com",
       selectors=["div.content::text"]  # Try different selectors
   )
   ```

2. **Timeout errors**
   ```python
   # Increase timeout
   crawler = EthosCrawler(timeout=60)
   ```

3. **Rate limiting**
   ```python
   # Reduce request rate
   crawler = EthosCrawler(requests_per_second=0.5)
   ```

4. **Ethical blocks**
   ```python
   # Check robots.txt
   from ethoscrawl.core.ethical_framework import check_robots_txt
   allowed = await check_robots_txt("https://example.com")
   ```

## Next Steps

Now that you've completed the quick start:

1. **Explore Examples**: Check the `examples/` directory for more use cases
2. **Read Documentation**: Dive deeper into specific features
3. **Join Community**: Participate in discussions and ask questions
4. **Contribute**: Help improve EthosCrawl

Ready for more? Check out the [Configuration Guide](configuration.md) for detailed settings.