import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

a = {
    "Airtel": {"mailid1": "Dear Airtel, this is my issue{input}."},
    "Vodafone": {"mailid2: "Dear Vodafone, this is my issue: {input}."},
    "Jio": {"mailid3": "Dear jio, this is my issue: {input}."}
}

provider_name = input("Enter the provider name: ")
input_text = input("Enter the input text: ")

if provider_name in a:
    # Retrieve the email ID and template for the provider
    email_id, template = list(a[provider_name].items())[0]

    # Replace the "{input}" placeholder in the template with the user input
    message = template.format(input=input_text)

    # Set the recipient and send the email
    recipient = email_id
    print(f"Sending email to {recipient}...")

    # Connect to Gmail SMTP server and send the email
    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.starttls()
        server.login('yourusername@outlook.com', 'urpassword')

        # Create a multipart message object and add the message to it
        msg = MIMEMultipart()
        msg['From'] = 'yourusername'
        msg['To'] = recipient
        msg['Subject'] = f"Message for {provider_name}"
        msg.attach(MIMEText(message))

        # Send the email
        server.sendmail('yourusername', recipient, msg.as_string())
        print("Email sent successfully!")
else:
    print("Invalid provider name.")
