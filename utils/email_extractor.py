import re
import json
from typing import List

# Compilation préalable des expressions régulières pour des performances optimisées
EMAIL_HTML_REGEX = re.compile(
    r'(?<![a-zA-Z0-9_.+-])'  # Assertion négative pour s'assurer que l'email n'est pas précédé de caractères valides
    r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?)'  # Capture de l'email avec un TLD optionnel supplémentaire
    r'(?!\.\w+)'  # Assertion négative pour exclure les sous-domaines indésirables
)

# Expression régulière pour détecter et supprimer les commentaires HTML
HTML_COMMENT_REGEX = re.compile(r'<!--.*?-->', re.DOTALL)

def extract_emails_html(text: str) -> List[str]:
    """
    Extrait les adresses email du contenu HTML ou texte brut.

    Cette fonction nettoie le texte en supprimant les commentaires HTML,
    puis utilise une expression régulière compilée pour trouver les
    adresses email valides. Elle est conçue pour exclure les emails
    contenant des sous-domaines indésirables.

    Args:
        text (str): Le contenu HTML ou texte brut à analyser.

    Returns:
        List[str]: Une liste d'adresses email extraites et valides.
    """
    # Supprimer les commentaires HTML pour éviter d'extraire des emails cachés
    text_no_comments = HTML_COMMENT_REGEX.sub('', text)

    # Trouver toutes les correspondances d'emails dans le texte nettoyé
    emails = EMAIL_HTML_REGEX.findall(text_no_comments)

    return emails

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
    valid_emails = [
        email for email in all_emails
        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) 
        and not re.match(r'^[a-f0-9]{32}@sentry\.zipify\.com$', email)
    ]
    return valid_emails
