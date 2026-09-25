import os
import base64
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from core.confirmation_manager import create_confirmation
# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

CREDENTIALS_FILE = os.path.join(
    BASE_DIR,
    "credentials.json"
)

TOKEN_FILE = os.path.join(
    BASE_DIR,
    "token.json"
)


# --------------------------------------------------
# GMAIL PERMISSIONS
# --------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]


# --------------------------------------------------
# CONNECT TO GMAIL
# --------------------------------------------------

def get_gmail_service():

    creds = None

    # Existing login token
    if os.path.exists(TOKEN_FILE):

        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    # Token invalid or expired
    if not creds or not creds.valid:

        if (
            creds
            and creds.expired
            and creds.refresh_token
        ):

            creds.refresh(Request())

        else:

            if not os.path.exists(CREDENTIALS_FILE):

                raise FileNotFoundError(
                    "credentials.json not found inside backend folder."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

        # Save login token
        with open(TOKEN_FILE, "w") as token:

            token.write(
                creds.to_json()
            )

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service


# --------------------------------------------------
# TEST CONNECTION
# --------------------------------------------------

def test_gmail_connection():

    try:

        service = get_gmail_service()

        profile = (
            service
            .users()
            .getProfile(userId="me")
            .execute()
        )

        return {
            "status": "success",
            "email": profile.get("emailAddress"),
            "message": "Gmail connected successfully."
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# --------------------------------------------------
# SEND EMAIL
# --------------------------------------------------

def send_email(
    recipient,
    subject,
    body
):

    try:

        service = get_gmail_service()

        message = MIMEText(body)

        message["to"] = recipient
        message["subject"] = subject

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        create_message = {
            "raw": encoded_message
        }

        sent_message = (
            service
            .users()
            .messages()
            .send(
                userId="me",
                body=create_message
            )
            .execute()
        )

        return {
            "status": "success",
            "message": "Email sent successfully.",
            "message_id": sent_message.get("id"),
            "recipient": recipient,
            "subject": subject
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# --------------------------------------------------
# CREATE DRAFT
# --------------------------------------------------

def create_email_draft(
    recipient,
    subject,
    body
):

    try:

        service = get_gmail_service()

        message = MIMEText(body)

        message["to"] = recipient
        message["subject"] = subject

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        draft_body = {
            "message": {
                "raw": encoded_message
            }
        }

        draft = (
            service
            .users()
            .drafts()
            .create(
                userId="me",
                body=draft_body
            )
            .execute()
        )

        return {
            "status": "success",
            "message": "Email draft created successfully.",
            "draft_id": draft.get("id"),
            "recipient": recipient,
            "subject": subject
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# --------------------------------------------------
# LIST UNREAD EMAILS
# --------------------------------------------------

def list_unread_emails(
    max_results=10
):

    try:

        service = get_gmail_service()

        response = (
            service
            .users()
            .messages()
            .list(
                userId="me",
                q="is:unread",
                maxResults=max_results
            )
            .execute()
        )

        messages = response.get(
            "messages",
            []
        )

        results = []

        for message in messages:

            message_data = (
                service
                .users()
                .messages()
                .get(
                    userId="me",
                    id=message["id"],
                    format="metadata",
                    metadataHeaders=[
                        "From",
                        "To",
                        "Subject",
                        "Date"
                    ]
                )
                .execute()
            )

            headers = message_data.get(
                "payload",
                {}
            ).get(
                "headers",
                []
            )

            email_info = {
                "id": message["id"],
                "from": "",
                "to": "",
                "subject": "",
                "date": ""
            }

            for header in headers:

                name = header.get("name")
                value = header.get("value")

                if name == "From":
                    email_info["from"] = value

                elif name == "To":
                    email_info["to"] = value

                elif name == "Subject":
                    email_info["subject"] = value

                elif name == "Date":
                    email_info["date"] = value

            results.append(email_info)

        return {
            "status": "success",
            "count": len(results),
            "emails": results
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# --------------------------------------------------
# SEARCH EMAILS
# --------------------------------------------------

def search_emails(
    query,
    max_results=10
):

    try:

        service = get_gmail_service()

        response = (
            service
            .users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=max_results
            )
            .execute()
        )

        messages = response.get(
            "messages",
            []
        )

        results = []

        for message in messages:

            message_data = (
                service
                .users()
                .messages()
                .get(
                    userId="me",
                    id=message["id"],
                    format="metadata",
                    metadataHeaders=[
                        "From",
                        "To",
                        "Subject",
                        "Date"
                    ]
                )
                .execute()
            )

            headers = message_data.get(
                "payload",
                {}
            ).get(
                "headers",
                []
            )

            email_info = {
                "id": message["id"],
                "from": "",
                "to": "",
                "subject": "",
                "date": ""
            }

            for header in headers:

                name = header.get("name")
                value = header.get("value")

                if name == "From":
                    email_info["from"] = value

                elif name == "To":
                    email_info["to"] = value

                elif name == "Subject":
                    email_info["subject"] = value

                elif name == "Date":
                    email_info["date"] = value

            results.append(email_info)

        return {
            "status": "success",
            "query": query,
            "count": len(results),
            "emails": results
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# --------------------------------------------------
# READ EMAIL
# --------------------------------------------------

def read_email(
    message_id
):

    try:

        service = get_gmail_service()

        message = (
            service
            .users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full"
            )
            .execute()
        )

        payload = message.get(
            "payload",
            {}
        )

        headers = payload.get(
            "headers",
            []
        )

        email_info = {
            "id": message_id,
            "from": "",
            "to": "",
            "subject": "",
            "date": "",
            "body": ""
        }

        for header in headers:

            name = header.get("name")
            value = header.get("value")

            if name == "From":
                email_info["from"] = value

            elif name == "To":
                email_info["to"] = value

            elif name == "Subject":
                email_info["subject"] = value

            elif name == "Date":
                email_info["date"] = value

        # Extract email body
        body = ""

        if "parts" in payload:

            for part in payload["parts"]:

                if part.get("mimeType") == "text/plain":

                    data = (
                        part
                        .get("body", {})
                        .get("data")
                    )

                    if data:

                        body = base64.urlsafe_b64decode(
                            data
                        ).decode(
                            "utf-8",
                            errors="ignore"
                        )

                        break

        else:

            data = (
                payload
                .get("body", {})
                .get("data")
            )

            if data:

                body = base64.urlsafe_b64decode(
                    data
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

        email_info["body"] = body

        return {
            "status": "success",
            "email": email_info
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
def prepare_email_send(
    recipient: str,
    subject: str,
    body: str
):
    """
    Prepare an email for sending.
    The email is NOT sent here.
    User confirmation is required before sending.
    """

    if not recipient:
        return {
            "status": "error",
            "message": "Recipient email address is required."
        }

    if not subject:
        return {
            "status": "error",
            "message": "Email subject is required."
        }

    if not body:
        return {
            "status": "error",
            "message": "Email body is required."
        }

    confirmation = create_confirmation(
        action="send_email",
        recipient=recipient,
        subject=subject,
        body=body
    )

    return {
        "status": "pending_confirmation",
        "message": "Email prepared. User confirmation is required before sending.",
        "confirmation_id": confirmation["confirmation_id"],
        "recipient": recipient,
        "subject": subject,
        "body": body
    }