import os
import re
import smtplib
import secrets
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import User , VerificationCodes , db


def send_verification_code():
    data = request.form.to_dict()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 409
    if not data["email"]:
        return jsonify({'message': 'Email missing'}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        return jsonify({'message': 'Email is not valid'}), 400

    # Email configuration
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_EMAIL_PASSWORD")  # For security, consider using environment variables
    from_name = "Recipe Rise"
    receiver_email = data["email"]
    subject = "Email Verification"
    secret =generate_secure_code(6)
    hashed_code = generate_password_hash(secret, method='pbkdf2:sha256')
    body = "This secret code \"" + secret +"\" is to verfiy your email\ndon't share it with anyone."

    # Create message
    message = MIMEMultipart()
    message["From"] = f"{from_name} <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    new_verification_code = VerificationCodes(
        email = receiver_email,
        code = hashed_code,
        tries = 1
    )
    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            db.session.add(new_verification_code)
            db.session.commit()
        return jsonify({'message': "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({'message': str(e)})


def generate_secure_code(length):
    characters = string.digits + string.ascii_letters
    return ''.join(secrets.choice(characters) for j in range(length))


def verify_secret_code():
    data = request.form.to_dict()
    if not data["secret_code"]:
        return jsonify({'message': 'secret code missing'}), 400
    verification_code =  VerificationCodes.query.filter(VerificationCodes.email == data['email']).first()

    if not verification_code:
        return jsonify({'message': 'there is no verification code for this Email ... try again'}), 404

    if verification_code.tries > 3 :
        verification_code.code = generate_secure_code(64)
        db.session.commit()
        return jsonify({'message': "Code expired!"}), 410

    if check_password_hash(verification_code.code, data["secret_code"]):
        db.session.delete(verification_code)
        db.session.commit()
        return jsonify({'message': "Email Verified!"})
    elif not check_password_hash(verification_code.code, data["secret_code"]):
        verification_code.tries += 1
        db.session.commit()
        return jsonify({'message': "code ERROR!"}), 422
    return None