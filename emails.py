import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart

load_dotenv()

def send_email(to_email, tickets):
    smtp_user = os.getenv("SES_SMTP_USER")
    smtp_pass = os.getenv("SES_SMTP_PASS")
    smtp_host = "email-smtp.us-east-2.amazonaws.com"
    smtp_port = 587

    from_email = "janekhuong05@gmail.com"
    subject = f"🚌 Megabus Price Alert"

    body = "Matching tickets found:\n\n"
    for t in tickets:
        body += (
            f"{t['date']}: ${t['price']} | {t['departureTime']} → {t['arrivalTime']}\n"
        )

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, to_email, msg.as_string())
        print("✅ Email sent via Amazon SES")
    except Exception as e:
        print("❌ SES send error:", e)


def test_email_send():
    smtp_user = os.getenv("SES_SMTP_USER")
    smtp_pass = os.getenv("SES_SMTP_PASS")
    smtp_host = "email-smtp.us-east-2.amazonaws.com"
    smtp_port = 587

    from_email = "janekhuong05@gmail.com"
    to_email = "janek170805@gmail.com" 

    subject = "Test Email from Megabus Notifier"
    body = "✅ This is a test email to confirm your email function works."

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(from_email, to_email, msg.as_string())
        print("✅ Test email sent successfully.")
    except Exception as e:
        print("❌ Failed to send email:", e)


# with st.spinner("Fetching tickets..."):
#     tickets = find_tickets(
#         origin_id=city_to_id[origin],
#         destination_id=city_to_id[destination],
#         start_date=str(date_range[0]),
#         end_date=str(date_range[1]),
#         total_passengers=total_passengers,
#         max_price=max_price,
#     )

# if tickets:
#     st.success(f"Found {len(tickets)} matching tickets!")
#     st.dataframe(tickets)
# else:
#     st.error("No tickets found under your price limit.")
