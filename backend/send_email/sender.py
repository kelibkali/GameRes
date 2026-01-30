import smtplib
from email.mime.text import MIMEText
from email.header import Header

from email.mime.multipart import MIMEMultipart

from config.settings import smtp_server, email_address,email_password

class EmailSender:
    def __init__(self, smtp_server,smtp_port, email_address,password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = email_address
        self.password = password

    def create_connection(self):
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.email_address, self.password)

        return server

    def send_code(self, to_email,code):
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to_email
        msg['Subject'] = Header("您的验证码","utf-8").encode()
        text = f"""您的验证码是:{code}。\n5分钟内有效，请尽快使用。"""
        msg.attach(MIMEText(text,'plain','utf-8'))
        try:
            server = self.create_connection()
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Error: unable to send send_email,{e}")
        return False

email_sender = EmailSender(smtp_server,25,email_address,email_password)