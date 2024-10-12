import os
import psycopg2

# إعداد قاعدة بيانات PostgreSQL
def connect_db():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username TEXT,
            points INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS referrals (
            user_id INTEGER,
            referred_user_id INTEGER,
            PRIMARY KEY (user_id, referred_user_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (referred_user_id) REFERENCES users (user_id)
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()