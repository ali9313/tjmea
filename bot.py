import os
import json
import psycopg2
import telebot

# إعدادات البوت
BOT_TOKEN = os.environ.get('TOKEN')  # تأكد من إعداد هذا في Heroku
bot = telebot.TeleBot(BOT_TOKEN)

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
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def load_data_from_json():
    with open('data.json') as f:
        data = json.load(f)

    conn = connect_db()
    cursor = conn.cursor()
    for user in data:
        cursor.execute(
            "INSERT INTO users (user_id, username, points) VALUES (%s, %s, %s) ON CONFLICT (user_id) DO NOTHING",
            (user['user_id'], user['username'], user['points'])
        )
    conn.commit()
    cursor.close()
    conn.close()

# دالة لإضافة المستخدم
def add_user(user_id, username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (user_id, username) VALUES (%s, %s) ON CONFLICT (user_id) DO NOTHING",
        (user_id, username)
    )
    conn.commit()
    cursor.close()
    conn.close()

# دالة للحصول على النقاط
def get_points(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        return result[0]  # إرجاع النقاط إذا تم العثور عليها
    return 0  # إرجاع 0 إذا لم يتم العثور على المستخدم

# الدوال الخاصة بالبوت
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    add_user(user_id, username)
    bot.send_message(message.chat.id, f"مرحباً {username}! لقد تم تسجيلك.")

@bot.message_handler(commands=['points'])
def send_points(message):
    user_id = message.from_user.id
    points = get_points(user_id)
    bot.send_message(message.chat.id, f"لديك {points} نقاط.")

# بدء البوت
init_db()
load_data_from_json()
bot.polling()