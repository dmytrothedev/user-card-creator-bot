import json
from typing import Final

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)

from config_example import TOKEN  # real token stored locally, not in GitHub


ASK_NAME, ASK_AGE, ASK_TOWN, ASK_LIFE = range(4)


async def debug_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prints each incoming update to the console as JSON. Helpful for debugging."""
    as_dict = update.to_dict()
    print("\n--- NEW UPDATE ---")
    print(json.dumps(as_dict, indent=2, ensure_ascii=False))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Yes, I'm ready!", callback_data="ready")],
        [InlineKeyboardButton("Not ready yet", callback_data="not_ready")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Hi! I'm a bot that helps you create your personal profile card. Shall we begin?",
        reply_markup=reply_markup,
    )


async def callback_start_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "ready":
        await query.edit_message_text(
            "Great! Let's start! 😊\nClick here to begin the survey → /conv"
        )
    elif query.data == "not_ready":
        await query.edit_message_text(
            "Okay, take your time.\nWhen you're ready, type /start again."
        )
    elif query.data == "end":
        await query.edit_message_text("Awesome! It was a pleasure 😊")
    elif query.data == "changes":
        await query.edit_message_text(
            "Okay, let's update your card.\nRestart with → /start"
        )
    else:
        await query.edit_message_text("Unknown command. Please restart the bot.")


async def conv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("What's your name?")
    return ASK_NAME


async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("How old are you?")
    return ASK_AGE


async def ask_town(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["age"] = update.message.text
    await update.message.reply_text("Which city do you live in?")
    return ASK_TOWN


async def ask_life(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["town"] = update.message.text
    await update.message.reply_text("Tell me a little bit about yourself 💬")
    return ASK_LIFE


async def result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["life"] = update.message.text

    name = context.user_data.get("name")
    age = context.user_data.get("age")
    town = context.user_data.get("town")
    life = context.user_data.get("life")

    final_keyboard = [
        [InlineKeyboardButton("Edit information", callback_data="changes")],
        [InlineKeyboardButton("Everything is correct!", callback_data="end")],
    ]
    reply_markup = InlineKeyboardMarkup(final_keyboard)

    await update.message.reply_text(
        f"📇 Your profile card:\n"
        f"Name: {name}\n"
        f"Age: {age}\n"
        f"City: {town}\n"
        f"About you: {life}",
        reply_markup=reply_markup,
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("conv", conv)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_town)],
            ASK_TOWN: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_life)],
            ASK_LIFE: [MessageHandler(filters.TEXT & ~filters.COMMAND, result)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("conv", conv))
    app.add_handler(CallbackQueryHandler(callback_start_answer))
    app.add_handler(MessageHandler(filters.ALL, debug_update))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
