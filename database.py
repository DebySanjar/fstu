"""Ma'lumotlarni saqlash uchun oddiy modul"""

# Vakansiya matni
current_vacancy = """Assalomu alaykum! 👋

Farg'ona davlat texnika universiteti Logotip tanloviga xush kelibsiz!

Logotipingizni yuborish uchun quyidagi ma'lumotlarni to'ldiring."""

# Foydalanuvchilar ro'yxati
users = {}

# Barcha foydalanuvchi ID lari
all_user_ids = set()

def get_vacancy():
    """Joriy vakansiyani olish"""
    return current_vacancy

def set_vacancy(text):
    """Vakansiyani yangilash"""
    global current_vacancy
    current_vacancy = text

def add_user_id(user_id):
    """Foydalanuvchi ID sini saqlash"""
    all_user_ids.add(user_id)

def get_all_user_ids():
    """Barcha foydalanuvchi ID larini olish"""
    return list(all_user_ids)

def save_user(user_id, data):
    """Foydalanuvchi ma'lumotlarini saqlash"""
    users[user_id] = data

def get_user(user_id):
    """Foydalanuvchi ma'lumotlarini olish"""
    return users.get(user_id)

def search_users(query):
    """Foydalanuvchilarni qidirish"""
    query = query.lower()
    results = []
    
    for user_id, data in users.items():
        if query in data.get('name', '').lower():
            results.append((user_id, data))
        elif query in data.get('phone', '').lower():
            results.append((user_id, data))
        elif query in data.get('address', '').lower():
            results.append((user_id, data))
        elif query in data.get('work_experience', '').lower():
            results.append((user_id, data))
    
    return results

def get_users_count():
    """Foydalanuvchilar sonini olish"""
    return len(all_user_ids)

def get_all_users():
    """Barcha foydalanuvchilarni olish"""
    return users
