import getpass, ssl, smtplib

from .Email import Email

DEFAULT_PORT = 465

PROMPT = '''\033[1m\
 [   Host   ]: %s
 [ Username ]: %s
 [ Password ]: \
\033[0m'''

ERROR = '''\033[1m\033[91m
Login failed.

Either username/password entries are incorrect,
or you may need to adjust security features in
your email account.
\033[0m\033[0m'''

class EmailService:

    def __init__(self, username, recipients=[], port=DEFAULT_PORT):
        self.port = port
        self.host = self.parse_host(username)
        self.username = username
        self.recipients = sorted(set(recipients + [username]))
        self.password = getpass.getpass(PROMPT % (self.host, username))
        self.send()
    
    def create(self, subject):
        return Email(
            service = self,
            subject = subject
        )

    # === PRIVATE ===
    
    def parse_host(self, username):
        return "smtp." + username.split("@")[1]
    
    def send(self, email=None):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.host, self.port, context=context) as server:
            
            try:
                server.login(self.username, self.password)
                
                if email is not None:
                    server.sendmail(self.username, self.recipients, email.export())
                
            except smtplib.SMTPAuthenticationError:
                print(ERROR)
            
            
