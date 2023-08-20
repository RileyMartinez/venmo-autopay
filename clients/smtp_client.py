import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SmtpClient:
    smtp_username: str
    smtp_password: str
    smtp_server: str
    smtp_port: int

    def __init__(self, username: str, password: str, server: str, port: int) -> None:
        self.smtp_username = username
        self.smtp_password = password
        self.smtp_server = server
        self.smtp_port = port
    
    def send_email(self, to, subject, body) -> bool:
        msg = MIMEMultipart()
        msg['From'] = self.smtp_username
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        server.login(self.smtp_username, self.smtp_password)

        msg_text = msg.as_string()
        errors: smtplib._SendErrs = server.sendmail(self.smtp_username, to, msg_text)
        server.close()

        return not errors
