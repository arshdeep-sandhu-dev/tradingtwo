#!/usr/bin/env python3
"""
send_email.py — Send an email from Python via SMTP.

Credentials are read from environment variables so you never hardcode a
password into the file:

    EMAIL_ADDRESS   your full email address (e.g. you@gmail.com)
    EMAIL_PASSWORD  your password or app-specific password

Quick start (Gmail):
    1. Turn on 2-Step Verification on your Google account.
    2. Create an "App Password": https://myaccount.google.com/apppasswords
    3. Export the variables in your terminal:
         export EMAIL_ADDRESS="you@gmail.com"
         export EMAIL_PASSWORD="the-16-char-app-password"
    4. Run it:
         python3 send_email.py

For other providers, just change SMTP_SERVER and SMTP_PORT below.
"""

import os
import sys
import smtplib
import ssl
from email.message import EmailMessage

# Load variables from a local .env file if python-dotenv is installed.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- SMTP settings (defaults are for Gmail) ---------------------------------
SMTP_SERVER = "smtp.gmail.com"   # Outlook: smtp.office365.com | Yahoo: smtp.mail.yahoo.com
SMTP_PORT = 465                  # 465 = SSL. Use 587 if your provider requires STARTTLS.


def send_email(to_address, subject, body, attachments=None):
    """
    Send a plain-text email, optionally with file attachments.

    Args:
        to_address (str | list[str]): recipient(s)
        subject (str): subject line
        body (str): plain-text message body
        attachments (list[str] | None): optional list of file paths to attach
    """
    sender = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")

    if not sender or not password:
        raise RuntimeError(
            "Set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables first."
        )

    # Normalize recipients to a list
    recipients = [to_address] if isinstance(to_address, str) else list(to_address)

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    # Attach any files
    for path in attachments or []:
        with open(path, "rb") as f:
            data = f.read()
        filename = os.path.basename(path)
        msg.add_attachment(
            data,
            maintype="application",
            subtype="octet-stream",
            filename=filename,
        )

    # Send over an encrypted connection
    context = ssl.create_default_context()
    if SMTP_PORT == 465:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(sender, password)
            server.send_message(msg)
    else:  # 587 / STARTTLS
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(sender, password)
            server.send_message(msg)

    print(f"Email sent to {', '.join(recipients)}")


if __name__ == "__main__":
    # Usage: python trading_email.py "your message" ["optional subject"]
    body = sys.argv[1] if len(sys.argv) > 1 else "Hello!\n\nThis message was sent from a Python script.\n"
    subject = sys.argv[2] if len(sys.argv) > 2 else "Test email from Python"
    send_email(
        to_address=os.environ.get("EMAIL_ADDRESS"),  # sends to yourself by default
        subject=subject,
        body=body,
        # attachments=["report.pdf"],  # uncomment to attach files
    )
