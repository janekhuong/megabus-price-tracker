import os
import logging
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart

load_dotenv()

# set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("info.log")],
)

def send_email(to_email, tickets):
    smtp_user = os.getenv("SES_SMTP_USER").strip()
    smtp_pass = os.getenv("SES_SMTP_PASS").strip()
    smtp_host = "email-smtp.us-east-2.amazonaws.com"
    smtp_port = 587

    from_email = "janekhuong05@gmail.com"
    subject = f"🚌 Megabus Price Alert"

    body = "Matching tickets found:\n\n"
    for t in tickets:
        body += (
            f"{t['date']}: ${t['price']} | {t['departureTime']} → {t['arrivalTime']}\n"
        )

    html = "<h3>Matching tickets found:</h3><ul>"
    for t in tickets:
        html += f"<li>{t['date']}: ${t['price']} | {t['departureTime']} → {t['arrivalTime']}</li>"
    html += "</ul>"

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, to_email, msg.as_string())
    except Exception as e:
        logging.exception(f"SES send error:, {e}")
