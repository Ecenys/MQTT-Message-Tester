# Descripción de la prueba y pasos del proceso de prueba
description = "Inauguration Test for SIP"
steps = [
    {"name": "Init Integrity",         "description": "Envio de mensaje 101100 con source 505 y espera de mensaje 101100 con source 503"},
    {"name": "WSN Response",           "description": "Se ha recibido el mensaje 101100 con source 503, las WSN contestan con un 101103 y la SIP debe enviar un 101104"},
    {"name": "Node Notification",      "description": "Se ha recibido el 101104 de la SIP, se debe enviar un 101105 y esperar un 101106"},
    {"name": "Node Confirmation",      "description": "Se ha recibido el 101106 de la SIP, se debe enviar un 101107 y esperar un 101110"},
    {"name": "End Test",               "description": "Se ha recibido el 101110 de la SIP. El test ha finalizado con exito"}
]

# Lista de topics a suscribirse
topics = ["101/#"]
i = 0
intentsInStep = 0
firstTry = True

def awake(self):
    pass

def betweenSteps(self):
    self.firstTry = True
    self.intentsInStep = 0

# Función maestra
def run(self):
    # Cargar archivos JSON o CBOR desde el archivo ZIP y almacenarlos en una variable
    self.suscriber.suscribe_topics(topics)

    # {"name": "Init Integrity",         "description": "Envio de mensaje 101100 con source 505 y espera de mensaje 101100 con source 503"}
def step1(self):
    self.consoleLog("Ejecutando paso 1...")
    if (self.firstTry):
        self.suscriber.publish("101/100/0/0/505/100/101", self.mmt.mqtt_messages[0])
        self.firstTry = False

    if (self.suscriber.get_message_from_last_call("101/100/0/0/503")):
        raise self.CompletedStep()
    
    self.intentsInStep += 1
    if (self.intentsInStep >= 100):
        raise self.FailedStep()
    

def step2(self):
    print("Ejecutando paso 2...")
    if (self.firstTry):
        self.suscriber.publish("101/103", self.mmt.mqtt_messages[1])
        self.firstTry = False

    if (self.suscriber.get_message_from_last_call("101/104")):
        raise self.CompletedStep()
    
    self.intentsInStep += 1
    if (self.intentsInStep >= 100):
        raise self.FailedStep()


def step3(self):
    print("Ejecutando paso 3...")
    if (self.firstTry):
        self.suscriber.publish("101/105", self.mmt.mqtt_messages[3])
        self.firstTry = False

    if (self.suscriber.get_message_from_last_call("101/106")):
        raise self.CompletedStep()
    
    self.intentsInStep += 1
    if (self.intentsInStep >= 100):
        raise self.FailedStep()

def step4(self):
    print("Ejecutando paso 4...")
    if (self.firstTry):
        self.suscriber.publish("101/107", self.mmt.mqtt_messages[5])
        firstTry = False

    if (self.suscriber.get_message_from_last_call("101/110")):
        raise self.CompletedStep()
    
    self.intentsInStep += 1
    if (self.intentsInStep >= 100):
        raise self.FailedStep()

def step5(self):
    print("Ejecutando paso 5...")
    raise self.FinishedTest()

def late(self):
    pass