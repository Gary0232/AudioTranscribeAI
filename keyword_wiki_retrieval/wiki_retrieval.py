import pywikibot
import mwparserfromhell
from PIL import Image

# Function to retrieve information from Wikipedia

def get_wikipedia_info(query, lang='en'):
    try:
        # Set the Wikipedia site language and initialize
        site = pywikibot.Site(lang, "wikipedia")
        page = pywikibot.Page(site, query)

        # Retrieve the page title, URL, and text
        title = page.title()
        url = page.full_url()
        wikitext = page.text
        parsed = mwparserfromhell.parse(wikitext)

        # Extract image URLs from the parsed content
        image_titles = [x.title.strip_code().strip() for x in parsed.filter_wikilinks() if
                        x.title.startswith("File:")]

        # Fetch actual URLs for the images
        images_url = []
        for image_title in image_titles:
            image_page = pywikibot.FilePage(site, image_title)
            image_url = image_page.full_url()
            images_url.append(image_url)
        # Extract the first 500 characters of text as a summary
        summary = parsed.strip_code().strip()[0:500]

        # Return the title, URL, summary, and images
        return title, url, summary, images_url
    except pywikibot.exceptions.PageRelatedError as e:
        # Handle errors, such as missing pages
        return f"Error: {e}", None, None, None


if __name__ == '__main__':
    # Example usage
    keyword = "Wine"
    title, url, summary, image = get_wikipedia_info(keyword)
    print(f"title: {title}\n url: {url}\n summary: {summary}\n image: {image}\n")

