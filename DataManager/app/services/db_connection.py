import psycopg2

# Функция для подключения к БД
def get_db_connection():
    conn = psycopg2.connect(
            host="localhost",
            database="ClientData",
            user="postgres",
            password="postgres",
            port="5432"
        )
    return conn
