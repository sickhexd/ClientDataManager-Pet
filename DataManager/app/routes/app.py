import os
from flask import Flask, request, render_template, redirect, url_for
import uuid
from datetime import datetime
from app.services.db_connection import get_db_connection
from app.services.encryption import generate_key, encrypt_data

# Устанавливаем правильный путь к шаблонам
template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_path = os.path.join(os.path.dirname(__file__), '..', 'static')

app = Flask(__name__,static_folder=static_path, template_folder=template_path)

f = 0
key = generate_key()

@app.route('/registration', methods=['GET', 'POST'])
def get_registration_data():
    global f
    if request.method == 'POST':
        surename = request.form.get('surename')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phoneNumber = request.form.get('phoneNumber')
        passportSeries = request.form.get('passportSeries')
        passportNumber = request.form.get('passportNumber')

        encrypted_email = encrypt_data(email, key)
        encrypted_phone = encrypt_data(phoneNumber, key)
        encrypted_passport_series = encrypt_data(passportSeries, key)
        encrypted_passport_number = encrypt_data(passportNumber, key)
        
        ik_id = str(uuid.uuid4())

        now = datetime.now()

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(""" 
                INSERT INTO Client (ik_id, surename, name, lastname, email, phoneNumber, passportSeries, passportNumber, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ik_id, surename, name, lastname, encrypted_email, encrypted_phone, encrypted_passport_series, encrypted_passport_number, now, now))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print("Ошибка при записи в базу данных:", e)
            return "Произошла ошибка при записи данных в базу."

        print(surename, name, lastname, email, phoneNumber, passportSeries, passportNumber)
        f = 1

        return redirect(url_for('application'))

    return render_template('registration.html')


@app.route('/submit', methods=['GET'])
def application():
    global f
    if f == 1:
        f = 0  
        return render_template('submit.html')
    else:
        return redirect(url_for('get_registration_data'))


if __name__ == '__main__':
    app.run(debug=True)
