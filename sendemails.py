#! /usr/bin/env python3
"""
    Script that sends emails using gmail

    This program has been partially obtained from
    https://developers.google.com/gmail/api/guides/sending
"""

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import email.encoders
import base64
import time
import mimetypes
from httplib2 import Http
from apiclient import errors
from googleapiclient.discovery import build
from oauth2client import file, client, tools

import config
from checkemails import EmailSpecs
import checkemails


def create_message(specs:EmailSpecs):
    """ Create a message for an email specs.
        Returns an object containing a base64url encoded email object.  """
    def process_attachment(path):
        """ converts the given file contents to a suitable attachment """
        content_type, encoding = mimetypes.guess_type(str(path))
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        with open(path, 'rb') as fp:
            if main_type == 'text':
                msg = MIMEText(fp.read(), _subtype=sub_type)
            elif main_type == 'image':
                msg = MIMEImage(fp.read(), _subtype=sub_type)
            elif main_type == 'audio':
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
            else:
                print(f"XXX adding attachment {main_type}/{sub_type}")
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
        filename = path.name
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        email.encoders.encode_base64(msg)
        return msg

    #message = MIMEMultipart('alternative')
    message = MIMEMultipart()
    message['to'] = specs.to
    message['from'] = config.sender
    message['subject'] = specs.subject
    message.attach(MIMEText(specs.text, 'html'))
    if specs.attachment is not None:
        message.attach(process_attachment(specs.attachment))

    print("Email for %s" % specs.to)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, message):
    """ Send an email message.

        Args:
           service: Authorized Gmail API service instance.
           message: Message to be sent.

        Returns:
            Sent Message.
    """
    user_id = 'me'  # user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

print("Sending messages")

store = file.Storage(config.token_path)
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(config.client_secret_path, config.scopes)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

print("Credentials ok")
email_specs = checkemails.unsent_emails()
for specs in email_specs:
    message = create_message(specs)
    sent_message = send_message(service, message)
    time.sleep(config.time_sleep_seconds)
    print("Done ", sent_message)
