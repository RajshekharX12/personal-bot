from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_TOKEN' with your actual Telegram bot token
TOKEN = 'YOUR_TOKEN'

# Dictionary to store banned users
banned_users = set()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your personal bot.')

def echo(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Check if user is banned
    if user_id in banned_users:
        update.message.reply_text('You are banned. Contact admin for assistance.')
        return

    # Echo the user's message
    update.message.reply_text(update.message.text)

def ban(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Ban the user
    banned_users.add(user_id)
    update.message.reply_text(f'User {user_id} has been banned.')

def unban(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Unban the user
    if user_id in banned_users:
        banned_users.remove(user_id)
        update.message.reply_text(f'User {user_id} has been unbanned.')
    else:
        update.message.reply_text(f'User {user_id} is not banned.')

def broadcast(update: Update, context: CallbackContext) -> None:
    # Get the message to broadcast
    message_text = ' '.join(context.args)

    # Broadcast the message to all users
    for user_id in context.bot.users:
        context.bot.send_message(chat_id=user_id, text=message_text)

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(CommandHandler("ban", ban))
    dp.add_handler(CommandHandler("unban", unban))
    dp.add_handler(CommandHandler("broadcast", broadcast, pass_args=True))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
