from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import logging
import json

logger = logging.getLogger(__name__)


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def extract_links(soup, base_url):
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/"):
            href = base_url.rstrip("/") + href
        if href.startswith("http") and is_valid_url(href):
            links.add(href)
    return links

def extract_links_jsonld(soup):
    links = set()
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            # Ensure script.string is not None before loading it as JSON
            if script.string:
                data = json.loads(script.string)
                if "sameAs" in data:
                    for link in data["sameAs"]:
                        if link and link.startswith("http") and is_valid_url(link):
                            links.add(link)
        except (json.JSONDecodeError, TypeError):
            continue
    return links

def link_scraper(url, headers, max_link=None):
    if not url or not is_valid_url(url):
        logger.error(f"Invalid URL provided: {url}")
        return {'error': 'Invalid URL provided.'}, 400

    try:
        response = requests.get(url, headers=headers, timeout=60)
        
        # Log request details
        logger.info(f"Request URL: {url}")
        logger.info(f"Request headers: {headers}")

        response.raise_for_status()
        
        # Log response details
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")

        # Log the HTML content fetched
        if response.status_code == 200:
            logger.info("***HTML FETCH SUCCESS***")
            logger.info(f"Fetched HTML content: {response.text[:500]}")  # Log first 500 chars of response
        else:
            logger.error("***HTML FETCH FAILED***")

        soup = BeautifulSoup(response.text, 'html.parser')

        links = extract_links(soup, url)
        jsonld_links = extract_links_jsonld(soup)
        all_links = links.union(jsonld_links)  # Combine both sets of links
        
        if max_link:
            all_links = list(all_links)[:max_link]  # Limit the number of links

        # Log the extracted links for verification
        logger.info(f"Extracted links: {all_links}")

        return list(all_links), None
    except requests.RequestException as e:
        logger.error(f"Error scraping {url}: {e}")
        logger.error("***HTML FETCH FAILED***")
        return [], str(e)
