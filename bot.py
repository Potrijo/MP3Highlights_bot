import youtube_dl
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Amb logging podrem rebre qualsevol error alhora d'interactuar amb l'usuari mitjançant consola, a mes
# ens donara informacio important com la hora o el dia al qual ha ocorregut l'error
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
updater = Updater("2121509067:AAHhIvVRswapHu5ucYCuSmZ8IhyGnX86k4s")

# Aquests metodes s'anomenen "command handlers" 
def start(update, context):
    user = update.effective_user
    update.message.reply_markdown_v2(f"Bones {user.mention_markdown_v2()}\!\nAquest bot et permet descarregar MP3 a partir d'enllaços de YouTube, així com editar\\-los a partir d'unes marques de temps o \"timestamps\"\\.\nSi vols aprendre més sobre les funcions d'aquest bot escriu /help\\.")


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

        filename = f"{mp3_info['title']}.mp3"
        
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl': "./MP3/"+ filename,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([mp3_info['webpage_url']])
            
            updater.bot.send_audio(chat_id=update.message.chat_id, audio=open(f'./MP3/{filename}', 'rb'))
    except Exception as e:
        print(e)
        update.message.reply_text("Sembla que ha hagut un error... Torna a intentar-ho més tard o prova amb un altre video.")


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

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    updater.idle()


main()