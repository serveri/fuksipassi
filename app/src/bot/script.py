import logging 
import os
from dotenv import load_dotenv
from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

logger = logging.getLogger(__name__)

# Store bot screaming status
screaming = False

load_dotenv()

TELEGRAM_APP_URL=os.getenv('TELEGRAM_APP_URL')
TELEGRAM_BOT_TOKEN=os.getenv('TELEGRAM_BOT_TOKEN')

# Pre-assign menu text
FIRST_MENU = "<b>Wlcome to Menu  1</b>\n\nContinue by pressing Next"
SECOND_MENU = "<b>Menu 2</b>\n\nA better menu with even more shiny inline buttons."
OPEN_APP_MENU = "<b>Tervetuloa TaskiMattiin</b>\n\nAvaa sovellus painamalla näppäintä"

# Pre-assign button text
NEXT_BUTTON = "Next"
BACK_BUTTON = "Back"
OPEN_BUTTON = "Open TaskiMatti"
TUTORIAL_BUTTON = "Tutorial"

# Build keyboards
FIRST_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(NEXT_BUTTON, callback_data=NEXT_BUTTON)
]])
OPEN_APP_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(OPEN_BUTTON, url=TELEGRAM_APP_URL)
]])
SECOND_MENU_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_BUTTON)],
    [InlineKeyboardButton(TUTORIAL_BUTTON, url="https://core.telegram.org/bots/api")]
])


def echo(update: Update, context: CallbackContext) -> None:
    """
    This function would be added to the dispatcher as a handler for messages coming from the Bot API
    """

    # Print to console
    print(f'{update.message.from_user.first_name} wrote {update.message.text}')

    if screaming and update.message.text:
        context.bot.send_message(
            update.message.chat_id,
            update.message.text.upper(),
            # To preserve the markdown, we attach entities (bold, italic...)
            entities=update.message.entities
        )
    else:
        # This is equivalent to forwarding, without the sender's name
        update.message.copy(update.message.chat_id)

        # TODO: call a function here
    context.bot.send_message(
        update.message.from_user.id,
        OPEN_APP_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=OPEN_APP_MARKUP
    )

def scream(update: Update, context: CallbackContext) -> None:
    """
    This function handles the /scream command
    """

    global screaming
    scream
    ing = True


def whisper(update: Update, context: CallbackContext) -> None:
    """
    This function handles /whisper command
    """

    global screaming
    screaming = False


def menu(update: Update, context: CallbackContext) -> None:
    """
    This handler sends a menu with the inline buttons we pre-assigned above
    """

    context.bot.send_message(
        update.message.from_user.id,
        FIRST_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=FIRST_MENU_MARKUP
    )

def open(update: Update, context: CallbackContext) -> None:
    """
    This handler sends a menu from which user can open the app
    """

    context.bot.send_message(
        update.message.from_user.id,
        OPEN_APP_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=OPEN_APP_MARKUP
    )

def button_tap(update: Update, context: CallbackContext) -> None:
    """
    This handler processes the inline buttons on the menu
    """

    data = update.callback_query.data
    text = ''
    markup = None

    if data == NEXT_BUTTON:
        text = SECOND_MENU
        markup = SECOND_MENU_MARKUP
    elif data == BACK_BUTTON:
        text = FIRST_MENU
        markup = FIRST_MENU_MARKUP
        

    # Close the query to end the client-side loading animation
    update.callback_query.answer()

    # Update message content with corresponding menu section
    update.callback_query.message.edit_text(
        text,
        ParseMode.HTML,
        reply_markup=markup
    )

def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    # Then, we register each handler and the conditions the update must meet to trigger it
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("scream", scream))
    dispatcher.add_handler(CommandHandler("whisper", whisper))
    dispatcher.add_handler(CommandHandler("menu", menu))
    dispatcher.add_handler(CommandHandler("open", open))

    # Register handler for inline buttons
    dispatcher.add_handler(CallbackQueryHandler(button_tap))

    # Echo any message that is not a command
    dispatcher.add_handler(MessageHandler(~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()