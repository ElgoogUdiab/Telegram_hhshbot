from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

from uuid import uuid4
import logging
import nbnhhsh


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    if query == "":
        update.inline_query.answer([])
    try:
        result = nbnhhsh.query(query)

        stringified_result = nbnhhsh.stringify(result)
        
        results = [
            InlineQueryResultArticle(
                id=uuid4(),
                title=result['title'],
                input_message_content=InputTextMessageContent(result['message_to_send']),
                description=result['description'],
            ) for result in stringified_result
        ]
    except Exception as e:
        results = []

    update.inline_query.answer(results)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

if __name__ == "__main__":
    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Get token and start
    try:
        with open("token") as f:
            token = f.readline().strip()
    except:
        print("No token! Create file named \"token\" under the same directory with main.py!")
        exit(1)
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # Inline handler
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Error handler
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()
