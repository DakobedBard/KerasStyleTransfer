from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto.ses

AWS_ACCESS_KEY = 'AKIA2KY4DZB3ZLSQDVFE'
AWS_SECRET_KEY = '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'

'''
Okay here is how you verify the email adress from the command line.. 
aws ses verify-email-identity --email-address testawsmathias@gmail.com

'''

class Email(object):

    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
        self.text = None
        self.attachment = None

    def add_attachment(self, attachment):
        self.attachment = attachment

    def send(self, from_addr=None, file_name = None):

        connection = boto.ses.connect_to_region(
            'us-west-2',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        msg = MIMEMultipart()
        msg['Subject'] = self.subject
        msg['From'] = 'neuralstyleglacier@gmail.com'
        msg['To'] = 'mddarr@gmail.com'

        part = MIMEApplication(self.attachment)
        part.add_header('Content-Disposition', 'attachment', filename='StyleTransfer.png')
        part.add_header('Content-Type', 'application/vnd.ms-excel; charset=UTF-8')

        msg.attach(part)

        # the message body
        part = MIMEText("Here is your fucking image" )
        msg.attach(part)

        return connection.send_raw_email(msg.as_string(),source='neuralstyleglacier@gmail.com',destinations='mddarr@gmail.com')


email = Email(to='mddarr@gmail.com', subject='Here is your fucking image!')
email.text = 'This is your fucking image'
#you could use StringIO.StringIO() to get the file value
email.add_attachment('myimage.png')
email.send(from_addr='neuralstyleglacier@gmail.com',file_name="myimage.png")