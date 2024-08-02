from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import config
from handlers import start, button, done

def main():
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler('done', done))

    application.run_polling()

if __name__ == '__main__':
    main()