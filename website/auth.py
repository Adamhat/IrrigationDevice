import os
import smtplib, ssl
import pandas as pd
import io
import xlsxwriter
from flask import Blueprint, Response, Flask, render_template, request, flash, jsonify
from .models import User, Alert, Water, Options
from . import db
from email.mime.text import MIMEText

# This file is where we store the login information if need be
auth = Blueprint('auth', __name__)

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

@auth.route('/alerts', methods=['GET', 'POST'])
def alerts():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Alert.query.filter_by(email=email).first()
        
        if user:
            flash('Email already registered for alerts. Email removed list.', category='success')
            db.session.delete(user)
            db.session.commit()
            pass
        elif len(email) < 3:
            flash('Email must be greater then 3 characters.', category='error')
            pass
        else:
            newUser = Alert(email=email)
            db.session.add(newUser)
            db.session.commit()

            subject = "Irrigation Alerts"
            body = "Welcome to the Quechan Irrigation Device (1) alert system. An email will be sent to this inbox once the amount of water has exceeded the allotted amount."
            sender = "quechan2023alerts@gmail.com"
            recipients = email
            password = os.getenv("PASSWORD_QUECHAN_2")
            send_email(subject, body, sender, recipients, password)

            flash('Successfully signed up for alerts!', category='success')
            pass

    return render_template("alerts.html")

@auth.route('/data', methods=['POST'])
def recieve_data():
    data = request.get_json()
    flowRate = data['FlowRate']
    volume = data['Volume']

    mostRecentOption = Options.query.order_by(Options.id.desc()).first()
    channelArea = ((float(mostRecentOption.channelFloor) + ((float(mostRecentOption.channelWidth) - float(mostRecentOption.channelFloor)) * float(mostRecentOption.channelHight))) * float(mostRecentOption.channelHight))

    updateTable = Water(flowRate=flowRate, volume=volume, channelArea=channelArea)
    db.session.add(updateTable)
    db.session.commit()
    
    return jsonify({'result' : 'Success', 
                    'flowRate' : flowRate, 
                    'volume' : volume})

@auth.route('/data')
def data():
    id = Water.query.order_by(Water.id)
    date = Water.query.order_by(Water.date)
    flowRate = Water.query.order_by(Water.flowRate)
    crossSection = Water.query.order_by(Water.crossSection)
    volume = Water.query.order_by(Water.volume)
    channelArea = Water.query.order_by(Water.channelArea)

    return render_template("data.html",
    id=id,
    date=date,
    flowRate=flowRate,
    crossSection=crossSection,
    volume=volume,
    channelArea=channelArea)

@auth.route('/options', methods=['GET', 'POST'])
def options():
    if request.method == 'POST':
        if request.form['submitButton'] == 'submitOptions':
            channelWidth = request.form.get('channelWidth')
            channelFloor = request.form.get('channelFloor')
            channelHight = request.form.get('channelHight')

            if len(channelWidth) == 0 or len(channelFloor) == 0 or len(channelHight) == 0:
                flash('Each option must contain a value.', category='error')
                pass
            elif float(channelWidth) <= 0:
                flash('Channel Surface Width must be greater then 0.', category='error')
                pass
            elif float(channelFloor) <= 0:
                flash('Channel Floor Width must be greater then 0.', category='error')
                pass
            elif float(channelHight) <= 0:
                flash('Channel Hight must be greater then 0.', category='error')
                pass
            else:
                updateTable = Options(channelWidth=channelWidth, channelFloor=channelFloor, channelHight=channelHight)
                db.session.add(updateTable)
                db.session.commit()

                mostRecentOption = Options.query.order_by(Options.id.desc()).first()
                flash(f"Channel width: {mostRecentOption.channelWidth}, Channel floor: {mostRecentOption.channelFloor}, Channel height: {mostRecentOption.channelHight}", category="success")
                pass
        elif request.form['submitButton'] == 'excelExport':
            data = Water.query.with_entities(Water.date, Water.volume, Water.flowRate).all()
            df = pd.DataFrame(data, columns=['date', 'volume', 'flowRate'])
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet('Data')
            header_format = workbook.add_format({'bold': True})
            date_format = workbook.add_format({'num_format': 'yyyy-mm-dd hh:mm:ss'})
            headers = ['Date', 'Volume', 'Flow Rate']
            
            for col, header in enumerate(headers):
                worksheet.write(0, col, header, header_format)
            for row, data_row in enumerate(data):
                for col, data_col in enumerate(data_row):
                    if col == 0:
                        worksheet.write(row+1, col, data_col, date_format)
                    else:
                        worksheet.write(row+1, col, data_col)
            workbook.close()

            response = Response(output.getvalue(),
                                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response.headers['Content-Disposition'] = 'attachment; filename=data.xlsx'

            return response
        elif request.form['submitButton'] == 'deleteData':
            Water.query.delete()
            db.session.commit()
            flash('All data successfully cleared! Re-enter options to continue recieving data.', category='success')
            pass
        else:
            pass

    return render_template("options.html")
    
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
