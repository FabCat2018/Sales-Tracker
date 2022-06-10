from __future__ import print_function

import re

from google_doc_mapper import GoogleDocMapper

# The ID of a sample document.
DOCUMENT_ID = '1EDpqzYphtaxSEcgQ6RBrkLehytIMaHePPSvxyO68Em0'


class SalesTracker:
    def run(self):
        ### Get games we are interested in from Google Doc ###
        games_of_interest = self.getGamesFromDoc()
        print(games_of_interest)

        ### Scrape webpage for list of games on sale ###
        # games_on_sale = getGamesOnSale()

        ### Find the intersection of both lists ###
        # intersection = ...

        ### Send intersection via email, including links to purchase games ###

        ### Extension: Run as cron job ###

        ### Extension: Allow budget to be set for max game on sale can cost ###

    def getGamesFromDoc(self):
        """Gets the list of 'To Play' games from the Google Doc"""

        # Get the raw content from the Google Doc
        mapper = GoogleDocMapper()
        raw_content = mapper.get_doc_content(DOCUMENT_ID)

        # Remove all empty entries from raw_content, only keeping paragraphs
        all_paragraphs = [
            game for game in raw_content if "paragraph" in game]

        [games, heading_indexes] = mapper.map_to_entries_and_headings(
            all_paragraphs)

        # Structure of doc means "To Play" games are always at the start
        games_to_play = games[heading_indexes[0] + 1: heading_indexes[1]]

        # Remove all entries which are line breaks
        games_to_play_no_whitespace = [
            game for game in games_to_play if game != "\n"]

        # Remove undesirable characters from game titles
        sanitised_games_to_play = []
        pattern = re.compile(r"\s\s*$")
        for game in games_to_play_no_whitespace:
            game_title = game.replace("(NYA)", "").replace("(NYR)", "")
            sanitised_games_to_play.append(re.sub(pattern, "", game_title))

        return sanitised_games_to_play


sales_tracker = SalesTracker()
sales_tracker.run()
