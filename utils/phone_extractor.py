import re
import json
import phonenumbers

def validate_phones(phones):
    valid_phones = []
    for phone in phones:
        try:
            parsed_phone = phonenumbers.parse(phone, "US")  # Use the appropriate country code
            if phonenumbers.is_valid_number(parsed_phone):
                valid_phones.append(phone)
        except phonenumbers.NumberParseException:
            continue
    return valid_phones

def extract_phones_html(text):
    phone_pattern = re.compile(r'\b(?:\d{1,4}[-.\s]?)?(\d{3}[-.\s]?){2}\d{4}\b')
    phones = phone_pattern.findall(text)
    return validate_phones(phones)

def extract_phones_jsonld(soup):
    phones = set()
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if "telephone" in data:
                phone = data["telephone"]
                try:
                    parsed_phone = phonenumbers.parse(phone, "US")  # Use the appropriate country code
                    if phonenumbers.is_valid_number(parsed_phone):
                        phones.add(phone)
                except phonenumbers.NumberParseException:
                    continue
        except (json.JSONDecodeError, TypeError):
            continue
    return list(phones)
