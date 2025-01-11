import re
import json

def extract_emails_html(text):
    # Updated regex pattern to exclude emails with subdomains
    return re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?!\.\w+)', text)

def extract_emails_jsonld(soup):
    emails = []
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if "email" in data:
                emails.append(data["email"])
        except (json.JSONDecodeError, TypeError):
            continue
    return emails

def extract_valid_emails(text, soup):
    # Extract emails from HTML
    html_emails = extract_emails_html(text)
    # Extract emails from JSON-LD
    jsonld_emails = extract_emails_jsonld(soup)
    # Combine both lists
    all_emails = html_emails + jsonld_emails
    # Validate emails using regex and exclude specific patterns
    valid_emails = [email for email in all_emails if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) and not re.match(r'^[a-f0-9]{32}@sentry\.zipify\.com$', email)]
    return valid_emails
