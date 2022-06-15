import os.path
import string

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']


class GoogleDocMapper:
    def get_doc_content(self, documentId):
        """
            Gets the content of the specified Google Doc

            Args:
                documentId: The ID of the Google Doc to be retrieved
        """

        creds = self._get_credentials()

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

    def _get_credentials(self):
        """Gets the login credentials for the Google Doc"""

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds

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
