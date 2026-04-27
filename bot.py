import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import filters, MessageHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
from telegram import ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv

#загрузка токена
load_dotenv()

#errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#сообщение при /start а так же кнопка
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button_hello = KeyboardButton("Delete all tasks")
    keyboard = ReplyKeyboardMarkup(
        [[button_hello]],
        resize_keyboard=True
    )
    await update.message.reply_text("Hello friend", reply_markup=keyboard)

#кнопка удаления(пока только сообщение)
async def delete_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("i can't do it right now")

#эхо сообщений 
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

#сообщения капсом
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

#в других чатах
async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results= []
    results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

#для команд которых нет
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry man, i dont know this command")

if __name__=='__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
  
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    delete_handle = MessageHandler(filters.Text(["Delete all tasks"]), delete_tasks)

    application.add_handler(start_handler)
    application.add_handler(delete_handle)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(unknown_handler)


    application.run_polling()