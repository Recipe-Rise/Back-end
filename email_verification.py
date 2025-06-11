import smtplib
import secrets
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import jsonify

secret_code =""
def verify_email(email):
    # Email configuration
    sender_email = "reciperisev@gmail.com"
    password = "dunejyjgmfjgpjkt"  # For security, consider using environment variables

    from_name = "Recipe Rise"
    receiver_email = email
    subject = "Email Verification"
    generate_secure_code()
    body = "This secret code \"" + secret_code +"\" is to verfiy your email\ndon't share it with anyone."

    # Create message
    message = MIMEMultipart()
    message["From"] = f"{from_name} <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return jsonify({'message': "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({'message': str(e)})

def generate_secure_code():
    length = 6
    characters = string.digits + string.ascii_letters
    global secret_code
    secret_code= ''.join(secrets.choice(characters) for i in range(length))

def verify_secret_code(entered_secret_code):
    if entered_secret_code == secret_code:
        return True
    else:
        return False