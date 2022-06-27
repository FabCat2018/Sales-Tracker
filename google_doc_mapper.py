from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDocMapper:
    def get_doc_content(self, creds, documentId):
        """
            Gets the content of the specified Google Doc

            Args:
                creds: Google login credentials
                documentId: The ID of the Google Doc to be retrieved
        """

        try:
            service = build('docs', 'v1', credentials=creds)

            # Retrieve the document contents from the Docs service.
            document = service.documents().get(documentId=documentId).execute()
            content = document.get("body").get("content")

            return content
        except HttpError as err:
            print(err)

    def map_to_entries_and_headings(self, all_paragraphs):
        """
            Maps Doc data to list of line entries, tracking which indexes are Headings

            Args:
                all_paragraphs: All ParagraphElements from a Google Doc
        """

        entries = []
        heading_indexes = []
        for i in range(len(all_paragraphs)):
            value = all_paragraphs[i]
            paragraph = value.get("paragraph")
            elements = paragraph.get("elements")

            if (self._is_paragraph_heading(paragraph)):
                heading_indexes.append(i)

            for elem in elements:
                entries.append(self._read_paragraph_element(elem))

        return [entries, heading_indexes]

    def remove_newlines(self, entries):
        """
            Removes any entries from a Google Doc which are just newlines

            Args:
                entries: The individual entries from the Doc
        """

        return [entry for entry in entries if entry != "\n"]

    def _is_paragraph_heading(self, paragraph):
        """
            Returns whether a paragraph is a Heading

            Args:
                paragraph: A ParagraphElement from a Google Doc
        """

        return paragraph.get("paragraphStyle").get("namedStyleType") == "HEADING_1"

    def _read_paragraph_element(self, element):
        """
            Returns the text in the given ParagraphElement

            Args:
                element: A ParagraphElement from a Google Doc
        """

        text_run = element.get("textRun")
        if not text_run:
            return ""
        return text_run.get("content")
