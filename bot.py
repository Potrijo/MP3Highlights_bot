import datetime
import telegram
import youtube_dl
from youtube_dl.utils import limit_length
import yt_dlp
import logging
import os
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

# Amb logging podrem rebre qualsevol error alhora d'interactuar amb l'usuari mitjançant consola, a mes
# ens donara informacio important com la hora o el dia al qual ha ocorregut l'error
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# Loggejar-te com amb el teu usuari
logger = logging.getLogger(__name__)   
# Token del nostre bot creat desde del bot father                             
updater = Updater("2064694571:AAEl-ZpGBdgxekKRSENYCkaSXFj0YGolA60")

# Aquests metodes s'anomenen "command handlers" 
# /start actua el handler següent
def start(update, context):
    # Guarda el nom de l'usuari que escriu el la comanda /start
    user = update.effective_user
    #Mostra el missatge següent
    update.message.reply_markdown_v2(f"Bones {user.mention_markdown_v2()}\!\nAquest bot et permet descarregar MP3 a partir d'enllaços de YouTube, així com editar\\-los a partir d'unes marques de temps o \"timestamps\"\\.\nSi vols aprendre més sobre les funcions d'aquest bot escriu /help")

# /help mostra el missatge següent
def help_command(update, context):
    # Mostra el missatge següent pel chat
    update.message.reply_text("Aquest bot té dos úniques comandes.\n/start: Dona una breu introducció sobre la funció del bot.\n/url: Espera a que l'usuari entri una URL per descarregar el MP3. Un cop ha rebut la URL revisarà si és vàlida o no, en cas de ser-ho descarregarà el arxiu d'audio MP3 i preguntarà a l'usuari què vol fer\\. Pots descarregar els arxius d'audio sense editar o editar\\-los per crear un retall o \"clip\"\nEn cas de retallar el video has d'entrar dos parametres, temps total de l'arxiu i el temps inicial.\nPer entrar temps total has d'escriure: canviar temps HHmmss \n Per entrar el temps inicial de l'audio: canviar longitud HHmmss")
# /url + url de youtube, descarrega el url següent en format d'audio
def get_url(update, context):
    try:
        url = str(context.args[0]) # Agafa l'argument després de /url, és a dir l'enllaç entrat per l'usuari
        check_url(url, update, context) # Comprova que és correcte
    except (IndexError, ValueError) as e:  # En cas de no ser correcte
        update.message.reply_text("No has passat cap argument!") # Mostra el missatge següent

# Descarrega l'audio de l'enllaç captat del mètode anterior
def check_url(url, update, context):
    try:
        update.message.reply_text("Estem descarregant el teu audio, això podria tardar uns minuts.") # Mostra el missatge d'esperar
        video_url = url 
        mp3_info = youtube_dl.YoutubeDL().extract_info( # fem que només descarregui l'enllaç en mp3
            url = video_url,download=False
        )
        
        global videoLength
        videoLength = int(mp3_info.get("duration", None)) # Guardem el contingut del vídeo en la variable global
        print(videoLength) # Imprimim la duració total del vídeo

        global filename 
        filename = f"{mp3_info['title']}.mp3" # Guradem el nom de l'arxiu mp3
        
        options={   # Propietats específicades per obtenir només l'audio
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl': "./MP3/"+ filename,
        }

        with yt_dlp.YoutubeDL(options) as ydl: # Descarreguem l'enllaç
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

        reply_markup = InlineKeyboardMarkup(keyboard) # Objecte que contè els botons

        update.message.reply_text('Vols retallar l\'audio?', reply_markup=reply_markup) # El text amb els botons
        #updater.dispatcher.add_handler(MessageHandler(Filters.text, ask_for_clip))

        #updater.bot.send_audio(chat_id=update.message.chat_id, audio=open(f'./MP3/{filename}', 'rb'))
    except Exception as e:  # En cas de trobar algun problema
        print(e)
        update.message.reply_text("Sembla que ha hagut un error... Torna a intentar-ho més tard o prova amb un altre video.")

# Funcion que guarda el texto
def reply(update: Update, context: CallbackContext):                     
    user_input = update.message.text
    x = user_input.split(" ")
    try:
        if (len(x) == 3)  and (x[0].lower() == "canviar") and (x[1].lower() == "temps"): # Comanda per guardar el temps inicial de l'audio
            startTime = x[2]
            startTimeHours = startTime[0:2] # hores
            startTimeMinutes = startTime[3:5] # minuts
            startTimeSeconds = startTime[6:8] # segons

            global startPoint
            startPoint = str(startTimeHours) + ":" + str(startTimeMinutes) + ":" + str(startTimeSeconds) # format final del temps inicial

            global startInSeconds
            startInSeconds = int(startTime[0:2]) * 3600 + int(startTime[3:5]) * 60 + int(startTime[6:8]) # Càlculs per passar el temps total a segons
            print(str(startInSeconds))

            update.message.reply_text(f"Has canviat el temps d'inici del clip a {startPoint}") # Mostres pel chat que has canviat el temps incial
        elif (len(x) == 3)  and (x[0].lower() == "canviar") and (x[1].lower() == "longitud"): # Mateix sistema per la longitud de l'arxiu
            length = x[2]
            lengthHours = length[0:2]
            lengthMinutes = length[3:5]
            lengthSeconds = length[6:8]

            global fileLength
            fileLength = str(lengthHours) + ":" + str(lengthMinutes) + ":" + str(lengthSeconds)

            global lengthInSeconds
            lengthInSeconds = int(length[0:2])* 3600 + int(length[3:5])* 60 + int(length[6:8])
            print(str(lengthInSeconds))

            update.message.reply_text(f"Has canviat la longitud del clip a {fileLength}")
        else: # En cas d'introduïr incorrectament algun paràmetre
            update.message.reply_text(f"No he entès la teva comanda. Si vols canviar la longitud i el minut d'inici del clip ho has d'esciure en format HH:mm:ss!")
    except ValueError: # Mostra l'excepció
        update.message.reply_text(f"El format ha de ser el següent HH:mm:ss!")
    return user_input # Retorna l'entrada de l'usuari processada

# Funció que mostra realitza una funció en cas de premer Sí i un altre en cas de pulsar No
def ask_for_clip(update: Update, context: CallbackContext):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query   # Guarda en aquesta variable el nom del botó pulsat per l'usuari
    query.answer() 
    try:
        if query.data =='Sí' and fileLength != None and startPoint != None: # En cas afirmatiu
            create_clip() # Crida la funció que retalla l'audio
        if query.data == "No": # En cas negatiu descarrega l'audio sense editarlo i el mostra pel chat
            query.edit_message_text(text=f"Aquí tens l'audio sense editar:") # Mostra el text següent pel chat
            updater.bot.send_audio(chat_id=chatid, audio=open(f'./MP3/{filename}', 'rb')) # L'envia amb el seu nom
    except NameError:   # En cas d'haver algun error mostra el missatge següent 
        updater.dispatcher.bot.sendMessage(chat_id=chatid, text="Sembla que no has definit la longitud i punt d'inici")

# En cas d'escollir l'acció de retallar  
def create_clip():
    try:
        print(str(lengthInSeconds + startInSeconds))
        if videoLength < (lengthInSeconds + startInSeconds): # Si introdueixes els paràmetres correctement
            os.system(f'ffmpeg -ss {startPoint} -i ./MP3/"{filename}" -y -t {fileLength} ./Clips/"clip_{filename}"')
            updater.bot.send_audio(chat_id=chatid, audio=open(f'./Clips/clip_{filename}', 'rb'))
    except Exception as e: # En cas contrari, el programa mostrarà el text següent
        updater.dispatcher.bot.sendMessage(chat_id=chatid, text="Sembla que has introduit uns valors invàlids")

# Mètode principal del programa, és l'execució de totes les funcions creades anteriorment
def main():
    ### Settings ###
    # Truquem al Updater per començar el bot amb el nostre token creat a partir del BotFather
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    ### Controlem les comandes de l'usuari ###
    # Aquesta comanda s'encarrega de donar la benvinguda a l'usuari i explicar de que tracta el bot
    dispatcher.add_handler(CommandHandler("start", start)) # Dispacther és el controlador de tots els handlers possibles, command handler troba /"nom de la funció especificada entre cometes y realitza la funció després de les cometes d'aquesta"

    # Aquesta comanda explica les funcions que te el bot aixi com explicar-les
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("url", get_url))
    #Handler per veure la resposta de l'usuari al prémer un butó.
    dispatcher.add_handler(CallbackQueryHandler(ask_for_clip))
    #Handler que actua cuando encuentra texto del usuario
    dispatcher.add_handler(MessageHandler(Filters.text, reply))         # Escolta el text de l'usuari sense necessitat de buscar cap /

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    updater.idle()


main()