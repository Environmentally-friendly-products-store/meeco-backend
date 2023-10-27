import base64
import os.path
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def gmail_send_message(mail_to_address, subject, message_text):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(message_text)
        message["To"] = mail_to_address
        message["From"] = "ecome.bestonlineshop@gmail.com"
        message["Subject"] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )

    except HttpError:
        send_message = None
    return send_message


if __name__ == "__main__":
    gmail_send_message()
