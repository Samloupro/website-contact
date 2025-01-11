import re
import json
import logging
from email_validator import validate_email, EmailNotValidError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_emails_html(text):
    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    for email in emails:
        logger.info(f"Extracted email from HTML: {email}")
    return emails

def extract_emails_jsonld(soup):
    emails = []
    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$')
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if "email" in data:
                email = data["email"].strip().rstrip('.')
                if email_regex.match(email):
                    emails.append(email)
                    logger.info(f"Extracted email from JSON-LD: {email}")
        except (json.JSONDecodeError, TypeError):
            continue
    return emails
