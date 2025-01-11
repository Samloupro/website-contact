import re
import json

def extract_emails_html(text):
    return re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)

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
        except (json.JSONDecodeError, TypeError):
            continue
    return emails
