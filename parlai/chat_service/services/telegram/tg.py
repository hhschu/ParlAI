import os

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from .client import chats, connect_ws

BOT_TOKEN = os.environ.get["BOT_TOKEN"]


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{update.effective_user.first_name}, just talk to me",
    )


def talk(update, context):
    incoming_message = update.message.text
    chat_id = update.effective_chat.id
    if chat_id not in chats:
        connect_ws(chat_id)
    chats[chat_id].put(incoming_message)
    contexts[chat_id] = context

def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I don't have any command."
    )


def client(bot_token):
    updater = Updater(token=bot_token, use_context=True)

    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(Filters.text & (~Filters.command), talk)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(unknown_handler)

    return updater


if __name__ == "__main__":
    c = client(BOT_TOKEN)
    c.start_polling()
