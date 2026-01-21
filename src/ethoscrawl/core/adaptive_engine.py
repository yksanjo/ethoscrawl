"""
Adaptive Scraping Engine

Enhanced Scrapling integration with self-learning capabilities for EthosCrawl.
This module provides adaptive web scraping that learns from website changes.
"""

import asyncio
import hashlib
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

# Try to import Scrapling, but provide fallback
try:
    from scrapling.fetchers import StealthyFetcher
    from scrapling.parsers import HTMLParser
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Scrapling not installed. Using fallback scraping methods.")

logger = logging.getLogger(__name__)


@dataclass
class ScrapingResult:
    """Result of a scraping operation"""
    data: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    success: bool
    error: Optional[str] = None
    adapted: bool = False
    original_selectors: Optional[List[str]] = None
    adapted_selectors: Optional[List[str]] = None


class AdaptiveScrapingEngine:
    """
    Enhanced Scrapling integration with self-learning capabilities.
    
    This engine adapts to website changes by learning patterns and
    automatically adjusting selectors when they fail.
    """
    
    def __init__(self, learning_rate: float = 0.1, cache_size: int = 1000):
        """
        Initialize the adaptive scraping engine.
        
        Args:
            learning_rate: How quickly to adapt to changes (0.0 to 1.0)
            cache_size: Maximum number of website patterns to cache
        """
        self.learning_rate = learning_rate
        self.cache_size = cache_size
        
        # Cache for website patterns and learned selectors
        self.website_patterns: Dict[str, Dict] = {}
        self.change_history: Dict[str, List] = {}
        self.selector_cache: Dict[str, List[str]] = {}
        
        # Initialize scrapling if available
        if SCRAPLING_AVAILABLE:
            self.fetcher = StealthyFetcher()
            self.parser = HTMLParser()
        else:
            self.fetcher = None
            self.parser = None
            
        logger.info(f"AdaptiveScrapingEngine initialized (Scrapling: {SCRAPLING_AVAILABLE})")
    
    async def scrape(
        self, 
        url: str, 
        selectors: List[str],
        max_retries: int = 3,
        timeout: int = 30
    ) -> ScrapingResult:
        """
        Scrape a URL with automatic adaptation to website changes.
        
        Args:
            url: The URL to scrape
            selectors: CSS selectors to extract data
            max_retries: Maximum number of retry attempts
            timeout: Request timeout in seconds
            
        Returns:
            ScrapingResult containing data and metadata
        """
        logger.info(f"Scraping {url} with {len(selectors)} selectors")
        
        # Generate session ID for tracking
        session_id = self._generate_session_id(url, selectors)
        
        # Try original selectors first
        result = await self._try_selectors(url, selectors, timeout)
        
        # If original selectors fail, try adaptation
        if not result.success and max_retries > 0:
            logger.info(f"Original selectors failed, attempting adaptation")
            
            for attempt in range(max_retries):
                # Generate adapted selectors
                adapted_selectors = await self._adapt_selectors(
                    url, 
                    selectors, 
                    result.error
                )
                
                # Try adapted selectors
                adapted_result = await self._try_selectors(
                    url, 
                    adapted_selectors, 
                    timeout
                )
                
                if adapted_result.success:
                    # Update learning model with successful adaptation
                    await self._update_patterns(
                        url, 
                        selectors, 
                        adapted_selectors, 
                        success=True
                    )
                    
                    adapted_result.adapted = True
                    adapted_result.original_selectors = selectors
                    adapted_result.adapted_selectors = adapted_selectors
                    
                    logger.info(f"Adaptation successful on attempt {attempt + 1}")
                    return adapted_result
                
                logger.debug(f"Adaptation attempt {attempt + 1} failed")
            
            # All adaptation attempts failed
            await self._update_patterns(
                url, 
                selectors, 
                [], 
                success=False
            )
        
        return result
    
    async def _try_selectors(
        self, 
        url: str, 
        selectors: List[str], 
        timeout: int
    ) -> ScrapingResult:
        """Try to scrape using given selectors"""
        try:
            # Fetch the page
            html_content = await self._fetch_page(url, timeout)
            
            if not html_content:
                return ScrapingResult(
                    data=[],
                    metadata={"url": url, "error": "Failed to fetch page"},
                    success=False,
                    error="Failed to fetch page"
                )
            
            # Parse and extract data
            data = await self._extract_data(html_content, selectors)
            
            # Generate metadata
            metadata = {
                "url": url,
                "selectors_used": selectors,
                "timestamp": datetime.now().isoformat(),
                "content_length": len(html_content),
                "data_points": len(data),
                "adaptation_required": False
            }
            
            return ScrapingResult(
                data=data,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return ScrapingResult(
                data=[],
                metadata={"url": url, "error": str(e)},
                success=False,
                error=str(e)
            )
    
    async def _fetch_page(self, url: str, timeout: int) -> Optional[str]:
        """Fetch a web page with appropriate method"""
        try:
            if SCRAPLING_AVAILABLE and self.fetcher:
                # Use Scrapling's stealthy fetcher
                response = await self.fetcher.fetch(url, timeout=timeout)
                return response.text if response else None
            else:
                # Fallback to httpx or requests
                import httpx
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.get(url)
                    response.raise_for_status()
                    return response.text
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    async def _extract_data(
        self, 
        html_content: str, 
        selectors: List[str]
    ) -> List[Dict[str, Any]]:
        """Extract data from HTML using selectors"""
        data = []
        
        try:
            if SCRAPLING_AVAILABLE and self.parser:
                # Use Scrapling's parser
                parsed = self.parser.parse(html_content)
                for selector in selectors:
                    elements = parsed.select(selector)
                    for elem in elements:
                        data.append({
                            "selector": selector,
                            "text": elem.text.strip() if hasattr(elem, 'text') else str(elem),
                            "html": str(elem)
                        })
            else:
                # Fallback using BeautifulSoup
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')
                
                for selector in selectors:
                    # Strip pseudo-elements for BeautifulSoup compatibility
                    clean_selector = selector.split('::')[0] if '::' in selector else selector
                    
                    try:
                        elements = soup.select(clean_selector)
                        for elem in elements:
                            # Handle pseudo-element extraction if specified
                            if '::text' in selector:
                                text = elem.get_text(strip=True)
                            elif '::attr(' in selector:
                                # Extract attribute
                                import re
                                attr_match = re.search(r'::attr\(([^)]+)\)', selector)
                                if attr_match:
                                    attr_name = attr_match.group(1)
                                    text = elem.get(attr_name, '')
                                else:
                                    text = elem.get_text(strip=True)
                            else:
                                text = elem.get_text(strip=True)
                            
                            data.append({
                                "selector": selector,
                                "text": text,
                                "html": str(elem)
                            })
                    except Exception as e:
                        logger.warning(f"Failed to extract with selector {selector}: {e}")
                        continue
            
            return data
            
        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            return []
    
    async def _adapt_selectors(
        self, 
        url: str, 
        failed_selectors: List[str], 
        error: Optional[str] = None
    ) -> List[str]:
        """Generate adapted selectors based on learned patterns"""
        domain = self._extract_domain(url)
        
        # Check if we have patterns for this domain
        if domain in self.website_patterns:
            patterns = self.website_patterns[domain]
            logger.debug(f"Using learned patterns for {domain}")
            
            # Generate new selectors based on patterns
            new_selectors = await self._generate_from_patterns(
                failed_selectors, 
                patterns
            )
            
            if new_selectors:
                return new_selectors
        
        # Fallback: use structural analysis
        logger.debug(f"No patterns for {domain}, using structural analysis")
        return await self._structural_adaptation(url, failed_selectors)
    
    async def _structural_adaptation(
        self, 
        url: str, 
        failed_selectors: List[str]
    ) -> List[str]:
        """Generate new selectors based on HTML structure analysis"""
        # This is a simplified version - in production, this would
        # analyze the HTML structure and generate new selectors
        
        # For now, return some common alternative selectors
        common_selectors = [
            "article", ".content", ".main", "#content", 
            ".post", ".entry", ".item", ".product"
        ]
        
        # Also try to modify the original selectors
        adapted = []
        for selector in failed_selectors:
            # Try different variations
            if selector.startswith('.'):
                # Class selector - try without dot, try with different classes
                class_name = selector[1:]
                adapted.extend([
                    f"[class*='{class_name}']",
                    f"[class^='{class_name}']",
                    f"[class$='{class_name}']",
                ])
            elif selector.startswith('#'):
                # ID selector - try as class
                id_name = selector[1:]
                adapted.append(f".{id_name}")
        
        return list(set(common_selectors + adapted))[:10]  # Limit to 10 selectors
    
    async def _generate_from_patterns(
        self, 
        failed_selectors: List[str], 
        patterns: Dict
    ) -> List[str]:
        """Generate new selectors from learned patterns"""
        # This would use ML models in production
        # For now, return patterns from similar successful scrapes
        
        if 'successful_selectors' in patterns:
            return patterns['successful_selectors'][:5]  # Return top 5
        
        return []
    
    async def _update_patterns(
        self, 
        url: str, 
        original_selectors: List[str], 
        adapted_selectors: List[str], 
        success: bool
    ):
        """Update learning patterns based on scraping results"""
        domain = self._extract_domain(url)
        
        if domain not in self.website_patterns:
            self.website_patterns[domain] = {
                'successful_selectors': [],
                'failed_selectors': [],
                'adaptation_history': [],
                'last_updated': datetime.now().isoformat()
            }
        
        patterns = self.website_patterns[domain]
        
        if success and adapted_selectors:
            # Add successful selectors to patterns
            for selector in adapted_selectors:
                if selector not in patterns['successful_selectors']:
                    patterns['successful_selectors'].append(selector)
            
            # Record adaptation
            patterns['adaptation_history'].append({
                'timestamp': datetime.now().isoformat(),
                'original': original_selectors,
                'adapted': adapted_selectors,
                'success': success
            })
        else:
            # Record failure
            for selector in original_selectors:
                if selector not in patterns['failed_selectors']:
                    patterns['failed_selectors'].append(selector)
        
        # Limit cache size
        if len(self.website_patterns) > self.cache_size:
            # Remove oldest entries
            oldest_key = min(
                self.website_patterns.keys(),
                key=lambda k: self.website_patterns[k].get('last_updated', '')
            )
            del self.website_patterns[oldest_key]
        
        patterns['last_updated'] = datetime.now().isoformat()
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        # Simple domain extraction
        match = re.match(r'https?://([^/]+)', url)
        if match:
            return match.group(1)
        return url
    
    def _generate_session_id(self, url: str, selectors: List[str]) -> str:
        """Generate a unique session ID"""
        content = f"{url}:{':'.join(sorted(selectors))}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics"""
        return {
            "total_domains_cached": len(self.website_patterns),
            "learning_rate": self.learning_rate,
            "scrapling_available": SCRAPLING_AVAILABLE,
            "cache_size": self.cache_size,
            "current_cache_size": len(self.website_patterns)
        }
    
    def clear_cache(self):
        """Clear all cached patterns"""
        self.website_patterns.clear()
        self.change_history.clear()
        self.selector_cache.clear()
        logger.info("Cache cleared")


# Example usage
async def example():
    """Example usage of AdaptiveScrapingEngine"""
    engine = AdaptiveScrapingEngine()
    
    # Scrape a website
    result = await engine.scrape(
        url="https://quotes.toscrape.com/",
        selectors=[".quote", ".text::text", ".author::text"]
    )
    
    if result.success:
        print(f"Successfully scraped {len(result.data)} items")
        for item in result.data[:3]:  # Show first 3 items
            print(f"  - {item.get('text', 'No text')}")
    else:
        print(f"Scraping failed: {result.error}")
    
    # Show stats
    stats = engine.get_stats()
    print(f"\nEngine stats: {stats}")


if __name__ == "__main__":
    # Run example
    asyncio.run(example())