from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from base64 import b64encode, b64decode
from flask import Flask, request, render_template, redirect, url_for
import psycopg2
from datetime import datetime
import uuid

# Функция для генерации случайного ключа
def generate_key():
    return os.urandom(32)

# Функция для шифрования данных
def encrypt_data(data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = data + (16 - len(data) % 16) * ' ' 
    encrypted = encryptor.update(padded_data.encode()) + encryptor.finalize()
    return b64encode(iv + encrypted).decode()  

# Функция для расшифровки данных
def decrypt_data(encrypted_data, key):
    encrypted_data = b64decode(encrypted_data)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted.decode().rstrip()

app = Flask(__name__)

# Функция для подключения к БД
def get_db_connection():
    conn = psycopg2.connect(
            host="localhost",  # Сервер базы данных
            database="ClientData",  # Имя базы данных
            user="postgres",  # Имя пользователя
            password="postgres",  # Пароль
            port="5432"  # Порт PostgreSQL
        )
    return conn

# Глобальная переменная для проверки отправки формы
f = 0
key = generate_key()

@app.route('/registration', methods=['GET', 'POST'])
def get_registration_data():
    global f
    if request.method == 'POST':
        # Получаем данные из формы
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
            # Вставляем данные в таблицу Client
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

        # Перенаправляем на страницу благодарности
        return redirect(url_for('application'))

    return render_template('registration.html')


@app.route('/submit', methods=['GET'])
def application():
    global f
    if f == 1:
        f = 0  # Сбрасываем флаг, чтобы при обновлении страницы не показывалось повторно
        return render_template('submit.html')
    else:
        return redirect(url_for('get_registration_data'))  # Если прямой переход, редирект на форму

