# notifier.py - Email notification module (version 2 — improved)

import smtplib
import logging
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")


@dataclass
class SMTPConfig:
    """Holds SMTP connection settings cleanly instead of passing 5+ arguments."""
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True


def is_valid_email(email: str) -> bool:
    """Validate an email address using a proper regex pattern."""
    return bool(EMAIL_REGEX.match(email.strip()))


def build_message(sender: str, recipient: str, subject: str, body: str) -> MIMEMultipart:
    """
    Build a properly formatted MIME email message.
    Supports both plain text and future HTML bodies.
    """
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = format_subject(subject)
    msg.attach(MIMEText(body, "plain"))
    return msg


def format_subject(subject: str) -> str:
    """Prefix subject with [NOTIFY] tag, stripping extra whitespace."""
    return f"[NOTIFY] {subject.strip()}"


def send_email(
    config: SMTPConfig,
    recipient: str,
    subject: str,
    body: str,
) -> bool:
    """
    Send a single email using SMTP with TLS support.

    Args:
        config: SMTP connection settings.
        recipient: Recipient email address.
        subject: Email subject line.
        body: Plain text email body.

    Returns:
        True if sent successfully, False otherwise.
    """
    if not is_valid_email(recipient):
        logger.error("Invalid recipient email address: %s", recipient)
        return False

    msg = build_message(config.username, recipient, subject, body)

    try:
        with smtplib.SMTP(config.host, config.port, timeout=10) as server:
            if config.use_tls:
                server.starttls()
            server.login(config.username, config.password)
            server.sendmail(config.username, recipient, msg.as_string())
            logger.info("Email sent to %s", recipient)
            return True
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed for user: %s", config.username)
    except smtplib.SMTPException as e:
        logger.error("SMTP error sending to %s: %s", recipient, e)
    except OSError as e:
        logger.error("Network error sending to %s: %s", recipient, e)
    return False


def send_bulk_emails(
    config: SMTPConfig,
    recipients: list[str],
    subject: str,
    body: str,
) -> dict[str, bool]:
    """
    Send emails to multiple recipients, reusing a single SMTP connection.

    Args:
        config: SMTP connection settings.
        recipients: List of recipient email addresses.
        subject: Email subject line.
        body: Plain text email body.

    Returns:
        Dict mapping each recipient to True (sent) or False (failed).
    """
    results: dict[str, bool] = {}
    valid = [r for r in recipients if is_valid_email(r)]
    invalid = [r for r in recipients if not is_valid_email(r)]

    for addr in invalid:
        logger.warning("Skipping invalid email: %s", addr)
        results[addr] = False

    if not valid:
        return results

    try:
        with smtplib.SMTP(config.host, config.port, timeout=10) as server:
            if config.use_tls:
                server.starttls()
            server.login(config.username, config.password)

            for recipient in valid:
                try:
                    msg = build_message(config.username, recipient, subject, body)
                    server.sendmail(config.username, recipient, msg.as_string())
                    logger.info("Bulk email sent to %s", recipient)
                    results[recipient] = True
                except smtplib.SMTPException as e:
                    logger.error("Failed to send to %s: %s", recipient, e)
                    results[recipient] = False
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP authentication failed")
        for r in valid:
            results[r] = False
    except OSError as e:
        logger.error("Network error during bulk send: %s", e)
        for r in valid:
            results.setdefault(r, False)

    return results