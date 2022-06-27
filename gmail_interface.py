from __future__ import print_function

import base64
from email.message import EmailMessage

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GmailInterface:
    @staticmethod
    def send_email(creds, src, dest, subject, content):
        """
            Sends an email from 'src' to 'dest' containing 'content'
            Args:
                creds: Google login credentials
                src: The address the email is sent from
                dest: The address the email is sent to
                subject: The subject header of the email
                content: The content of the email
        """

        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=creds)

            # Create message
            message = EmailMessage()
            message.set_content(content)
            message["To"] = src
            message["From"] = dest
            message["Subject"] = subject

            # Encode the message
            encoded_message = base64.urlsafe_b64encode(
                message.as_bytes()).decode()

            # Send the message
            send_message = (service.users().messages().send(
                userId="me", body={"raw": encoded_message}
            ).execute())
            print(f"Message ID: {send_message['id']} has been sent")

        except HttpError as error:
            print(f'An error occurred: {error}')
