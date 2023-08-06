import os

from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

STYLE = "plain"

class Email:

    def __init__(self, service, subject):
        self.service = service
        self.subject = subject
        self.body = []
        self.attachments = []
    
    def write(self, s):
        self.body.append(s)
    
    def attach(self, f):
        base = MIMEBase("application", "octet-stream")
        with open(f, "rb") as fd:
            base.set_payload(fd.read())
        encode_base64(base)
        fname = os.path.basename(f)
        base.add_header("Content-Disposition", "attachment; filename= %s" % fname)
        self.attachments.append(base)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.service.send(self)
    
    # === PRIVATE ===
    
    def export(self):
        msg = MIMEMultipart()
        msg["From"] = self.service.username
        msg["To"] = self.service.username
        msg["Subject"] = self.subject
        
        body = "\r\n".join(self.body)
        msg.attach(MIMEText(body, STYLE))
        
        for attachment in self.attachments:
            msg.attach(attachment)
        
        return msg.as_string()
