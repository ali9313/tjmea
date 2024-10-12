from database import connect_db

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

# دالة لإضافة نقاط للمستخدم
def add_points(user_id, points):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET points = points + %s WHERE user_id = %s", (points, user_id))
    conn.commit()
    cursor.close()
    conn.close()

# دالة تسجيل الإحالة
def register_referral(user_id, referred_user_id):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO referrals (user_id, referred_user_id) VALUES (%s, %s)",
            (user_id, referred_user_id)
        )
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()  # في حالة كان المستخدم قد أحيل سابقًا
    finally:
        cursor.close()
        conn.close()

# دالة التحقق من الإحالة
def is_referred(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM referrals WHERE referred_user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] > 0