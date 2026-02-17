import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', '8597744088:AAGggNPeXU-SGPZLvz4C-DE77WdP_q2GIdU')
ADMIN_ID = int(os.getenv('ADMIN_ID', '7176985245'))

# Xatoliklarni tekshirish
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID topilmadi! .env faylini tekshiring.")
