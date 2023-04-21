import imaplib
import email
import os

user = "mailid"
password = "password"
server = "outlook.office365.com"
#connection
mail = imaplib.IMAP4(server)
mail.starttls()
mail.login(user, password)
mail.select('inbox')

status, data = mail.search(None, 'ALL')
mail_ids = []
for block in data:
    mail_ids += block.split()

for i in mail_ids:
    status, data = mail.fetch(i, '(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            message = email.message_from_bytes(response_part[1])
            # print("hello world")

            if message.is_multipart():
                for part in message.get_payload():
                    if not part.is_multipart() and 'attachment' in str(part.get('Content-Disposition')):
                        filename = part.get_filename()
                        if filename:
                            # Create the attachments folder if it does not exist
                            attachments_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'attachments')
                            if not os.path.exists(attachments_dir):
                                os.makedirs(attachments_dir)

                            filepath = os.path.join(attachments_dir, filename)
                            with open(filepath, 'wb') as f:
                                f.write(part.get_payload(decode=True))
                            print(f'Downloaded file: {filename}')
            else:
                mail_content = message.get_payload()
                mail_from = message['from']
                mail_subject = message['subject']
                print(f'From: {mail_from}')
                print(f'Subject: {mail_subject}')
                print(f'Content: {mail_content}')

