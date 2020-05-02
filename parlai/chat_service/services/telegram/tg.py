import logging
import os
import queue
import threading

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from .client import chats, connect_ws, contexts

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

BOT_TOKEN = os.environ["BOT_TOKEN"]


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{update.effective_user.first_name}, just talk to me",
    )


def talk(update, context):
    incoming_message = update.message.text
    chat_id = update.effective_chat.id
    if chat_id not in chats:
        chats[chat_id] = queue.Queue()
        user = update.effective_user
        username = f"{user.first_name} {user.last_name}"
        threading.Thread(connect_ws, args=(chat_id, username)).start()
    chats[chat_id].put(incoming_message)
    contexts[chat_id] = context


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="sorry, I don't have any command. just talk to me",
    )


if __name__ == "__main__":
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(Filters.text & (~Filters.command), talk)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
