import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SmtpClient:
    def __init__(self, username, password, server, port):
        self.smtp_username = username
        self.smtp_password = password
        self.smtp_server = server
        self.smtp_port = port
    
    def send_email(self, to, subject, body):
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
