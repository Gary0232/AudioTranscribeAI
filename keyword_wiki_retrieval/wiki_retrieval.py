import pywikibot
import mwparserfromhell


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
        wikitext = page.text  # Extracting first 500 characters as summary
        parsed = mwparserfromhell.parse(wikitext)
        templates = parsed.filter_templates()

        # print the template names and parameters
        for template in templates:
            print(f"Template name: {template.name}")
            for param in template.params:
                print(f"  {param.name}: {param.value}")

        # retrieve all categories in the page
        categories = [x.title.strip_code() for x in parsed.filter_wikilinks() if x.title.startswith("Category:")]
        print(categories)
        # preview the first 500 characters of the page
        print(parsed.strip_code().strip()[0:500])
        # preview the first 500 characters of the wikitext
        print(wikitext[0:500])

        return title, url, parsed
    except pywikibot.exceptions.PageRelatedError as e:
        # If the page doesn't exist or other related errors occur, handle it
        return f"Error: {e}", None, None


if __name__ == '__main__':
    # Example usage
    keyword = "Wine"
    get_wikipedia_info(keyword)
