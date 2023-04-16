import paho.mqtt.client as mqtt
import zipfile

# Descripción de la prueba y pasos del proceso de prueba
description = "Prueba de ejemplo"
steps = [
    {"id": 1, "name": "Init Test",              "description": "test1",                                "status": "pending"},
    {"id": 2, "name": "Send Configuration",     "description": "for the test2",                        "status": "pending"},
    {"id": 3, "name": "Send Ack",               "description": "and the final description",            "status": "pending"}
]

# Lista de topics a suscribirse
topics = ["topic1", "topic2", "topic3"]

# Variable para almacenar los mensajes MQTT recibidos
mqtt_messages = {}

#constructor
def __init__(self):
    # Inicializar el contador de pasos
    self.currentStep = 0

# Función para leer los archivos JSON o CBOR y realizar la prueba
def run(suscriber, zip_filename):
    # Cargar archivos JSON o CBOR desde el archivo ZIP y almacenarlos en una variable
    suscriber.suscribe_topics(topics)
    suscriber.client.publish("init_test_topic", "init_test_message")
    # (Agregar aquí la lógica específica para leer y procesar los archivos)
    print(f"Leyendo archivos desde {zip_filename}...")
    with zipfile.ZipFile(zip_filename, "r") as zip_file:
        for file in zip_file.namelist():
            if file.endswith('.json') or file.endswith('.cbor'):
                zip_file.extract(file)
                with open(file, "rb") as f:
                        mqtt_messages[file] = f

    # Realizar la prueba y avanzar los pasos
    for step in steps:
        # Verificar si el paso ya ha sido completado o fallado
        if step["status"] == "completed" or step["status"] == "failed":
            continue

        # Obtener el mensaje del paso correspondiente
        file = get_step_message(step["id"])

        # Envío de mensaje MQTT
        suscriber.client.publish(file['topic'], file['message'])

        # Esperar a que se reciba la respuesta MQTT
        while file['topic'] not in mqtt_messages:
            pass

        # Actualizar el estado del paso según la respuesta MQTT recibida
        # if mqtt_messages[file['topic']] == "completado":
        #     print(f"Paso {step['id']}: Completado")
        #     step["status"] = "completed"
        # elif mqtt_messages[file['topic']] == "fallo":
        #     print(f"Paso {step['id']}: Fallo")
        #     step["status"] = "failed"
        # else:
        #     print(f"Paso {step['id']}: Realizándose")

    # Desconectar del broker MQTT
    suscriber.client.loop_stop()
    suscriber.client.disconnect()

# Función para obtener el mensaje del paso correspondiente
def get_step_message(step_id):
    # (Agregar aquí la lógica específica para obtener el mensaje del paso según el ID)
    # Ejemplo: en este caso, se retorna un mensaje fijo para cada paso
    if step_id == 1:
        return {"topic": "init_test_topic", "message": "init_test_message"}
    elif step_id == 2:
        return {"topic": "send_configuration_topic", "message": "send_configuration_message"}
    elif step_id == 3:
        return {"topic": "send_ack_topic", "message": "send_ack_message"}

# Ejecutar la prueba
if __name__ == "__main__":
    zip_filename = "test.zip"  # Nombre del archivo ZIP con los archivos de prueba
    run(zip_filename)
