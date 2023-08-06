import getpass, ssl, smtplib

from .Email import Email

DEFAULT_PORT = 465
DEFAULT_HOST = "smtp.gmail.com"

PROMPT = '''\033[1m\
 [ Username ]: %s
 [ Password ]: \
\033[0m'''

class EmailService:

    def __init__(self, username, recipients=[], host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.username = username
        self.recipients = sorted(set(recipients + [username]))
        self.password = getpass.getpass(PROMPT % username)
    
    def create(self, subject):
        return Email(
            service = self,
            subject = subject
        )

    # === PRIVATE ===
    
    def send(self, email):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
            server.ehlo()
            server.login(self.username, self.password)
            server.sendmail(self.username, self.recipients, email.export())
