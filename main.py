import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import csv

def load_email_settings():
    """Load email settings from a configuration file."""
    config_file = "email_config.txt"
    if not os.path.exists(config_file):
        print(f"Configuration file '{config_file}' not found. Please create one.")
        return None

    settings = {}
    with open(config_file, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            settings[key] = value
    return settings

def send_email(recipient, subject, message, settings):
    """Send an email using the provided settings."""
    try:
        # Create the email
        email = MIMEMultipart()
        email["From"] = settings["EMAIL_ADDRESS"]
        email["To"] = recipient
        email["Subject"] = subject
        email.attach(MIMEText(message, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(settings["SMTP_SERVER"], int(settings["SMTP_PORT"])) as server:
            server.starttls()
            server.login(settings["EMAIL_ADDRESS"], settings["EMAIL_PASSWORD"])
            server.sendmail(settings["EMAIL_ADDRESS"], recipient, email.as_string())
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")

def bulk_send_email(file_path, subject, message):
    """Send emails in bulk from a CSV file."""
    settings = load_email_settings()
    if not settings:
        return

    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                recipient = row[0]
                send_email(recipient, subject, message, settings)
    except Exception as e:
        print(f"Error reading CSV file: {e}")

if __name__ == "__main__":
    print("Welcome to the Email Sender Script!")
    print("1. Send a single email")
    print("2. Send bulk emails from a CSV file")
    choice = input("Choose an option (1 or 2): ")

    settings = load_email_settings()
    if not settings:
        print("Unable to proceed without email configuration.")
        exit()

    if choice == "1":
        recipient = input("Enter recipient email address: ")
        subject = input("Enter email subject: ")
        message = input("Enter email message: ")
        send_email(recipient, subject, message, settings)
    elif choice == "2":
        file_path = input("Enter path to CSV file: ")
        subject = input("Enter email subject: ")
        message = input("Enter email message: ")
        bulk_send_email(file_path, subject, message)
    else:
        print("Invalid option selected.")
