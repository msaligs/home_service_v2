import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'mail.smtp2go.com' #'locallhost'
SMTP_PORT = 2525  #587   #1025
USERNAME = "macho3.com"
SENDER_EMAIL = "tafagy@polkaroad.net"
SENDER_PASSWORD = "nw2b2gb11JV2H4Q2" #"yckixkxeojlbyzrb"    nw2b2gb11JV2H4Q2


def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(host=SMTP_SERVER, port=SMTP_PORT) as server:
            server.starttls()
            server.login(USERNAME, SENDER_PASSWORD)
            # server.set_debuglevel(1)  # Enable debug output

            # server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

