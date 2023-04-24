import paho.mqtt.client as mqtt
import socket
from PyQt5.QtWidgets import QMessageBox

# crea el metodo suscriber.Suscriber()
class Suscriber(object):
    def __init__(self):
        self.client = mqtt.Client()
        self.messages = []
        self.last_message_position = 0

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
            print(f"Subscribiendo a {topic}")
            self.client.subscribe(topic)
        return self.client
    
    # Suscribe a un topic
    def suscribe_topic(self, topic):
        print(f"Subscribiendo a {topic}")
        self.client.subscribe(topic)
        return self.client

    def checkBrokerAddress(self, brokerAddress, port, user = None, password = None):
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
                print("Conexion con el broker establecida")
                return True
            else:
                return False
        except Exception as e:
            print(f"Ocurrió un error al intentar conectar con el broker: {e}")
            return False
        


    # Funcion que se ejecuta cuando se establece la conexion con el broker
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conexión exitosa al broker MQTT")
        else:
            print("Error de conexión, código de retorno = ", rc)

    # Funcion que se ejecuta cuando se recibe un mensaje
    def on_message(self, client, userdata, message):
        print(f"Mensaje recibido: {message.topic}")
        self.messages.append(message)

    # Funcion que se ejecuta cuando se suscribe a un topic
    def on_subscribe(self, client, userdata, mid, granted_qos):
        #imprime mid y granted_qos
        print(f"Suscripcion exitosa a mid: {mid} y granted_qos: {granted_qos}")

    # Funcion que se ejecuta cuando se desconecta del broker
    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Desconexion inesperada del broker MQTT")
        else:
            print("Desconexion exitosa del broker MQTT")

    # Funcion que devuelve el mensaje con el topic y si no lo encuentra devuelve None
    def get_single_message(self, topic):
        for message in self.messages:
            if topic in message.topic:
                return message.payload
        return None
    
    # Funcion que devuelve el ultimo mensaje con el topic y si no lo encuentra devuelve None
    def get_last_message(self, topic):
        for message in reversed(self.messages):
            if topic in message.topic:
                return message.payload
        return None

    # Funcion que devuelve todos los mensajes con el topic y si no lo encuentra devuelve una lista vacia
    def get_all_messages(self, topic):
        messages = []
        for message in self.messages:
            if topic in message.topic :
                messages.append(message.payload)
        return messages

    # Resetea last_message_position a 0
    def reset_last_message_position(self):
        self.last_message_position = 0

    # Actualiza last_message_position a la ultima posicion de la lista de mensajes
    def update_last_message_position(self):
        self.last_message_position = len(self.messages) - 1

    # Funcion que devuelve, entre todos los mensajes recibidos desde la ultima llamada a esta funcion, el mensaje con el topic y si no lo encuentra devuelve None
    # Se guardará la posicion del ultimo mensaje con el topic en la variable last_message_position
    def get_message_from_last_call(self, topic):
        for message in self.messages[self.last_message_position:]:
            self.last_message_position = self.messages.index(message)
            if topic in message.topic:
                return message.payload
        return None
    
    # Funcion que devuelve el topic de un mensaje con el que concuerde el payload, si no lo encuentra devuelve None
    def get_topic_from_message(self, payload):
        for message in self.messages:
            if message.payload == payload:
                return message.topic
        return None
    
    # Funcion que devuelve el topic de todos los mensajes con el que concuerde el payload, si no lo encuentra devuelve None
    def get_all_topics_from_message(self, payload):
        topics = []
        for message in self.messages:
            if message.payload == payload:
                topics.append(message.topic)
        return topics
    
    # Funcion que se le pasa una lista de topics, busca en la lista y si encuentra alguno devuelve el topic, si no lo encuentra devuelve None
    def search_topic_from_list(self, topics):
        for message in self.messages:
            if message.topic in topics:
                return message.topic
        return None

if __name__ == "__main__":
    # Inicia la conexion con el broker
    pass
