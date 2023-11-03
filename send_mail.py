import imghdr
import os
import smtplib
import ssl
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()
username = os.getenv('USER_NAME')
password = os.getenv('PASSWORD')


def sendmail(image):
    print(image)
    if image != "":
        email_message = EmailMessage()
        email_message["Subject"] = "Motion Detected!"
        email_message.set_content("New motion detected and its image is attached")
        with open(image, "rb") as file:
            content = file.read()
        email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login(username, password)
        mail.sendmail(username, username, email_message.as_string())
        mail.quit()
        print("mail sent")
    else:
        print("no path available")


# if __name__ == "__main__":
#     sendmail("hi")