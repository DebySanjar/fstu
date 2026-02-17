"""Ma'lumotlarni saqlash uchun oddiy modul"""

# Vakansiya matni
current_vacancy = """🎨 <b>Eng yaxshi logotip tanlovi</b>

Farg'ona davlat texnika universiteti yangi ko'rinishdagi logotip yaratish bo'yicha "Eng yaxshi logotip" tanlovini e'lon qiladi.

📋 <b>Talablar:</b>
• Logotip universitet nomi va maqomini to'liq ifodalashi
• Ilmiy salohiyatini aks ettirishi
• Bosma va raqamli shaklda sifatini yo'qotmasligi
• Mualliflik huquqini buzmasligi

🏆 <b>Mukofotlar:</b>
1-o'rin – 7 000 000 so'm va diplom
2-o'rin – 4 000 000 so'm va diplom
3-o'rin – 2 000 000 so'm va diplom

Shuningdek, hakamlar hay'ati tomonidan saralangan 10 nafar eng yaxshi ish mualliflari rag'batlantiriladi.

👥 <b>Ishtirokchilar:</b>
Tanlovda universitet professor-o'qituvchilari, xodimlar va talabalar ishtirok etishlari mumkin.

Logotipingizni yuborish uchun "📝 Logotip yuborish" tugmasini bosing."""

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
