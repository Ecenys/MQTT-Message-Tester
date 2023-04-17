# Descripción de la prueba y pasos del proceso de prueba
description = "Prueba de ejemplo"
steps = [
    {"name": "Init Test",              "description": "test1"},
    {"name": "Send Configuration",     "description": "for the test2"}
]

# Lista de topics a suscribirse
topics = ["topic1", "topic2", "topic3"]
i = 0
def awake(self):
    pass

# Función maestra
def run(self):
    suscriber = self.suscriber

    # Cargar archivos JSON o CBOR desde el archivo ZIP y almacenarlos en una variable
    suscriber.suscribe_topics(topics)

def step1(self):
    # (Agregar aquí la lógica específica para el paso 1)
    print("Ejecutando paso 1...")
    self.suscriber.publish("topic1", self.mmt.mqtt_messages[0])
    if self.i >= 10:
        raise self.CompletedTest()
    self.i += 1

def step2(self):
    # (Agregar aquí la lógica específica para el paso 2)
    print("Ejecutando paso 2...")
    raise self.CompletedTest()

def late(self):
    pass