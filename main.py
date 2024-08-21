from telegram import Update, ChatPermissions, Chat
from telegram import ChatMember
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '7305037034:AAFxXevC5hfwBoQMpq2Vi53itfxzPoxtYlY'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to AiAKitaX Link Remover!\n\nGroup : @AiAkita_Dog')

def delete_links(update: Update, context: CallbackContext) -> None:
    # Check if we have an original or edited message
    message = update.message or update.edited_message
    if not message:
        return  # Exit if there is no message to process

    # Check if the message has entities
    if not message.entities:
        return  # Exit if there are no entities in the message

    chat_id = message.chat_id
    user_id = message.from_user.id
    chat_member = context.bot.get_chat_member(chat_id, user_id)

    if chat_member.status in ('administrator', 'creator'):
        return  # Exit if the sender is an admin or creator

    # Process each entity to check for links
    for entity in message.entities:
        if entity.type in ('text_link', 'url'):
            # Delete the message containing a link
            try:
                message.delete()
            except Exception as e:
                logger.error(f"Failed to delete message: {e}")
            return  # Exit after deleting the message


def welcome_message(update: Update, context: CallbackContext) -> None:
    new_member = update.message.new_chat_members[0]
    update.message.reply_text(f"Welcome, {new_member.first_name}! Feel free to introduce yourself.")

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Available commands:\n/start - Start the bot\n/help - Show available commands')

def ban_user(update: Update, context: CallbackContext) -> None:
    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.message.chat_id
    context.bot.kick_chat_member(chat_id, user_id)
    update.message.reply_text(f"User has been banned.")

def mute_user(update: Update, context: CallbackContext) -> None:
    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.message.chat_id
    context.bot.restrict_chat_member(chat_id, user_id, permissions=ChatPermissions(can_send_messages=False))
    update.message.reply_text(f"User has been muted.")

def unban_user(update: Update, context: CallbackContext) -> None:
    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.message.chat_id
    context.bot.unban_chat_member(chat_id, user_id)
    update.message.reply_text(f"User has been unbanned.")

def unmute_user(update: Update, context: CallbackContext) -> None:
    user_id = update.message.reply_to_message.from_user.id
    chat_id = update.message.chat_id
    context.bot.restrict_chat_member(chat_id, user_id, permissions=ChatPermissions(can_send_messages=True))
    update.message.reply_text(f"User has been unmuted.")



def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    # Register a command handler for the /start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Register a command handler for the /help command
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Register a message handler to delete messages containing links
    dispatcher.add_handler(MessageHandler(Filters.chat_type.groups & ~Filters.command, delete_links))

    # Register a message handler to welcome new members
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_message))

    # Register a command handler for the /ban command
    dispatcher.add_handler(CommandHandler("ban", ban_user))

    # Register a command handler for the /mute command
    dispatcher.add_handler(CommandHandler("mute", mute_user))

    # Register a command handler for the /unban command
    dispatcher.add_handler(CommandHandler("unban", unban_user))

    # Register a command handler for the /unmute command
    dispatcher.add_handler(CommandHandler("unmute", unmute_user))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
