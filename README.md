# telegramBot

Proyecto realizado para la asignatura Tecnologías Multimedia e Interacción por Adrián García, Alfonso Tomé y Verónica del Valle. Este bot permite transcribir audios a texto en diferentes idiomas, traducir texto y realizar encuestas a traves de grupos de Telegram. El Token actual de la API se relaciona con el alias @Transcrypt_Bot.

El bot admite lo siguientes comandos:

* **/help**: Este comando muestra al usuario una ayuda indicandole todos los comando que existen en la aplicación y además una breve descripción.
 
* **/config**: Este comando es el encargado de mostrar al usuario un teclado especial en el que se muestran una serie de idiomas para que seleccione su el idioma al que quiere que le traduzca las cosas el bot.
 
* **/status**: Este comando muestra la configuración actual del bot, es decir, si el bot traducirá y transcribirá además del idioma que se ha establecido por defecto.
 
* **/auto**: Activa la traducción y transcripción automática.
 
* **/auto translate**:  Activa únicamente la traducción automática.
 
* **/auto transcribe**:  Activa únicamente la transcripción automática. 
 
* **/manual**: Desactiva la traducción y la transcripción. Este comando sólo está disponible en los grupos.
 
* **/translate [texto]**: Este comando es el encargado de traducir un texto, hay dos opciones enviarle un texto acompañando al comando o no introducir el texto en cuyo caso se traducirá el último mensaje que se haya enviado.
 
* **/transcribe [idioma]**: Este comando se encarga de transcribir un audio, en este caso se le puede indicar el idioma en el que viene el audio junto con el comando y en caso de que no se indique el idioma se considerará que es el idioma por defecto del usuario.
 
* **/initPoll**: Este comando es el encargado de crear la encuesta seguido de una cadena en formato JSON con los campos y los valores.

* **/endPoll**: Finaliza la encuestra y genera una grafica con los resultados.
