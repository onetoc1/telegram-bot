import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7993439090:AAEqiy8YsZ7rFJxjcT_Faq59ZtT0reRrHUE"
ADMIN_ID = 5505303576  # замени на свой ID

PROMOCODES = {
    "1win": "CAZDIME",
    "melbet": "MACL"
}

MIRRORS = {
    "1win": "https://1wbfqv.life/?open=register&p=shyf",
    "melbet": "https://refpa9819469.top/L?tag=s_429201m_18637c_&site=429201&ad=18637&r=user/registration.php"
}

subscribers = set()

def get_keyboard(user_id):
    keyboard = [
        ['Промокод 1WIN 🎰', 'Ссылка 1WIN 🔗'],
        ['Промокод MelBet 🎲', 'Ссылка MelBet 🔗'],
        ['Мой Telegram ID 🆔']
    ]
    if user_id == ADMIN_ID:
        keyboard.append(['Проверить онлайн 🟢', 'Отправить рассылку 📢'])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    subscribers.add(user_id)
    await update.message.reply_text(
        "Привет! Я помогу тебе с промокодами и ссылками 😊\nВыбери нужную кнопку на клавиатуре ниже.",
        reply_markup=get_keyboard(user_id)
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Если админ сейчас вводит текст для рассылки
    if user_id == ADMIN_ID and context.user_data.get('waiting_broadcast'):
        message = update.message.text
        context.user_data['waiting_broadcast'] = False

        count = 0
        for uid in subscribers:
            try:
                await context.bot.send_message(chat_id=uid, text=f"📢 Рассылка:\n\n{message}")
                count += 1
                await asyncio.sleep(0.05)
            except Exception:
                pass

        await update.message.reply_text(f"Рассылка отправлена {count} пользователям.")
        return  # Важный return, чтобы дальше не обрабатывалось

    text = update.message.text

    if text == 'Промокод 1WIN 🎰':
        await update.message.reply_text(f"Твой промокод для 1WIN: {PROMOCODES['1win']} 🎉")
    elif text == 'Ссылка 1WIN 🔗':
        await update.message.reply_text(
            f"Актуальная ссылка 1WIN: <a href=\"{MIRRORS['1win']}\">КЛИК</a> 🔗",
            parse_mode='HTML'
        )
    elif text == 'Промокод MelBet 🎲':
        await update.message.reply_text(f"Твой промокод для MelBetа: {PROMOCODES['melbet']} 🎉")
    elif text == 'Ссылка MelBet 🔗':
        await update.message.reply_text(
            f"Актуальная ссылка MelBetа: <a href=\"{MIRRORS['melbet']}\">КЛИК</a> 🔗",
            parse_mode='HTML'
        )
    elif text == 'Мой Telegram ID 🆔':
        await update.message.reply_text(f"Твой Telegram ID: {user_id} 🆔")

    elif user_id == ADMIN_ID:
        if text == 'Проверить онлайн 🟢':
            await update.message.reply_text(f"Пользователей, кто запускал /start: {len(subscribers)}")
        elif text == 'Отправить рассылку 📢':
            await update.message.reply_text("Введите сообщение для рассылки:")
            context.user_data['waiting_broadcast'] = True
        else:
            await update.message.reply_text("Команда не распознана. Используй /start.")
    else:
        await update.message.reply_text("Команда не распознана. Используй /start.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "Или нажми кнопки на клавиатуре ниже."
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
