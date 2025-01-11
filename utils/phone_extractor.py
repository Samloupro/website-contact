import json
import phonenumbers
from phonenumbers import PhoneNumberMatcher

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
    phones = []
    for match in PhoneNumberMatcher(text, "US"):  # Use the appropriate country code
        phones.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
    return phones

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
                        phones.add(phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164))
                except phonenumbers.NumberParseException:
                    continue
        except (json.JSONDecodeError, TypeError):
            continue
    return list(phones)
