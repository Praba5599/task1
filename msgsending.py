from email.message import EmailMessage
import smtplib

sender = "mailid"
devteam=["mailid1","mailid2"]
recipient = devteam
message = "happy new year"

email = EmailMessage()
email["From"] = sender
email["To"] = recipient
email["Subject"] = "Test Email"
email.set_content(message)

smtp = smtplib.SMTP("smtp.office365.com", port=587)
smtp.starttls()
smtp.login(sender, "password")
smtp.sendmail(sender, recipient, email.as_string())
smtp.quit()
