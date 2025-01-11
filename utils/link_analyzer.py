from bs4 import BeautifulSoup
import requests
import logging
from urllib.parse import urlparse
from utils.email_extractor import extract_emails_html, extract_emails_jsonld
from utils.phone_extractor import extract_phones_html, extract_phones_jsonld, validate_phones

logger = logging.getLogger(__name__)

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def analyze_links(link, headers, domain):
    emails = {}
    phones = {}
    visited_links = set()

    if link in visited_links:
        return emails, phones, visited_links

    logger.info(f"Analyzing link: {link}")
    visited_links.add(link)

    try:
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        emails_found = extract_emails_html(soup.text) + extract_emails_jsonld(soup)
        for email in set(emails_found):
            emails.setdefault(email, []).append(link)

        phones_found = extract_phones_html(soup.text) + extract_phones_jsonld(soup)
        for phone in set(validate_phones(phones_found)):
            phones.setdefault(phone, []).append(link)
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to process link {link}: {e}")

    return emails, phones, visited_links
