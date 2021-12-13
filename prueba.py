import youtube_dl
import logging
import os
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
updater = Updater("2077856255:AAFlBNNNkm1IaDMI8mUatDGpz5X15idMPo0")

def start(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(f"Bones {user.mention_markdown_v2()}\!\nHOLA QUE TAL Aquest bot et permet descarregar MP3 a partir d'enllaços de YouTube, així com editar\\-los a partir d'unes marques de temps o \"timestamps\"\\.\nSi vols aprendre més sobre les funcions d'aquest bot escriu /help\\.")


def echo(update, context):
     if(update.message.text.upper().find("Hola que tal") == 0):
        #update.message.reply_text("Prefiero comer pizza")
        paco = context.args[0]
        print(paco)

def main():
    ### Settings ###
    # Truquem al Updater per començar el bot amb el nostre token creat a partir del BotFather
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    ### Controlem les comandes de l'usuari ###
    # Aquesta comanda s'encarrega de donar la benvinguda a l'usuari i explicar de que tracta el bot
    dispatcher.add_handler(CommandHandler("start", start))

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    updater.idle()

main()