import smtplib
from private_data import email_data


my_email_address = email_data['FROM_EMAIL']
my_app_password = email_data.get("GMAIL_APP_PASSWORD")
to_email_address = email_data.get("TO_EMAIL_ADDRESS")
SMTP_GMAIL_ADDRESS = "smtp.gmail.com"
SMTP_GMAIL_PORT = 587


def send_mail(message):
    with smtplib.SMTP(SMTP_GMAIL_ADDRESS, SMTP_GMAIL_PORT) as connection:
        # secure the connection from malicious hackers or attackers
        connection.starttls()
        # Log in to your email account
        connection.login(user=my_email_address, password=my_app_password)
        # Send email
        connection.sendmail(from_addr=my_email_address, to_addrs=to_email_address,
                            msg=f"Subject:Congratulations\n\nHello!\n{message}\n\nRegards\nYour Favourite Security+ App")