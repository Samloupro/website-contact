@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url or not is_valid_url(url):
        return jsonify({'error': 'Invalid URL provided.'}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links_html = extract_links_html(soup, url)
        links_jsonld = extract_links_jsonld(soup, url)
        links = set(links_html + links_jsonld)  # Combine and deduplicate links

        emails = {}
        phones = {}
        social_links = extract_social_links_jsonld(soup)
        visited_links = set()
        domain = urlparse(url).netloc

        for link in links:  # Analyze all links
            if link in visited_links or urlparse(link).netloc != domain:
                continue
            visited_links.add(link)
            try:
                sub_response = requests.get(link, headers=headers, timeout=10)
                sub_response.raise_for_status()
                sub_soup = BeautifulSoup(sub_response.text, 'html.parser')

                sub_emails = extract_emails_html(sub_soup.text) + extract_emails_jsonld(sub_soup)
                for email in set(sub_emails):
                    if email not in emails:
                        emails[email] = []
                    emails[email].append(link)

                sub_phones = extract_phones_html(sub_soup.text) + extract_phones_jsonld(sub_soup)
                for phone in set(validate_phones(sub_phones)):
                    if phone not in phones:
                        phones[phone] = []
                    phones[phone].append(link)
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to process link {link}: {e}")
                continue

        result = {
            "request_id": str(uuid.uuid4()),
            "domain": url.split("//")[-1].split("/")[0],
            "query": url,
            "status": "OK",
            "data": [
                {
                    "emails": [{"value": email, "sources": sources} for email, sources in emails.items()],
                    "phone_numbers": [{"value": phone, "sources": sources} for phone, sources in phones.items()],
                    "social_links": {
                        "facebook": social_links.get("facebook"),
                        "github": social_links.get("github"),
                        "instagram": social_links.get("instagram"),
                        "linkedin": social_links.get("linkedin"),
                        "pinterest": social_links.get("pinterest"),
                        "snapchat": social_links.get("snapchat"),
                        "tiktok": social_links.get("tiktok"),
                        "twitter": social_links.get("twitter"),
                        "youtube": social_links.get("youtube")
                    },
                    "unique_links": sorted(list(visited_links))  # Add unique links to the result in alphabetical order
                }
            ]
        }

        logger.info(f"Processed URL: {url}")
        return jsonify(result)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error accessing the URL: {e}")
        return jsonify({'error': f"Error accessing the URL: {str(e)}"}), 500
