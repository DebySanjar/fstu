from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from states import FormStates, AdminStates, ContactStates, ReplyStates
from keyboards import (
    main_menu, cancel_keyboard, confirm_keyboard, admin_keyboard,
    phone_keyboard, search_filter_keyboard, about_bot_keyboard,
    vacancy_confirm_keyboard, reply_to_user_keyboard
)
import database

router = Router()
admin_mode = {}

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    database.add_user_id(user_id)
    
    if user_id == ADMIN_ID:
        await message.answer("👋 Assalomu alaykum, Admin!\n\nSiz admin panelidasiz.", reply_markup=admin_keyboard())
    else:
        vacancy_text = database.get_vacancy()
        await message.answer(vacancy_text, reply_markup=main_menu())

@router.message(F.text == "ℹ️ Bot haqida")
async def about_bot(message: Message):
    await message.answer(
        "🤖 <b>Bot haqida</b>\n\n"
        "Bu bot Farg'ona davlat texnika universiteti Logotip tanlovini "
        "o'tkazish maqsadida yaratilgan.\n\n"
        "📝 Bot orqali siz:\n• Logotipingizni yuborishingiz\n• Tanlov natijalarini bilib olishingiz mumkin\n\n"
        "Savol va masalalar yuzasidan adminga murojaat qilishingiz mumkin.",
        parse_mode="HTML",
        reply_markup=about_bot_keyboard()
    )

@router.message(F.text == "📝 Logotip yuborish")
async def start_form(message: Message, state: FSMContext):
    await state.set_state(FormStates.full_name)
    await message.answer("Ism va familyangizni kiriting:", reply_markup=cancel_keyboard())

@router.message(FormStates.full_name)
async def process_full_name(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await state.update_data(full_name=message.text)
    await state.set_state(FormStates.faculty)
    await message.answer("Fakultetingizni kiriting:", reply_markup=cancel_keyboard())

@router.message(FormStates.faculty)
async def process_faculty(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await state.update_data(faculty=message.text)
    await state.set_state(FormStates.group)
    await message.answer("Guruhingizni kiriting:", reply_markup=cancel_keyboard())

@router.message(FormStates.group)
async def process_group(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await state.update_data(group=message.text)
    await state.set_state(FormStates.phone)
    await message.answer(
        "Telefon raqamingizni yuboring:\n\n📱 Kontakt ulashish tugmasini bosing yoki raqamni yozing.",
        reply_markup=phone_keyboard()
    )

@router.message(FormStates.phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await state.set_state(FormStates.logo)
    await message.answer("Logotip rasmini yuboring:", reply_markup=cancel_keyboard())

@router.message(FormStates.phone)
async def process_phone_text(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await state.update_data(phone=message.text)
    await state.set_state(FormStates.logo)
    await message.answer("Logotip rasmini yuboring:", reply_markup=cancel_keyboard())

@router.message(FormStates.logo, F.photo)
async def process_logo(message: Message, state: FSMContext):
    logo_id = message.photo[-1].file_id
    await state.update_data(logo=logo_id)
    data = await state.get_data()
    
    summary = (
        "📋 <b>Sizning ma'lumotlaringiz:</b>\n\n"
        f"👤 <b>Ism va familya:</b> {data['full_name']}\n"
        f"🎓 <b>Fakultet:</b> {data['faculty']}\n"
        f"👥 <b>Guruh:</b> {data['group']}\n"
        f"📞 <b>Telefon:</b> {data['phone']}\n\n"
        "Ma'lumotlar to'g'rimi?"
    )
    
    await message.answer_photo(photo=data['logo'], caption=summary, parse_mode="HTML", reply_markup=confirm_keyboard())

@router.message(FormStates.logo)
async def process_logo_invalid(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await message.answer("❌ Iltimos, logotip rasmini yuboring!")

@router.callback_query(F.data == "confirm_send")
async def confirm_send(callback: CallbackQuery, state: FSMContext, bot):
    data = await state.get_data()
    user = callback.from_user
    database.save_user(user.id, data)
    
    username = user.username if user.username else "Yo'q"
    admin_message = (
        "📨 <b>Yangi logotip!</b>\n\n"
        f"� <b>Ishm va familya:</b> {data['full_name']}\n"
        f"🎓 <b>Fakultet:</b> {data['faculty']}\n"
        f"👥 <b>Guruh:</b> {data['group']}\n"
        f"📞 <b>Telefon:</b> {data['phone']}\n\n"
        f"🆔 <b>Telegram ID:</b> {user.id}\n"
        f"�‍<💼 <b>Username:</b> @{username}"
    )
    
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=data['logo'],
        caption=admin_message,
        parse_mode="HTML",
        reply_markup=reply_to_user_keyboard(user.id)
    )
    
    user_id = callback.from_user.id
    is_admin = user_id == ADMIN_ID
    await callback.message.answer("✅ Logotipingiz muvaffaqiyatli yuborildi!\n\nTez orada natijalar e'lon qilinadi. 😊", reply_markup=admin_keyboard() if is_admin else main_menu())
    await callback.answer()
    await state.clear()

@router.callback_query(F.data == "restart_form")
async def restart_form(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(FormStates.full_name)
    await callback.message.answer("🔄 Qayta to'ldiring.\n\nIsm va familyangizni kiriting:", reply_markup=cancel_keyboard())
    await callback.answer()
    await callback.message.answer("🔄 Anketani qayta to'ldiring.\n\nIshlamoqchi bo'lgan ishingiz:", reply_markup=job_types_keyboard())
    await callback.answer()

@router.message(F.text == "📢 E'lon yuborish")
async def admin_vacancy(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    await state.set_state(AdminStates.vacancy_text)
    await message.answer("📝 E'lon matnini yuboring:\n\nBu matn barcha ishtirokchilarga yuboriladi.", reply_markup=cancel_keyboard())

@router.message(AdminStates.vacancy_text)
async def process_vacancy(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard())
        return
    
    # Vakansiyani saqlash
    await state.update_data(vacancy_text=message.text)
    
    # Tasdiqlash uchun ko'rsatish
    await message.answer(
        f"📋 <b>E'lon:</b>\n\n{message.text}\n\n"
        "E'lonni barcha ishtirokchilarga yuborishni tasdiqlaysizmi?",
        parse_mode="HTML",
        reply_markup=vacancy_confirm_keyboard()
    )

@router.callback_query(F.data == "confirm_vacancy")
async def confirm_vacancy(callback: CallbackQuery, state: FSMContext, bot):
    """Vakansiyani tasdiqlash va yuborish"""
    data = await state.get_data()
    vacancy_text = data['vacancy_text']
    
    database.set_vacancy(vacancy_text)
    user_ids = database.get_all_user_ids()
    success_count = 0
    failed_count = 0
    
    await callback.message.answer("⏳ Yuborilmoqda...", reply_markup=admin_keyboard())
    
    for user_id in user_ids:
        if user_id == ADMIN_ID:
            continue
        try:
            await bot.send_message(chat_id=user_id, text=f"📢 <b>Yangi e'lon!</b>\n\n{vacancy_text}", parse_mode="HTML")
            success_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Failed to send to {user_id}: {e}")
    
    await callback.message.answer(
        f"✅ E'lon saqlandi!\n\n"
        f"📤 Muvaffaqiyatli: {success_count} ta\n"
        f"❌ Xatolik: {failed_count} ta\n"
        f"👥 Jami: {len(user_ids) - 1} ta ishtirokchi",
        reply_markup=admin_keyboard()
    )
    await callback.answer()
    await state.clear()

@router.callback_query(F.data == "restart_vacancy")
async def restart_vacancy(callback: CallbackQuery, state: FSMContext):
    """Vakansiyani qayta yozish"""
    await state.set_state(AdminStates.vacancy_text)
    await callback.message.answer(
        "🔄 E'lon matnini qayta yozing:",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

@router.message(F.text == "📊 Statistika")
async def admin_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    users_count = database.get_users_count()
    all_users = database.get_all_users()
    applications_count = len(all_users)
    await message.answer(f"📊 <b>Statistika</b>\n\n👥 Jami ishtirokchilar: {users_count}\n📝 Logotip yuborgan: {applications_count}", parse_mode="HTML", reply_markup=admin_keyboard())

@router.message(F.text == "🔍 Ishtirokchilarni qidirish")
async def search_users_menu(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    await message.answer("🔍 <b>Qidiruv</b>\n\nQidiruv turini tanlang:", parse_mode="HTML", reply_markup=search_filter_keyboard())

@router.callback_query(F.data.startswith("search_by_"))
async def search_filter_selected(callback: CallbackQuery, state: FSMContext):
    search_type = callback.data.split("_")[-1]
    search_names = {"name": "👤 Ism", "phone": "📞 Telefon", "address": "📍 Manzil", "work": "💼 Ish tajribasi"}
    await state.set_state(AdminStates.search_query)
    await state.update_data(search_type=search_type)
    await callback.message.answer(f"🔍 <b>{search_names[search_type]} bo'yicha qidirish</b>\n\nQidiruv so'zini kiriting:", parse_mode="HTML", reply_markup=cancel_keyboard())
    await callback.answer()

@router.callback_query(F.data == "cancel_search")
async def cancel_search(callback: CallbackQuery):
    await callback.message.answer("❌ Qidiruv bekor qilindi.", reply_markup=admin_keyboard())
    await callback.answer()

@router.message(AdminStates.search_query)
async def process_search_query(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Qidiruv bekor qilindi.", reply_markup=admin_keyboard())
        return
    
    query = message.text
    results = database.search_users(query)
    
    if not results:
        await message.answer("❌ Hech narsa topilmadi.\n\nBoshqa so'z bilan qidiring yoki /admin buyrug'i bilan admin paneliga qayting.", reply_markup=cancel_keyboard())
        return
    
    response = "🔍 <b>Qidiruv natijalari:</b>\n\n"
    response += f"Topildi: {len(results)} ta\n\n"
    
    for i, (user_id, data) in enumerate(results[:10], 1):
        job_type = data.get('job_type', 'Noma\'lum')
        address = data.get('address', 'Noma\'lum')
        response += (
            f"{i}. 👤 <b>{data['name']}</b>\n"
            f"   💼 {job_type}\n"
            f"   📍 {address}\n"
            f"   📞 {data['phone']}\n"
            f"   💼 {data['work_experience']}\n"
            f"   🆔 ID: <code>{user_id}</code>\n\n"
        )
    
    if len(results) > 10:
        response += f"... va yana {len(results) - 10} ta natija"
    
    await message.answer(response, parse_mode="HTML", reply_markup=admin_keyboard())
    await state.clear()


@router.callback_query(F.data == "contact_admin")
async def contact_admin(callback: CallbackQuery, state: FSMContext):
    """Adminga murojaat qilish"""
    await state.set_state(ContactStates.message)
    await callback.message.answer(
        "📝 <b>Adminga murojaat</b>\n\n"
        "Xabaringizni yozing. Admin tez orada javob beradi:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

@router.message(ContactStates.message)
async def process_contact_message(message: Message, state: FSMContext, bot):
    """Adminga xabar yuborish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=main_menu())
        return
    
    user = message.from_user
    username = user.username if user.username else "Yo'q"
    
    # Adminga xabar yuborish
    admin_msg = (
        "📨 <b>Yangi murojaat!</b>\n\n"
        f"👤 <b>Ism:</b> {user.first_name} {user.last_name or ''}\n"
        f"🆔 <b>ID:</b> {user.id}\n"
        f"👨‍💼 <b>Username:</b> @{username}\n\n"
        f"💬 <b>Xabar:</b>\n{message.text}"
    )
    
    try:
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_msg,
            parse_mode="HTML",
            reply_markup=reply_to_user_keyboard(user.id)
        )
        await message.answer(
            "✅ Xabaringiz adminga yuborildi!\n\nTez orada javob beramiz.",
            reply_markup=main_menu()
        )
    except Exception as e:
        await message.answer(
            "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.",
            reply_markup=main_menu()
        )
        print(f"Failed to send message to admin: {e}")
    
    await state.clear()


@router.callback_query(F.data.startswith("reply_"))
async def reply_button_clicked(callback: CallbackQuery, state: FSMContext):
    """Javob berish tugmasi bosildi"""
    user_id = int(callback.data.split("_")[1])
    await state.update_data(user_id=user_id)
    await state.set_state(ReplyStates.message)
    await callback.message.answer(
        f"💬 <b>Foydalanuvchiga javob berish</b>\n\n"
        f"Foydalanuvchi ID: {user_id}\n\n"
        "Javob xabaringizni yozing:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

@router.message(ReplyStates.message)
async def process_reply_message(callback: Message, state: FSMContext, bot):
    """Foydalanuvchiga javob yuborish"""
    if callback.text == "❌ Bekor qilish":
        await state.clear()
        await callback.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard())
        return
    
    data = await state.get_data()
    user_id = data['user_id']
    
    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"📩 <b>Admin javob berdi:</b>\n\n{callback.text}",
            parse_mode="HTML"
        )
        await callback.answer(
            "✅ Xabar muvaffaqiyatli yuborildi!",
            reply_markup=admin_keyboard()
        )
    except Exception as e:
        await message.answer(
            f"❌ Xatolik yuz berdi!\n\n"
            f"Foydalanuvchi topilmadi yoki botni bloklagan.\n\n"
            f"Xatolik: {str(e)}",
            reply_markup=admin_keyboard()
        )
        print(f"Failed to send reply to user {user_id}: {e}")
    
    await state.clear()
