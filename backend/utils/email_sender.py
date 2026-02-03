"""
Email Sender Utility
Sends emails using SMTP
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    """
    Handles sending emails via SMTP
    """

    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_email = os.getenv('SMTP_EMAIL')
        self.smtp_password = os.getenv('SMTP_PASSWORD')

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachments: list = None,
        cc_email: str = None
    ) -> dict:
        """
        Send an email with optional attachments

        Args:
            to_email: Recipient email
            subject: Email subject
            body: Email body (HTML or plain text)
            attachments: List of file paths to attach
            cc_email: CC recipient email

        Returns:
            Dictionary with success status
        """
        if not self.smtp_email or not self.smtp_password:
            print("⚠️ SMTP credentials not configured. Skipping email send.")
            return {'success': False, 'error': 'SMTP credentials missing'}

        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_email
            msg['To'] = to_email
            msg['Subject'] = subject
            if cc_email:
                msg['Cc'] = cc_email

            msg.attach(MIMEText(body, 'html'))

            # Add attachments
            if attachments:
                for filepath in attachments:
                    if os.path.exists(filepath):
                        with open(filepath, "rb") as f:
                            part = MIMEApplication(
                                f.read(),
                                Name=os.path.basename(filepath)
                            )
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(filepath)}"'
                        msg.attach(part)

            # Connect and send
            recipients = [to_email]
            if cc_email:
                recipients.append(cc_email)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_email, self.smtp_password)
                server.sendmail(self.smtp_email, recipients, msg.as_string())

            return {'success': True}

        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return {'success': False, 'error': str(e)}

# Mock sender for development when no credentials
class MockEmailSender:
    def send_email(self, to_email, subject, body, attachments=None, cc_email=None):
        print(f"📧 [MOCK EMAIL] To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Attachments: {attachments}")
        return {'success': True, 'mock': True}
