import telebot
from telebot import types
import os
import requests

# توكن البوت
TOKEN = '8289028685:AAGmSHEzAIZjjzS5xxbOoCYNGPbpHB7lScU'
bot = telebot.TeleBot(TOKEN)

# إعدادات Supabase
SUPABASE_URL = 'https://kbwmfvhzdhxjkfhojncf.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtid21mdmh6ZGh4amtmaG9qbmNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMxMjQwNjIsImV4cCI6MjA3ODcwMDA2Mn0._vGkiQtKrfWgdKpklWacTfSymXVupw7XKl0f0LFUStQ'

# عند كتابة /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("إنشاء طلب وظيفة")
    btn2 = types.KeyboardButton("عرض الطلبات")
    markup.add(btn1, btn2)
    
    bot.send_message(
        message.chat.id,
        "أهلاً فيك في منصة التوظيف! 👷‍♂️\nاختر خيار:",
        reply_markup=markup
    )

# عند الضغط على زر
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "إنشاء طلب وظيفة":
        bot.reply_to(message, "حلو! اكتب وصف الوظيفة (مثلاً: 'مطلوب مصور في دمشق، 50 ألف ليرة')")
        bot.register_next_step_handler(message, save_job)
    
    elif message.text == "عرض الطلبات":
        show_jobs(message)

# حفظ الطلب في Supabase
def save_job(message):
    job_text = message.text
    data = {"description": job_text, "user_id": message.from_user.id}
    
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/jobs",
        json=data,
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
    )
    
    if response.status_code == 201:
        bot.reply_to(message, "تم إنشاء الطلب بنجاح! ✅\nستصلك العروض قريباً.")
    else:
        bot.reply_to(message, "فشل الحفظ، حاول لاحقاً.")

# عرض الطلبات
def show_jobs(message):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/jobs",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
    )
    
    if response.status_code == 200:
        jobs = response.json()
        if jobs:
            text = "الطلبات المتاحة:\n\n"
            for job in jobs:
                text += f"• {job['description']}\n"
            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "لا توجد طلبات حالياً.")
    else:
        bot.send_message(message.chat.id, "خطأ في جلب البيانات.")

# تشغيل البوت
print("البوت شغال 24/7...")
bot.infinity_polling()
