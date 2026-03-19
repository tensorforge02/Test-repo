# notifier.py - Basic email notification module (version 1)

import smtplib


def send_email(to, subject, body, smtp_host, smtp_port, username, password):
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.login(username, password)
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(username, to, message)
    server.quit()


def send_bulk_emails(recipients, subject, body, smtp_host, smtp_port, username, password):
    for recipient in recipients:
        send_email(recipient, subject, body, smtp_host, smtp_port, username, password)


def format_subject(subject):
    return "[NOTIFY] " + subject


def is_valid_email(email):
    return "@" in email and "." in email