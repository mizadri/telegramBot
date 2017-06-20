import telebot

import GoogleTranslate
import Languages
import Transcriptor

autoTranslate = True
autoTranscribe = True

TOKEN = '253392761:AAFkYql4kQWckika_zG-99Q_YMiYymxb_s0'
bot = telebot.TeleBot(TOKEN)


def help_command(message):
    cadena = "/help - Muestra la ayuda para el uso de los comandos. \n"
    cadena += "/config - Modifica el idioma del usuario. \n"
    cadena += "/auto - Activa la traduccion y transcripcion automatica. Obligatorio en chat individuales. \n"
    cadena += "/manual - Desactiva la traduccion y transcripcion automatica. Solo disponible para grupos. \n"
    cadena += "/status - Informa sobre el estado de la configuracion (manual o automatica). \n"
    cadena += "/translate - Traduce el ultimo texto enviado o el enviado a continuacion del comando. \n"
    cadena += "/transcribe - Transcribe el ultimo audio enviado en el idioma del usuario o el indicado a continuacion del comando.\n"
    cadena += "/initPoll - En los siguientes mensajes recibidos se intentara configurar una encuesta mediante una cadena JSON.\n"
    cadena += "/endPoll - Finaliza la encuestra y genera una grafica con los resultados."
    bot.send_message(message.chat.id, cadena)


def config_command(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.row('Spanish')
    markup.row("English")
    markup.row("French")
    markup.one_time_keyboard = True
   
    message = bot.send_message(message.chat.id, "Selecciona una accion:", reply_markup=markup)
    bot.register_next_step_handler(message, message.text)
    

def auto_command(message):
    global autoTranslate
    global autoTranscribe
    if bot.get_chat_members_count(message.chat.id) > 2:
        parts = message.text.split(" ")
        if len(parts) > 1 and parts[1] == "translate":
            bot.send_message(message.chat.id, "Traduccion automatica activada") 
            autoTranslate = True
            autoTranscribe = False
            print "Activar translate"
        elif len(parts) > 1 and parts[1] == "transcribe":
            bot.send_message(message.chat.id, "Transcripcion automatica activada") 
            autoTranslate = False
            autoTranscribe = True
            print "Activar transcript"
        elif len(parts) > 1:
            bot.send_message(message.chat.id, "Por favor introduzca que desea activar o envie solo /auto para activar todo") 
        elif len(parts) == 1:
            autoTranslate = True
            autoTranscribe = True
            print "Activa todo"
            bot.send_message(message.chat.id, "Respuesta automatica activada")
    else:
        bot.send_message(message.chat.id, "Configuracion obligatoria para chats individuales") 


def manual_command(message):
    global autoTranslate
    global autoTranscribe
    if bot.get_chat_members_count(message.chat.id) > 2:
        autoTranslate = False
        autoTranscribe = False
        bot.send_message(message.chat.id, "Si quieres seguir recibiendo las traducciones y transcripciones crea una conversacion mendiante el siguiente enlace")
        bot.send_message(message.chat.id, "telegram.me/TMIPruebaBot")
    else:
        bot.send_message(message.chat.id, "Opcion no disponible para chats individuales") 
        return True


def status_command(message):
    if autoTranscribe:
        cadena = "autoTranscribe: Activado \n"
    else:
        cadena = "autoTranscribe: Desactivado \n" 
    
    if autoTranslate:
        cadena = cadena + "autoTranslate: Activado"
    else:
        cadena = cadena + "autoTranslate: Desactivado"
    bot.send_message(message.chat.id, cadena)
    


def translate_command(message, last_message, lenguaje):
    separador = message.text.split("/translate")
    # Traduce el mensaje que acompania al comando
    if len(separador[1]) > 0:
        translator = GoogleTranslate.GoogleTranslator()
        text = translator.translate(message.text, lenguaje)[0]
        bot.send_message(message.from_user.id,text[u'translatedText'])
    # Traduce el ultimo mensaje que le ha llegado
    else :
        print last_message
        translator = GoogleTranslate.GoogleTranslator()
        text = translator.translate(last_message, lenguaje)[0]
        bot.send_message(message.from_user.id,text[u'translatedText'])


def transcribe_command(message, lenguaje):
    separador = message.text.split(" ")
    # Se transcribe al idioma indicado a traves del comando
    if len(separador) == 2:
        Transcriptor.convertirAudioTexto(message.from_user.id, Languages.language[separador[1]], message.from_user.username, message.chat.id)
    # Se transcribe al idioma por defecto
    else :
        Transcriptor.convertirAudioTexto(message.from_user.id, Languages.giveLanguajeTranscriptor(lenguaje), message.from_user.username, message.chat.id)

