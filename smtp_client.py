import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SmtpClient:
    def __init__(self, username, password, server, port):
        """Constructor for SmtpClient

        Args:
            username (string): Email address to send from
            password (string): Password for email address
            server (string): SMTP server domain (e.g. smtp.gmail.com)
            port (string): SMTP server port (e.g. 465)
        """
        self.smtp_username = username
        self.smtp_password = password
        self.smtp_server = server
        self.smtp_port = port
    
    def send_email(self, to, subject, body):
        """Send an email

        Args:
            to (string): Email address to send to
            subject (string): Email subject
            body (string): Email body
        """
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        server.login(self.smtp_username, self.smtp_password)

        msg_text = msg.as_string()
        server.sendmail(self.smtp_username, to, msg_text)
        server.close()
