# from agents.email_agent import search_emails


# result = search_emails(
#     "in:anywhere",
#     max_results=5
# )

# print(result)
# from agents.email_agent import list_unread_emails


# result = list_unread_emails(
#     max_results=5
# )

# print(result)

from agents.email_agent import read_email


message_id = "1a0d1d60f595855a"

result = read_email(message_id)

print(result)
from agents.email_agent import create_email_draft


result = create_email_draft(
    recipient="rishithagopathi@gmail.com",
    subject="DeskPilot Test Draft",
    body="Hello Rishitha,\n\nThis is a test draft created by DeskPilot.\n\nRegards,\nDeskPilot"
)

print(result)