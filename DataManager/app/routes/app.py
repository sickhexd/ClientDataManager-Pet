from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import uuid
import os
from datetime import datetime
from app.services.db_connection import get_db_connection
from app.services.encryption import generate_key, encrypt_data
from app.services.auth_email import generate_and_send_code  

# Устанавливаем правильный путь к шаблонам
template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_path = os.path.join(os.path.dirname(__file__), '..', 'static')
app = Flask(__name__, static_folder=static_path, template_folder=template_path)
app.secret_key = os.urandom(24)  # Ключ для работы с сессиями

f = 0
key = generate_key()

# Словарь для хранения кодов аутентификации
auth_codes = {}

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
        
        code = generate_and_send_code(email)
        auth_codes[email] = code
        session['is_code_sent'] = True

        f = 1

        return redirect(url_for('verify_code', email=email))

    return render_template('registration.html')

@app.route(f'/verify_code/<email>', methods=['GET', 'POST'])
def verify_code(email):
    if request.method == 'POST':
        entered_code = request.form.get('code')

        if email in auth_codes and auth_codes[email] == entered_code:
            del auth_codes[email]
            session.pop('is_code_sent', None)
            return redirect(url_for('application'))
        else:
            return "Неверный код, попробуйте снова."

    is_code_sent = session.get('is_code_sent', False)
    return render_template('verify_code.html', email=email, isCodeSent=is_code_sent)  # Страница для ввода кода

@app.route('/resend_code', methods=['POST'])
def resend_code():
    data = request.get_json()
    email = data.get('email')
    
    if email in auth_codes:
        new_code = generate_and_send_code(email)
        auth_codes[email] = new_code
        return jsonify({"success": True})

    return jsonify({"success": False}), 400

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
