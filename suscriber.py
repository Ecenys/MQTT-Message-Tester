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

    #Funcion que busca entre los mensajes recibidos el mensaje con el topic especificado y devuelve el payload
    def get_message(self, topic):
        for message in self.messages:
            if message.topic == topic:
                return message.payload

    def suscribe_topics(self, topics):
        for topic in topics:
            self.consoleLog(f"Subscribiendo a {topic}")
            self.client.subscribe(topic)
        return self.client
    
    # Suscribe a un topic
    def suscribe_topic(self, topic):
        self.consoleLog(f"Subscribiendo a {topic}")
        self.client.subscribe(topic)
        return self.client

    def checkBrokerAddress(self, brokerAddress, port=1883, user = None, password = None):
        # Si hay una conexion con el broker, se desconecta
        if self.client.is_connected():
            self.client.disconnect()
        try:
            # Creamos un objeto socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Establecemos un tiempo de espera de 1 segundo para la conexión
            sock.settimeout(10)
            # User y password si no es none
            if user != None and password != None:
                self.client.username_pw_set(user, password)
            # Intentamos conectar al broker en la dirección y puerto especificados
            resultado = sock.connect_ex((brokerAddress, port))
            # Cerramos el socket
            sock.close()
            # Si el resultado de la conexión es 0 (éxito), entonces podemos establecer la conexión
            if resultado == 0:
                #conecta con el broker
                self.client.on_connect = self.on_connect
                self.client.on_message = self.on_message
                self.client.on_subscribe = self.on_subscribe
                self.client.on_disconnect = self.on_disconnect
                self.client.connect(brokerAddress, port)
                self.client.loop_start()
                self.consoleLog("Conexion con el broker establecida")
                return True
            else:
                return False
        except Exception as e:
            self.consoleLog(f"Ocurrió un error al intentar conectar con el broker: {e}")
            return False
        


    # Funcion que se ejecuta cuando se establece la conexion con el broker
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.consoleLog("Conexión exitosa al broker MQTT")
        else:
            self.consoleLog("Error de conexión, código de retorno = ", rc)

    # Funcion que se ejecuta cuando se recibe un mensaje
    def on_message(self, client, userdata, message):
        self.consoleLog(f"Mensaje recibido: {message.topic.decode('utf-8')}")
        self.messages.append(message)
    
    # Funcion que se ejecuta cuando se suscribe a un topic
    def on_subscribe(self, client, userdata, mid, granted_qos):
        #imprime mid y granted_qos
        self.consoleLog(f"Suscripcion exitosa a mid: {mid} y granted_qos: {granted_qos}")

    # Funcion que se ejecuta cuando se desconecta del broker
    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.consoleLog("Desconexion inesperada del broker MQTT")
        else:
            self.consoleLog("Desconexion exitosa del broker MQTT")

if __name__ == "__main__":
    # Inicia la conexion con el broker
    pass
