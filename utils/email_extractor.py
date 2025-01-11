import re
import json
import logging
from email_validator import validate_email, EmailNotValidError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_emails_html_strict(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    potential_emails = re.findall(email_pattern, text)
    valid_emails = []
    
    for email in potential_emails:
        try:
            # Valider l'e-mail
            valid = validate_email(email)
            valid_emails.append(valid.email)
            logger.info(f"Email valide extrait du HTML : {valid.email}")
        except EmailNotValidError as e:
            logger.warning(f"Adresse e-mail invalide trouvée : {email} - {e}")
    
    return valid_emails

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
