from __future__ import print_function

import re

from google_doc_mapper import GoogleDocMapper
from web_scraper import WebScraper

# The ID of the Google Doc
DOCUMENT_ID = '1EDpqzYphtaxSEcgQ6RBrkLehytIMaHePPSvxyO68Em0'


class SalesTracker:
    def run(self):
        ### Get games we are interested in from Google Doc ###
        games_of_interest = self._get_games_from_doc()

        ### Scrape webpage for list of games on sale ###
        games_on_sale = self._get_games_on_sale()

        ### Find the intersection of both lists ###
        formatted_games_of_interest = self._format_game_strings(
            games_of_interest)
        formatted_games_on_sale = self._format_game_strings(games_on_sale)
        full_matches = set(formatted_games_of_interest) & set(
            formatted_games_on_sale)

        partial_matches = set()
        for game_to_buy_title in formatted_games_of_interest:
            for game_on_sale_title in formatted_games_on_sale:
                if game_to_buy_title in game_on_sale_title:
                    partial_matches.add(game_on_sale_title)

        intersection = list(set(full_matches | partial_matches))
        print(intersection)

        ### Send intersection via email, including links to purchase games ###

        ### Extension: Run as cron job ###

        ### Extension: Allow budget to be set for max game on sale can cost ###

    def _get_games_from_doc(self):
        """Gets the list of 'To Play' games from the Google Doc"""

        # Get the raw content from the Google Doc
        mapper = GoogleDocMapper()
        raw_content = mapper.get_doc_content(DOCUMENT_ID)

        # Remove all empty entries from raw_content, only keeping paragraphs
        all_paragraphs = [game for game in raw_content if "paragraph" in game]

        [games, heading_indexes] = mapper.map_to_entries_and_headings(
            all_paragraphs)

        # Structure of doc means "To Play" games are always at the start
        games_to_play = games[heading_indexes[0] + 1: heading_indexes[1]]

        # Remove all entries which are just whitespace
        games_to_play_no_whitespace = mapper.remove_newlines(games_to_play)

        # Remove undesirable characters from game titles
        sanitised_games_to_play = []
        pattern = re.compile(r"\s\s*$")
        for game in games_to_play_no_whitespace:
            game_title = game.replace("(NYA)", "").replace("(NYR)", "")
            sanitised_games_to_play.append(re.sub(pattern, "", game_title))

        return sanitised_games_to_play

    def _get_games_on_sale(self):
        """Gets the list of games on sale from desired sites"""

        website_url = "https://www.trueachievements.com"
        web_scraper = WebScraper()

        # Get the URL of the latest sales page
        start_page = web_scraper.get_webpage(website_url)
        articles = web_scraper.get_elements_by_selector(
            start_page, "article > a")
        article_names = list(map(
            lambda article: {"title": article.get_text(), "link": article["href"]}, articles))
        sales_articles = list(filter(
            lambda article: "sale round-up" in article["title"].lower(), article_names))
        sales_page_url = website_url + sales_articles[0]["link"]

        # Get the raw webpage from the latest sales page URL
        raw_page = web_scraper.get_webpage(sales_page_url)

        # Find the sections on the page to scrape
        sections_of_interest = ["Xbox One Bundles & Special Editions", "Xbox One Games", "Xbox One DLC",
                                "Xbox 360 (backwards compatible) Games",
                                "Xbox 360 (backwards compatible) DLC"]

        sections = web_scraper.get_all_matching_elements(raw_page, "h3", {})
        section_names = [section.text for section in sections]
        sections_to_scrape = list(
            set(sections_of_interest) & set(section_names))

        # Scrape sections for games
        games_on_sale = []
        for section in sections_to_scrape:
            section_header = web_scraper.get_first_matching_element(
                raw_page, "h3", {"string": section})

            section_sales_div = web_scraper.get_next_sibling(section_header)
            table_rows = web_scraper.get_elements_by_selector(
                section_sales_div, "table > tbody > tr")

            ### Extension: Add prices into result set, as on same row ###

            for row in table_rows:
                web_scraper.get_first_matching_element(row, "td", {})
                game_titles = row.find("td").find_all("a")
                games_on_sale.extend([title.text for title in game_titles])

        return games_on_sale

    def _format_game_strings(self, collection):
        """
            Formats all strings in 'collection'

            Args:
                collection: The collection to format; iterable
        """

        collection_stripped = self._strip_characters(collection)
        return self._replace_quotes(collection_stripped)

    def _strip_characters(self, collection):
        """
            Strips undesirable characters from all strings in 'collection'

            Args:
                collection: The collection to remove characters from; iterable
        """

        return list(
            map(
                lambda entry: entry.replace(u"\u00a9", "")
                .replace(u"\u00ae", "")
                .replace(u"\u2117", "")
                .replace(u"\u2120", "")
                .replace(u"\u2122", ""),
                collection
            )
        )

    def _replace_quotes(self, collection):
        """
            Standardises quotes for all strings in 'collection'

            Args:
                collection: The collection to change quotes for; iterable
        """

        return list(map(lambda entry: entry.replace("'", "’"), collection))


sales_tracker = SalesTracker()
sales_tracker.run()
