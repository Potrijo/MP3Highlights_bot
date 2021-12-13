
# -- coding: latin-1 --

import telegram
import youtube_dl
import yt_dlp
import logging
import os
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

# Amb logging podrem rebre qualsevol error alhora d'interactuar amb l'usuari mitjançant consola, a mes
# ens donara informacio important com la hora o el dia al qual ha ocorregut l'error
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
updater = Updater("2064694571:AAEl-ZpGBdgxekKRSENYCkaSXFj0YGolA60")

# Aquests metodes s'anomenen "command handlers" 
def start(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(f"Bones {user.mention_markdown_v2()}\!\nAquest bot et permet descarregar MP3 a partir d'enllaços de YouTube, així com editar\\-los a partir d'unes marques de temps o \"timestamps\"\\.\nSi vols aprendre més sobre les funcions d'aquest bot escriu /help")


def help_command(update, context):
    update.message.reply_text("Aquest bot té dos úniques comandes.\n/start: Dona una breu introducció sobre la funció del bot.\n/url: Espera a que l'usuari entri una URL per descarregar el MP3. Un cop ha rebut la URL revisarà si és vàlida o no, en cas de ser-ho descarregarà el arxiu d'audio MP3 i preguntarà a l'usuari què vol fer\\. Pots descarregar els arxius d'audio sense editar o editar\\-los per crear un retall o \"clip\"")

def get_url(update, context):
    try:
        url = str(context.args[0])
        check_url(url, update, context)
    except (IndexError, ValueError) as e:
        update.message.reply_text("No has passat cap argument!")

def check_url(url, update, context):
    try:
        update.message.reply_text("Estem descarregant el teu audio, això podria tardar uns minuts.")
        video_url = url
        mp3_info = youtube_dl.YoutubeDL().extract_info(
            url = video_url,download=False
        )
        global filename
        filename = f"{mp3_info['title']}.mp3"
        
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl': "./MP3/"+ filename,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download(video_url)
        
        #Definim variables globals per accedir-hi més tard
        global chatid
        chatid = update.message.chat_id
        
        #Opcions dels buttons
        keyboard = [
            [
                InlineKeyboardButton("Sí", callback_data='Sí'),
                InlineKeyboardButton("No", callback_data='No')
            ],
        ]   

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Vols retallar l\'audio?', reply_markup=reply_markup)
        #updater.dispatcher.add_handler(MessageHandler(Filters.text, ask_for_clip))

        #updater.bot.send_audio(chat_id=update.message.chat_id, audio=open(f'./MP3/{filename}', 'rb'))
    except Exception as e:
        print(e)
        update.message.reply_text("Sembla que ha hagut un error... Torna a intentar-ho més tard o prova amb un altre video.")

# Funcion que guarda el texto
def reply(update: Update, context: CallbackContext):                     
    user_input = update.message.text
    x = user_input.split(" ")

    if (len(x) == 3)  and (x[0].lower() == "canviar") and (x[1].lower() == "longitud"):
        startTime = x[2]
        startTimeHours = startTime[0:2]
        startTimeMinutes = startTime[3:5]
        startTimeSeconds = startTime[6:8]
        global startPoint
        startPoint = str(startTimeHours) + ":" + str(startTimeMinutes) + ":" + str(startTimeSeconds)
        print(startPoint)
    
    if (len(x) == 3)  and (x[0].lower() == "canviar") and (x[1].lower() == "temps"):
        length = x[2]
        lengthHours = length[0:2]
        lengthMinutes = length[3:5]
        lengthSeconds = length[6:8]
        global fileLength
        fileLength = str(lengthHours) + ":" + str(lengthMinutes) + ":" + str(lengthSeconds)
        print(fileLength)

    print(user_input)
    return user_input

def ask_for_clip(update: Update, context: CallbackContext):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    print("queryData: "+query.data)
    if query.data =='Sí' and fileLength  !=None and startPoint != None:
        create_clip(update, context)
    elif query.data == "No":
        query.edit_message_text(text=f"Aquí tens l'audio sense editar:")
        updater.bot.send_audio(chat_id=chatid, audio=open(f'./MP3/{filename}', 'rb'))
    elif fileLength == None and startPoint == None:
        update.message.reply_markdown_v2("Sembla que no has definit la longitud del retall o el punt de començament")

    
def create_clip(update: Update, context: CallbackContext):
    '''Hay que cambiarlo para que entre el usuario los datos desde el chat
    esto no nos sirve porque es para la terminal'''
    try:
        print(f"Start: {startPoint}")
        print(f"Length: {fileLength}")

        os.system(f'ffmpeg -ss {startPoint} -i MP3/"{filename}" -t {fileLength} "{filename}_clip.mp3"')
    except Exception as e:
        print(e)
        update.message.reply_markdown_v2("Sembla que no has introduit el format de manera correcta. ")    

def main():
    ### Settings ###
    # Truquem al Updater per començar el bot amb el nostre token creat a partir del BotFather
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    ### Controlem les comandes de l'usuari ###
    # Aquesta comanda s'encarrega de donar la benvinguda a l'usuari i explicar de que tracta el bot
    dispatcher.add_handler(CommandHandler("start", start))

    # Aquesta comanda explica les funcions que te el bot aixi com explicar-les
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("url", get_url))
    #Handler per veure la resposta de l'usuari al prémer un butó.
    dispatcher.add_handler(CallbackQueryHandler(ask_for_clip))
    #Handler que actua cuando encuentra texto del usuario
    dispatcher.add_handler(MessageHandler(Filters.text, reply))         # Uso handler y muestra que funciona por el terminal

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    updater.idle()


main()