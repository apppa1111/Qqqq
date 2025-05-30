from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random

ADMIN_ID = 396217206  # Ваш ID

bible_quotes = [
    "«Господь — мой пастырь; я ни в чём не буду нуждаться.» (Псалом 22:1)",
    "«Блаженны чистые сердцем, ибо они Бога увидят.» (Матфей 5:8)",
    "«Не бойся, ибо Я с тобой.» (Исаия 41:10)",
    "«Я — путь, и истина, и жизнь.» (Иоанн 14:6)"
]

auto_responses = {
    "как дела?": "Спасибо, всё хорошо! 🙏",
    "привет": "Здравствуйте! Чем могу помочь? 🙌",
    "пока": "До свидания! Да благословит вас Бог! ✋"
}

keyboard = [
    ["📖 Чтение на день", "🕊 Слово дня"],
    ["📚 Библиотека христианина", "❓ Частый вопрос"],
    ["😔 Что делать, если…", "🧞‍♂️ Вопрос священнику"],
    ["📅 Церковный календарь"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

PRAYER_FILE = "prayers.txt"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Пожалуйста, выберите действие:", reply_markup=reply_markup)

# Чтение на день
async def reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Пример текста, позже можно заменить на динамическое чтение Евангелия дня
    text = "Евангелие дня: «В начале было Слово...»"
    await update.message.reply_text(text)

# Слово дня
async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(bible_quotes))

# Библиотека христианина (утреннее правило)
async def prayer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Пример текста, наполнить позже
    text = "Утреннее молитвенное правило: молитва о прощении..."
    await update.message.reply_text(text)

# Частые вопросы
async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Пример ответа
    text = "Часто задаваемые вопросы:\n1. Как подготовиться к исповеди?\n2. Что такое причастие?"
    await update.message.reply_text(text)

# Советы в духовных состояниях
async def state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Если вы чувствуете уныние, помолитесь и почитайте Псалом 50."
    await update.message.reply_text(text)

# Вопрос священнику
async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["awaiting_question"] = True
    await update.message.reply_text("✍️ Пожалуйста, напишите ваш вопрос священнику:")

# Сохранение вопроса священнику
async def save_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    with open("questions.txt", "a", encoding="utf-8") as f:
        f.write(f"{update.effective_user.first_name}: {question}\n")
    await update.message.reply_text("Спасибо! Ваш вопрос сохранён и будет рассмотрен.")

# Церковный календарь (пример)
async def calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Пример статичного текста, можно реализовать парсер для динамики
    text = "Сегодня 30 мая. Пост: строгий пост."
    await update.message.reply_text(text)

# Обработка текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if context.user_data.get("awaiting_question"):
        context.user_data["awaiting_question"] = False
        await save_question(update, context)
        return

    if text == "📖 чтение на день".lower():
        await reading(update, context)
    elif text == "🕊 слово дня".lower():
        await quote(update, context)
    elif text == "📚 библиотека христианина".lower():
        await prayer(update, context)
    elif text == "❓ частый вопрос".lower():
        await question(update, context)
    elif text == "😔 что делать, если…".lower():
        await state(update, context)
    elif text == "🧞‍♂️ вопрос священнику".lower():
        await ask(update, context)
    elif text == "📅 церковный календарь".lower():
        await calendar(update, context)
    elif text in auto_responses:
        await update.message.reply_text(auto_responses[text])
    else:
        await update.message.reply_text("❗ Пожалуйста, используйте кнопки ниже.", reply_markup=reply_markup)

# Запуск бота
app = ApplicationBuilder().token("7820850246:AAGC1mrwvF-1R9tEOf0RKCoE9prP5xXp180").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

app.run_polling()
