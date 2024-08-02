from aiosmtplib import SMTP
from email.message import EmailMessage

async def send_email(recipient: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = "jethaniaditya7@gmail.com"
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    async with SMTP(hostname="smtp.gmail.com", port=587) as smtp:
        await smtp.login("jethaniaditya7@gmail.com", "hArrYPOTTER@4")
        await smtp.send_message(message)
