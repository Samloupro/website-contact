import re

def extract_social_links(unique_links):
    social_links = {
        "facebook": None,
        "instagram": None,
        "twitter": None,
        "tiktok": None,
        "linkedin": None,
        "youtube": None,
        "pinterest": None,
        "github": None,
        "snapchat": None
    }

    # Define regex patterns for social media links
    patterns = {
        "facebook": re.compile(r"(https?://(www\.)?facebook\.com/[^\s/]+)"),
        "instagram": re.compile(r"(https?://(www\.)?instagram\.com/[^\s/]+)"),
        "twitter": re.compile(r"(https?://(www\.)?twitter\.com/[^\s/]+)"),
        "tiktok": re.compile(r"(https?://(www\.)?tiktok\.com/@[^\s/]+)"),
        "linkedin": re.compile(r"(https?://(www\.)?linkedin\.com/in/[^\s/]+)"),
        "youtube": re.compile(r"(https?://(www\.)?youtube\.com/(channel|user)/[^\s/]+)"),
        "pinterest": re.compile(r"(https?://(www\.)?pinterest\.com/[^\s/]+)"),
        "github": re.compile(r"(https?://(www\.)?github\.com/[^\s/]+)"),
        "snapchat": re.compile(r"(https?://(www\.)?snapchat\.com/add/[^\s/]+)")
    }

    for link in unique_links:
        for key, pattern in patterns.items():
            if not social_links[key]:  # Only update if the link is not already found
                match = pattern.search(link)
                if match:
                    social_links[key] = match.group(0)
                    print(f"Found {key.capitalize()} link: {social_links[key]}")

    return social_links
