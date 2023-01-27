import os
import smtplib, ssl
from flask import Blueprint, render_template, request, flash
from .models import User, Alert
from . import db
from email.message import EmailMessage

# This file is where we store the login information if need be
auth = Blueprint('auth', __name__)

@auth.route('/alerts', methods=['GET', 'POST'])
def alerts():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Alert.query.filter_by(email=email).first()
        
        if user:
            flash('Email already registered for alerts.', category='error')
            pass
        elif len(email) < 3:
            flash('Email must be greater then 3 characters.', category='error')
            pass
        else:
            new_user = Alert(email=email)
            db.session.add(new_user)
            db.session.commit()

            msg = EmailMessage()
            msg.set_content('Welcome to the Quechan Irrigation Device (1) alert system. An email will be sent to this inbox once the amount of water has exeded the aloted ammout.')
            msg['Subject'] = 'Irrigation Alerts'
            msg['From'] = 'quechan2023@outlook.com'
            msg['To'] = email

            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

            with smtplib.SMTP('smtp.office365.com', port=587) as smtp:
                smtp.starttls(context=context)
                smtp.login('quechan2023@outlook.com', 'capstone2023')
                smtp.send_message(msg)

            flash('Successfully signed up for alerts!', category='success')
            pass

    return render_template("alerts.html")
    
@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 3:
            flash('Email must be greater then 3 characters.', category='error')
            pass
        elif len(firstName) < 1:
            flash('First name must be greater then 1 character.', category='error')
            pass
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            pass
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            pass
        else:
            flash('Account created!.', category='success')
            pass

    return render_template("sign_up.html")
    