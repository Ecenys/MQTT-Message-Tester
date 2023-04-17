import paho.mqtt.client as mqtt
import socket
from PyQt5.QtWidgets import QMessageBox

# crea el metodo suscriber.Suscriber()
class Suscriber(object):
    def __init__(self):
        self.client = mqtt.Client()

    def disconnect(self):
        # Desconectar del broker MQTT
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, message):
        self.client.publish("topic1", message)
        pass

    def suscribe_topics(self, topics):
        for topic in topics:
            print(f"Subscribiendo a {topic}")
            self.client.subscribe(topic)
        return self.client

    def checkBrokerAddress(self, brokerAddress, port=1883):
        # Si hay una conexion con el broker, se desconecta
        if self.client.is_connected():
            self.client.disconnect()
        try:
            # Creamos un objeto socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Establecemos un tiempo de espera de 1 segundo para la conexión
            sock.settimeout(10)
            # Intentamos conectar al broker en la dirección y puerto especificados
            resultado = sock.connect_ex((brokerAddress, port))
            # Cerramos el socket
            sock.close()
            # Si el resultado de la conexión es 0 (éxito), entonces podemos establecer la conexión
            if resultado == 0:
                #conecta con el broker
                self.client.connect(brokerAddress, port)
                self.client.on_message = self.on_message
                self.client.loop_start()
                print("Conexión con el broker establecida")
                return True
            else:
                return False
        except Exception as e:
            print(f"Ocurrió un error al intentar conectar con el broker: {e}")
            return False


    # Función para manejar los mensajes MQTT recibidos
    def on_message(client, userdata, msg):
        print("estoy aqui")
        print("---------------------------")
        print("---------------------------")
        print("---------------------------")
        print("---------------------------")
        print("---------------------------")
        print("---------------------------")
        global mqtt_messages
        mqtt_messages[msg.topic] = msg.payload.decode()

    # Inicia la conexion con el broker
    # def on_connect(self, client, userdata, flags, rc):
    #     self.client = mqtt.Client()
    #     self.client.on_message = self.on_message
    #     self.client.connect(self.broker, self.port)
    #     self.client.loop_start()
        
    #     # Usuario y contraseña
    #     self.client.username_pw_set(self.username, self.password)
    #     return self.client

if __name__ == "__main__":
    # Inicia la conexion con el broker
    pass
