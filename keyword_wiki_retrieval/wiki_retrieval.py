import pywikibot


# Function to retrieve information from Wikipedia
def get_wikipedia_info(query, lang='en'):
    try:
        # Set language of Wikipedia you want to search
        site = pywikibot.Site(lang, "wikipedia")

        # Search for the query on Wikipedia
        page = pywikibot.Page(site, query)

        # Retrieve title, URL, and summary of the Wikipedia page
        title = page.title()
        url = page.full_url()
        summary = page.text[:500]  # Extracting first 500 characters as summary

        return title, url, summary
    except pywikibot.exceptions.PageRelatedError as e:
        # If the page doesn't exist or other related errors occur, handle it
        return f"Error: {e}", None, None


if __name__ == '__main__':
    # Example usage
    keyword = "Wine"
    print(get_wikipedia_info(keyword))