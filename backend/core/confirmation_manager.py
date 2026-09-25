import uuid
from typing import Dict, Any


# Temporary in-memory storage for pending confirmations
_pending_confirmations: Dict[str, Dict[str, Any]] = {}


def create_confirmation(
    action: str,
    recipient: str,
    subject: str,
    body: str
) -> Dict[str, Any]:
    """
    Create a pending confirmation for an action.
    """

    confirmation_id = str(uuid.uuid4())

    confirmation = {
        "confirmation_id": confirmation_id,
        "action": action,
        "recipient": recipient,
        "subject": subject,
        "body": body,
        "status": "pending"
    }

    _pending_confirmations[confirmation_id] = confirmation

    return confirmation


def get_confirmation(confirmation_id: str) -> Dict[str, Any] | None:
    """
    Get a pending confirmation by its ID.
    """

    return _pending_confirmations.get(confirmation_id)


def confirm_confirmation(confirmation_id: str) -> Dict[str, Any] | None:
    """
    Mark a pending confirmation as confirmed.
    """

    confirmation = _pending_confirmations.get(confirmation_id)

    if confirmation is None:
        return None

    if confirmation["status"] != "pending":
        return confirmation

    confirmation["status"] = "confirmed"

    return confirmation


def cancel_confirmation(confirmation_id: str) -> Dict[str, Any] | None:
    """
    Cancel a pending confirmation.
    """

    confirmation = _pending_confirmations.get(confirmation_id)

    if confirmation is None:
        return None

    if confirmation["status"] != "pending":
        return confirmation

    confirmation["status"] = "cancelled"

    return confirmation


def remove_confirmation(confirmation_id: str) -> None:
    """
    Remove a confirmation from temporary storage.
    """

    _pending_confirmations.pop(confirmation_id, None)