#!/usr/bin/env python
# -*- coding: utf-8 -*

# --- APIS externas --- #

import telebot
import langdetect


# --- Ficheros propios --- # 

import GoogleTranslate
import Transcriptor
import Comands
import Languages
import Poll


# --- CONFIGURACION DEL BOT --- #

TOKEN = '253392761:AAFkYql4kQWckika_zG-99Q_YMiYymxb_s0'
bot = telebot.TeleBot(TOKEN)
#global autoTranslate
#global autoTranscript

last_message = ""
lenguaje  = "es"

isPollStarted = False


# --- --- --- --- --- --- --- #


# --- SE REGISTRAN LOS COMANDOS DISPONIBLES --- #

@bot.message_handler(commands=['help'])
def help_command(message):
    Comands.help_command(message)


@bot.message_handler(commands=['config'])
def config_command(message):
    Comands.config_command(message)


@bot.message_handler(commands=['auto'])
def auto_command(message):
    Comands.auto_command(message)

@bot.message_handler(commands=['manual'])
def manual_command(message):
    Comands.manual_command(message)

@bot.message_handler(commands=['status'])
def status_command(message):
    Comands.status_command(message)


@bot.message_handler(commands=['translate'])
def translate_command(message):
    global last_message
    Comands.translate_command(message, last_message, lenguaje)

@bot.message_handler(commands=['transcribe'])
def transcribe_command(message):
    global lenguaje
    Comands.transcribe_command(message, lenguaje)

@bot.message_handler(commands=['initPoll'])
def initPoll_command(message):
    global isPollStarted
    isPollStarted = True
    bot.send_message(message.chat.id, '''Se ha iniciado el modo encuesta, el siguiente mensaje en formato JSON define la encuesta. Por ejemplo:
        {"title":"Mejor idioma", 
        "English":"Tea and rain", 
        "French":"Ca va", 
        "Spanish":"Tapas y sol"}''')

@bot.message_handler(commands=['endPoll'])
def endPoll_command(message):
    global isPollStarted
    isPollStarted = False
    Poll.finishPoll()
    photo = open('./poll_result.png', 'rb')
    bot.send_photo(message.chat.id, photo)

# --- --- --- --- --- --- --- --- --- --- --- #


# --- Funcion principal, continua espera de mensajes --- #

def listener(mensajes): 
    global lenguaje
    for m in mensajes:
        print Poll.opciones_votos
        print m.text
        chat_id = m.chat.id
        username = m.from_user.username
        if m.content_type == 'voice':
            file_id = m.voice.file_id
            Transcriptor.descargarArchivo(file_id)
            Transcriptor.convertirVozWav()
            if Comands.autoTranscribe:
                Transcriptor.convertirAudioTexto(chat_id, Languages.giveLanguajeTranscriptor(lenguaje), m.from_user.username, chat_id)
        elif m.content_type == 'audio':
            file_id = m.audio.file_id
            fichero = Transcriptor.descargarArchivo(file_id)
            Transcriptor.convertirAudioWav(fichero)
            if Comands.autoTranscribe:
                Transcriptor.convertirAudioTexto(chat_id, Languages.giveLanguajeTranscriptor(lenguaje), username, chat_id)
        elif m.content_type == "text" and isPollStarted and "{" in m.text:
            opciones = Poll.initPoll(m.text, bot.get_chat_members_count(chat_id))
            markup = telebot.types.ReplyKeyboardMarkup()
            markup.one_time_keyboard = True
            for opc in opciones:
                markup.row(opc)
            message = bot.send_message(chat_id, "Elige una alternativa:", reply_markup=markup)
            #bot.register_next_step_handler(message, message.text)
        elif m.content_type == "text" and isPollStarted and m.text in Poll.opciones_votos.keys():
            print "Voto registrado"
            Poll.registerVote(m.text)
        elif m.content_type == "text" and m.text.find("/") == -1: 
            language_detect = langdetect.detect(m.text)
            m.text = m.text.encode("utf-8")
            if Languages.giveLanguage(m) != "":
                lenguaje = Languages.giveLanguage(m)
            elif language_detect != lenguaje: 
                translator = GoogleTranslate.GoogleTranslator()
                text = translator.translate(m.text, lenguaje)[0]
                texto = text[u'translatedText'].replace("&#39;", "'")
                if Comands.autoTranslate or bot.get_chat_members_count(chat_id) == 2:
                    bot.send_message(m.chat.id,texto) 
            global last_message
            last_message = m.text

# --- --- --- ------ --- --- --- --- --- --- --- --- --- #

bot.set_update_listener(listener) 
bot.polling()
