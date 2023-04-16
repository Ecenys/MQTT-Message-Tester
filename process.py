import paho.mqtt.client as mqtt
import zipfile

# Descripción de la prueba y pasos del proceso de prueba
description = "Prueba de ejemplo"
steps = [
    {"id": 1, "name": "Init Test",              "description": "test1"},
    {"id": 2, "name": "Send Configuration",     "description": "for the test2"}
]

# Lista de topics a suscribirse
topics = ["topic1", "topic2", "topic3"]

# Variable para almacenar los mensajes MQTT recibidos
mqtt_messages = {}

#constructor
def __init__(self):
    # Inicializar el contador de pasos
    self.currentStep = 1

def initTest(self, suscriber, zip_filename):
    self.suscriber = suscriber

    # Cargar archivos JSON o CBOR desde el archivo ZIP y almacenarlos en una variable
    suscriber.suscribe_topics(topics)

    # (Agregar aquí la lógica específica para leer y procesar los archivos)
    print(f"Leyendo archivos desde {zip_filename}...")
    i = 0
    with zipfile.ZipFile(zip_filename, "r") as zip_file:
        for file in zip_file.namelist():
            if file.endswith('.json') or file.endswith('.cbor'):
                zip_file.extract(file)
                with open(file, "r", encoding='utf-8') as f:
                        mqtt_messages[i] = f.read()
                        i += 1

# Función maestra
def run(suscriber, zip_filename):
    # Inicializar la prueba
    initTest(suscriber, zip_filename)

    #bloque
    # Realizar la prueba y avanzar los pasos
    for step in steps:
        # Verificar si el paso ya ha sido completado o fallado
        if step["status"] == "completed" or step["status"] == "failed":
            continue
        # Obtener el mensaje del paso correspondiente
        # Envío de mensaje MQTT
        
        # Esperar a que se reciba la respuesta MQTT
        # while file['topic'] not in mqtt_messages:
        #     pass

def step1(self):
    # (Agregar aquí la lógica específica para el paso 1)
    print("Ejecutando paso 1...")
    self.suscriber.client.publish(mqtt_messages[0])

def step2(self):
    # (Agregar aquí la lógica específica para el paso 2)
    print("Ejecutando paso 2...")

# Ejecutar la prueba
if __name__ == "__main__":
    zip_filename = "test.zip"  # Nombre del archivo ZIP con los archivos de prueba
    run(zip_filename)
