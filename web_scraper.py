from bs4 import BeautifulSoup
import requests


class WebScraper:
    # Main method
    def get_webpage(self, url):
        """
            Gets the content of the specified webpage as a BS4 object

            Args:
                url: The URL of the webpage to get content from
        """

        # Fetch the webpage
        webpage = requests.get(url)

        # Create the object that will contain all the info in the URL
        return BeautifulSoup(webpage.text, "lxml")

    def get_first_matching_element(self, soup, tag, attrs):
        """
            Gets the first element of 'soup' which matches 'tag' and 'attrs', as a new BS4 object

            Args:
                soup: A BS4 object
                tag: The element type to match against
                attrs: Any extra attributes to include in matching, e.g. className, id; dict
        """

        return soup.find(tag, **attrs)

    def get_all_matching_elements(self, soup, tag, attrs):
        """
            Gets a list of elements from 'soup' which match 'tag' and 'attrs'

            Args:
                soup: A BS4 object
                tag: The element type to match against, a string
                attrs: Any extra attributes to include in matching, e.g. className, id, etc., iterable
        """

        return soup.find_all(tag, **attrs)

    def get_next_sibling(self, element):
        """
            Gets the next element on the same level as 'element', as a new BS4 object

            Args:
                element: A BS4 object
        """

        return element.next_sibling

    def get_elements_by_selector(self, soup, selector):
        """
            Gets a list of elements from 'soup' which match 'selector'

            Args:
                soup: A BS4 object
                selector: The CSS selector to match against, a string
        """

        return soup.select(selector)
