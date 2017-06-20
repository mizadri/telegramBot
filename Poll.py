import matplotlib.pyplot as plt
import json

labels = []
counts = []
votos_recibidos = []
participantes = 1
titulo = ""
opciones_votos = {}

# participantes = 20
# poll_str = '''{"title":"Mejor idioma", "Italiani":"Tea and rain", "French":"Ca va", "Spanish":"Tapas y sol"}'''

# Parsear string que define la encuesta con json.loads(j_str)
def initPoll(poll_str, n):
	global opciones_votos
	global titulo
	global participantes
	# Parsear encuesta 
	opciones_votos = json.loads(poll_str)
	if opciones_votos["title"]:
		titulo = opciones_votos["title"]
		opciones_votos.pop("title")
	# Inicializar el contador de votos para cada opcion
	for label, count in opciones_votos.iteritems():
		opciones_votos[label] = 0
	participantes = n
	return opciones_votos.keys()

# votos_recibidos = ["Spanish","English","Spanish","Spanish","Spanish"
# ,"English","English","French","French","French","English","Spanish"
# ,"English","Spanish","English","Spanish","Spanish","French"]

# Regustrar viti
def registerVote(vote):
	global votos_recibidos
	votos_recibidos.append(vote)

# Recolectar resultados de encuesta y generar grafica
def finishPoll():
	global opciones_votos
	global labels
	global counts
	# Contar los votos recibidos y calcular abstenciones 
	for voto in votos_recibidos:
		opciones_votos[voto] += 1
	n_votos = len(votos_recibidos)
	if  n_votos < participantes - 1:
		opciones_votos["NS/NC"] = participantes - 1 - n_votos
	# Preparar datos de entrada para matplotlib
	for label, count in opciones_votos.iteritems():
		labels.append(label)
		counts.append(count)
	# Obtener el maximo de votos para resaltar su fraccion
	m = max(counts)
	explode = []  
	for el in counts:
		if el == m:
			explode.append(0.1)
		else:
			explode.append(0)
	# Generar la grafica y guardarla en formato PNG
	fig1, ax1 = plt.subplots()
	ax1.pie(counts, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
	ax1.axis('equal')
	if titulo:
		plt.title('%s: %d/%d (votos/participantes)'%(titulo,n_votos,participantes))
	else:
		plt.title('%d/%d (votos/participantes)'%(n_votos,participantes))
	plt.savefig("poll_result.png",bbox_inches='tight')
	plt.close()