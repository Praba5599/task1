import datetime
import os
import smtplib
import email
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["mydatabase"]
collection = db["mycollection"]

def details(input_text, provider_name):
    details = collection.find_one({"Provider_name": provider_name})
    print(type(details))
    if details:
    # Email details
        receiver_mail = details['Receiver_mail']
        cc = details['CC']
        bcc = details['BCC']
        subject = details['Subject']
        template = details['Template'].replace("{input_text}", input_text)
        
        return receiver_mail, cc, bcc, subject, template
    
def sending_mail(receiver_mail, cc, bcc, subject, template, attachment_path=None):
    message = email.message.EmailMessage()
    message['From'] = smtp_username
    message['To'] = receiver_mail
    message['Cc'] = cc
    message['Bcc'] = bcc
    message['Subject'] = subject
    message.set_content(template, subtype='html')

 # Add attachment if provided
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=os.path.basename(attachment_path))
           
    try:
        # Send email using SMTP server
        mail.send_message(message)
        print("Email sent successfully")
        status = "sent"
    except Exception as e:
        print("Error sending email: {}".format(e))
        status = "failed"
    

    db = client["maildatabase"]
    collection = db["mailcollection"]
    check = {'receiver_mail': receiver_mail,
        'cc': cc,
        'bcc': bcc,
        'sent_time': datetime.datetime.now(),
        'status':status,
        'document':bool(attachment_path),
        'reply msg':'',
        'reply time':'',
        'any attachments':''

    }
    result = collection.insert_one(check)
 
if __name__ == "__main__":
    smtp_username = "username"
    smtp_password = "password"
    smtp_server = "outlook.office365.com"
    smtp_port = 587
    while True:
        try:
            mail = smtplib.SMTP(smtp_server, smtp_port)
            mail.starttls()
            mail.login(smtp_username, smtp_password)

            while True:
                try:
                    input_text = input("Enter the input text: ")
                    provider_name = input("Enter the provider name: ")
                    attachment_path = input("Enter the path to the attachment (optional): ")
                    receiver_mail, cc, bcc, subject, template = details(input_text, provider_name)
                    sending_mail(receiver_mail, cc, bcc, subject, template, attachment_path=attachment_path)
                except smtplib.SMTPAuthenticationError as e:
                    print("SMTP login failed: {}".format(e))
                    mail.quit()
                    mail = smtplib.SMTP(smtp_server, smtp_port)
                    mail.starttls()
                    mail.login(smtp_username, smtp_password)
                    continue
        except Exception as e:
            print("Error connecting to SMTP server: {}".format(e))
            continue
