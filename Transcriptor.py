import telebot
import pydub 
import urllib2
import speech_recognition as sr

TOKEN = '378150155:AAElHn0FFP6btekZILgVYoq6HcTSo5Nr744' 
bot = telebot.TeleBot(TOKEN)


# --- Funcion encargada de guardar en local el archivo recien enviado, almacenado en los servicios de telegram --- #

def descargarArchivo(file_id): 
    file_info = bot.get_file(file_id)
    # Se separa por "." para obtener la extension del archivo 
    separador = file_info.file_path.split(".")
    extension = separador[len(separador)-1]
    # Se indica el nombre del archivo a guardar
    archivoGuardar = "audio."+extension
    
    # Se descarga el archivo de los servicios de telegram
    archivoDescargar = 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path)
    descarga = urllib2.urlopen(archivoDescargar)
    
    ficheroGuardar=file(archivoGuardar,"w")
    ficheroGuardar.write(descarga.read())
    ficheroGuardar.close()
    
    return archivoGuardar


# --- Funcion encargada de convertir un archivo de voz (.OGA) a .WAV ---#

def convertirVozWav(): 
    # Se convierto el audio a .WAV haciendo uso de pydub
    ogg_version = pydub.AudioSegment.from_ogg("audio.oga")
    ogg_version.export("audio.wav", format="wav")        


# --- Funcion encarga de convertir archivos de audio, en multiples formatos (mp4, mp3, ogg, flv ...) a .WAV --- #

def convertirAudioWav(fichero):
    # Se separa por "." para obtener la extension del archivo
    separador = fichero.split(".")
    extension = separador[len(separador)-1]
    # Se convierto el audio a .WAV haciendo uso de pydub
    ogg_version = pydub.AudioSegment.from_file(fichero, format=extension)
    ogg_version.export("audio.wav", format="wav")  


# --- Funcion encargada de convertir un audio a formato texto utilizando la API de BING --- #

def convertirAudioTexto(chat_id, idioma, username, idChatError):
    r = sr.Recognizer()
    with sr.WavFile("audio.wav") as source:             
        audio = r.record(source)
    
    try:
        KEY_BING = "0e542302909f4a29b70715e9acc99e41"
        texto = r.recognize_bing(audio,KEY_BING,idioma,False)
        bot.send_message(chat_id,"@"+str(username)+": "+texto)
        
    except Exception:
        print "He dado error"
        bot.send_message(idChatError,"@"+str(username)+": telegram.me/TMIPruebaBot")


