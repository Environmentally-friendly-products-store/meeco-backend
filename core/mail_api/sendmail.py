import os

import requests
from dotenv import load_dotenv

load_dotenv()

X_API_KEY = os.environ["X_API_KEY"]
MAIL_URL = os.environ["MAIL_URL"]
MAIL_FROM_ADDRESS = os.environ["MAIL_FROM_ADDRESS"]
MAIL_FROM_NAME = os.environ["MAIL_FROM_NAME"]


def send_email(email_to_address, email_to_name, subject, message):
    json = {
        "mail": {
            "to": {
                "email": email_to_address,
                "name": email_to_name,
            },
            "from": {
                "email": MAIL_FROM_ADDRESS,
                "name": MAIL_FROM_NAME,
            },
            "subject": subject,
            "html": message,
        }
    }
    headers = {"X-Api-Key": X_API_KEY}
    return requests.post(MAIL_URL, json=json, headers=headers)
