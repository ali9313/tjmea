import os
import telebot
from database import init_db
from user_functions import add_user, get_points, add_points, register_referral, is_referred

# إعدادات البوت
BOT_TOKEN = os.environ.get('TOKEN')  # تأكد من إعداد هذا في Heroku
REFERRAL_POINTS = 10  # عدد النقاط التي يحصل عليها المستخدم عند إحالة صديق
bot = telebot.TeleBot(BOT_TOKEN)

# الدوال الخاصة بالبوت
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    referral_info = message.text.split()

    add_user(user_id, username)

    # التحقق إذا كانت هناك إحالة
    if len(referral_info) > 1:
        referrer_id = int(referral_info[1])
        if not is_referred(user_id):
            register_referral(referrer_id, user_id)
            add_points(referrer_id, REFERRAL_POINTS)  # إضافة نقاط للمحيل
            bot.send_message(referrer_id, f"لقد حصلت على {REFERRAL_POINTS} نقاط لإحالة صديقك!")
    
    bot.send_message(message.chat.id, f"مرحباً {username}! لقد تم تسجيلك.")

@bot.message_handler(commands=['points'])
def send_points(message):
    user_id = message.from_user.id
    points = get_points(user_id)
    bot.send_message(message.chat.id, f"لديك {points} نقاط.")

# أمر لعرض رابط الإحالة
@bot.message_handler(commands=['referral'])
def send_referral_link(message):
    user_id = message.from_user.id
    referral_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    bot.send_message(message.chat.id, f"رابط الإحالة الخاص بك هو:\n{referral_link}")

# بدء البوت
init_db()
bot.polling()