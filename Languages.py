language = {}
language["Spanish"] = "es"
language["English"] = "en"
language["French"] = "fr"
default = "es"

def giveLanguage(message):
    try:
        return language[message.text]
    except Exception:
        return ""
    
    
def giveLanguajeTranscriptor(lenguaje):
    if lenguaje == "es":
        return "es-ES"
    elif lenguaje == "en":
        return "en-GB"
    elif lenguaje == "fr":
        return "fr-FR"