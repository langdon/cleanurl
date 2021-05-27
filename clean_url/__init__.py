import logging

import azure.functions as func
from unalix import clear_url, unshort_url
import logging
import os
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Send me your urls to clean!')

#def echo(update: Update, _: CallbackContext) -> None:
#    """Echo the user message."""
#    update.message.reply_text(update.message.text)

def clean_url(update: Update, _: CallbackContext) -> None:
    """Unshorten and strip tracking info."""
    dirty_url = update.message.text
    full_url = unshort_url(dirty_url)
    logging.info(f'URL expanded: {full_url}')    
    clean_url = clear_url(full_url)
    logging.info(f'URL clean: {clean_url}')    
    update.message.reply_text(f"Original URL: {dirty_url}\nURL with tracking information removed \n{clean_url}")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

#    # on non command i.e message - echo the message on Telegram
#    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, clean_url))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    dirty_url = req.params.get('url')
    if not dirty_url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            dirty_url = req_body.get('url')

#    logging.info(f'URL rcvd: {dirty_url}')    
    if dirty_url:
        full_url = unshort_url(dirty_url)
#        logging.info(f'URL expanded: {full_url}')    
        clean_url = clear_url(full_url)
#        logging.info(f'URL clean: {clean_url}')    
        return func.HttpResponse(f"Original URL: {dirty_url}\nURL with tracking information removed \n{clean_url}")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a 'url' in the query string or in the request body to clean the input dirty_url.",
            status_code=200
        )
        
