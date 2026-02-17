from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    """Asosiy menyu"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Logotip yuborish")],
            [KeyboardButton(text="ℹ️ Bot haqida")]
        ],
        resize_keyboard=True
    )
    return keyboard

def cancel_keyboard():
    """Bekor qilish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )
    return keyboard

def phone_keyboard():
    """Telefon raqam ulashish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Kontakt ulashish", request_contact=True)],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard

def confirm_keyboard():
    """Tasdiqlash tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Yuborish", callback_data="confirm_send"),
                InlineKeyboardButton(text="🔄 Qayta to'ldirish", callback_data="restart_form")
            ]
        ]
    )
    return keyboard

def vacancy_confirm_keyboard():
    """Vakansiya tasdiqlash tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ E'lon qilish", callback_data="confirm_vacancy"),
                InlineKeyboardButton(text="🔄 Qayta yozish", callback_data="restart_vacancy")
            ]
        ]
    )
    return keyboard

def admin_keyboard():
    """Admin paneli"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📢 E'lon yuborish")],
            [KeyboardButton(text="🔍 Ishtirokchilarni qidirish")],
            [KeyboardButton(text="📊 Statistika")]
        ],
        resize_keyboard=True
    )
    return keyboard

def vacancy_confirm_keyboard():
    """Vakansiya tasdiqlash tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ E'lon qilish", callback_data="confirm_vacancy"),
                InlineKeyboardButton(text="🔄 Qayta yozish", callback_data="restart_vacancy")
            ]
        ]
    )
    return keyboard

def reply_to_user_keyboard(user_id):
    """Foydalanuvchiga javob berish tugmasi"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Javob berish", callback_data=f"reply_{user_id}")]
        ]
    )
    return keyboard

def about_bot_keyboard():
    """Bot haqida inline tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📞 Adminga murojaat", callback_data="contact_admin")]
        ]
    )
    return keyboard

def search_filter_keyboard():
    """Qidiruv filtri tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Ism bo'yicha", callback_data="search_by_name")],
            [InlineKeyboardButton(text="📞 Telefon bo'yicha", callback_data="search_by_phone")],
            [InlineKeyboardButton(text="📍 Manzil bo'yicha", callback_data="search_by_address")],
            [InlineKeyboardButton(text="💼 Ish tajribasi bo'yicha", callback_data="search_by_work")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_search")]
        ]
    )
    return keyboard

def position_keyboard():
    """Pozitsiya tanlash tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👨‍🎓 Talaba", callback_data="position_student")],
            [InlineKeyboardButton(text="👨‍🏫 O'qituvchi", callback_data="position_teacher")]
        ]
    )
    return keyboard

def faculty_keyboard():
    """Fakultetlar ro'yxati"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Axborot texnologiyalari va telekommunikatsiyalar", callback_data="faculty_it")],
            [InlineKeyboardButton(text="Mexanika-mashinasozlik", callback_data="faculty_mech")],
            [InlineKeyboardButton(text="Energetika muhandisligi", callback_data="faculty_energy")],
            [InlineKeyboardButton(text="Kimyo texnologiya", callback_data="faculty_chem")],
            [InlineKeyboardButton(text="Arxitektura va qurilish", callback_data="faculty_arch")],
            [InlineKeyboardButton(text="Ishlab chiqarishda boshqaruv", callback_data="faculty_mgmt")],
            [InlineKeyboardButton(text="Yengil sanoat va to'qimachilik", callback_data="faculty_textile")]
        ]
    )
    return keyboard
