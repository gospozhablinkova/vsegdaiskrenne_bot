import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ChatMemberHandler
)

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN")

# ─────────────────────────────────────────
# ТВОИ МАТЕРИАЛЫ — редактируй здесь
# ─────────────────────────────────────────

MATERIALS = {
    "relations": {
        "title": "💌 Отношения",
        "items": [
            ("111 вопросов для отношений", "https://t.me/vsegdaiskrenne/605"),
            ("Что меняется после свадьбы", "https://t.me/vsegdaiskrenne/2"),
            ("Токсичные отношения без драмы", "https://t.me/vsegdaiskrenne/3"),
        ]
    },
    "life": {
        "title": "🌿 Жизнь",
        "items": [
            ("Синдром отложенной жизни", "https://t.me/vsegdaiskrenne/4"),
            ("Жизнь без подруг в новом городе", "https://t.me/vsegdaiskrenne/5"),
            ("Деньги и лень — честно", "https://t.me/vsegdaiskrenne/6"),
        ]
    },
    "mind": {
        "title": "🧠 Мышление",
        "items": [
            ("Ты не сложная — ты нормальная", "https://t.me/vsegdaiskrenne/7"),
            ("Мягкость — это не слабость", "https://t.me/vsegdaiskrenne/8"),
            ("Не всем нужен рост", "https://t.me/vsegdaiskrenne/9"),
        ]
    },
    "about": {
        "title": "👤 Про меня",
        "items": [
            ("Кто я и почему стоит остаться", "https://t.me/vsegdaiskrenne/10"),
            ("Моя история: от токсичного к браку", "https://t.me/vsegdaiskrenne/11"),
            ("Почему «Госпожа»", "https://t.me/vsegdaiskrenne/12"),
        ]
    },
}

WELCOME_TEXT = (
    "Привет 👋\n\n"
    "Я бот канала *vsegdaiskrenne* — здесь собраны самые важные материалы Ани.\n\n"
    "Выбери тему — и получишь подборку:"
)

# ─────────────────────────────────────────
# Кнопки главного меню
# ─────────────────────────────────────────

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(MATERIALS["relations"]["title"], callback_data="relations"),
         InlineKeyboardButton(MATERIALS["life"]["title"], callback_data="life")],
        [InlineKeyboardButton(MATERIALS["mind"]["title"], callback_data="mind"),
         InlineKeyboardButton(MATERIALS["about"]["title"], callback_data="about")],
        [InlineKeyboardButton("📌 Все материалы", callback_data="all")],
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("← Назад", callback_data="back")]
    ])

# ─────────────────────────────────────────
# Форматирование подборки
# ─────────────────────────────────────────

def format_section(key: str) -> str:
    section = MATERIALS[key]
    lines = [f"*{section['title']}*\n"]
    for title, url in section["items"]:
        lines.append(f"• [{title}]({url})")
    return "\n".join(lines)

# ─────────────────────────────────────────
# Хендлеры
# ─────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back":
        await query.edit_message_text(
            WELCOME_TEXT,
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )
    elif data == "all":
        text = "📚 *Все материалы*\n\n" + "\n\n".join(
            format_section(k) for k in MATERIALS
        )
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=back_keyboard(),
            disable_web_page_preview=True
        )
    elif data in MATERIALS:
        text = format_section(data)
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=back_keyboard(),
            disable_web_page_preview=True
        )

# Приветствие нового подписчика канала
async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    if result.new_chat_member.status == "member":
        user = result.new_chat_member.user
        name = user.first_name or "друг"
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text=(
                    f"Привет, {name} 👋\n\n"
                    "Рада, что ты здесь.\n"
                    "Я Аня — говорю честно про жизнь, отношения и мышление без иллюзий.\n\n"
                    "Вот главное, с чего начать:"
                ),
                parse_mode="Markdown",
                reply_markup=main_menu_keyboard()
            )
        except Exception:
            pass  # пользователь заблокировал личку — ок

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Напиши /start — покажу главное меню 👇"
    )

# ─────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(ChatMemberHandler(greet_new_member, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))
    app.run_polling()

if __name__ == "__main__":
    main()
