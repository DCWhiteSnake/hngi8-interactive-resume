import smtplib
from email.mime.text import MIMEText


def send_mail(customer, email, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '1140bb8db77804'
    password = '496b3883b89178'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Email: {email}</li><li>Comments: {comments}</li></ul>"

    sender_email = email
    receiver_email = 'davidokeke.c@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'HNG Stage 2'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
