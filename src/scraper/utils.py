import re
import time
from urllib.parse import urljoin

import requests

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"


def safe_get(url, retries=3, delay=1):
    """Make an HTTP GET request with basic retry logic."""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"  Attempt {attempt + 1} failed for {url}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
    print(f"  Giving up on {url}")
    return None


def resolve_url(base, href):
    """
    Resolve a relative or root-relative URL against a base URL.
    Uses urllib.parse.urljoin for correct handling of all URL forms.
    """
    if not href:
        return ""
    return urljoin(base, href)
##return

def clean_text(text):
    """Strip and normalize whitespace from a text string."""
    if not text:
        return ""
    return " ".join(str(text).strip().split())


def parse_price(price_str):
    """Extract a numeric float from a price string like '$123.45'."""
    if not price_str:
        return None
    try:
        cleaned = re.sub(r"[^\d.]", "", str(price_str))
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def deduplicate(products):
    """
    Remove duplicate products based on their URL.
    Returns (unique_products, count_of_duplicates_removed).
    """
    seen_urls = set()
    unique = []
    removed = 0
    for product in products:
        url = product.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(product)
        else:
            removed += 1
    return unique, removed