# Django Imports
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Module Imports
from applibs.logger import get_logger

logger = get_logger(__name__)

def sanitize_email(email: str) -> str | None:
    if not email:
        logger.error("Email is not present")
        return None

    # Sanitize email
    email = str(email).lower().strip()

    try:
        validate_email(email)
    except ValidationError:
        logger.error(f"Email is not valid: {email}")
        return None

    return email