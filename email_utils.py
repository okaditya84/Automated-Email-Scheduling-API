# from aiosmtplib import SMTP
# from email.message import EmailMessage

# async def send_email(recipient: str, subject: str, body: str):
#     message = EmailMessage()
#     message["From"] = "jethaniaditya7@gmail.com"
#     message["To"] = recipient
#     message["Subject"] = subject
#     message.set_content(body)

#     async with SMTP(hostname="smtp.gmail.com", port=587) as smtp:
#         await smtp.login("jethaniaditya7@gmail.com", "hArrYPOTTER@4")
#         await smtp.send_message(message)


import aiosmtplib
from email.message import EmailMessage
import os

async def send_email(recipient: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_FROM", "jethaniaditya7@gmail.com")
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        smtp = aiosmtplib.SMTP(hostname="smtp.gmail.com", port=587, use_tls=True)
        await smtp.connect()
        await smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        await smtp.send_message(message)
        await smtp.quit()
        print(f"Email sent successfully to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise