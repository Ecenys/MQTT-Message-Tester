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
    def get_message_from_last_call_that_topic_contains(self, topic):
        for message in self.messages[self.last_message_position:]:
            self.last_message_position = self.messages.index(message)
            if topic in message.topic:
                return message.payload
        return None
    
    # Funcion que devuelve, entre todos los mensajes recibidos desde la ultima llamada a esta funcion, todos los mensajes con el topic y si no lo encuentra devuelve una lista vacia
    # Se guardará la posicion del ultimo mensaje con el topic en la variable last_message_position
    def get_all_messages_from_last_call_that_topic_contains(self, topic):
        messages = []
        for message in self.messages[self.last_message_position:]:
            self.last_message_position = self.messages.index(message)
            if topic in message.topic:
                messages.append(message.payload)
        return messages
    
    # # Funcion que devuelve el topic de un mensaje con el que concuerde el payload, si no lo encuentra devuelve None
    # def get_topic_from_message(self, payload):
    #     for message in self.messages:
    #         if message.payload == payload:
    #             return message.topic
    #     return None
    
    # # Funcion que devuelve el topic de todos los mensajes con el que concuerde el payload, si no lo encuentra devuelve None
    # def get_all_topics_from_message(self, payload):
    #     topics = []
    #     for message in self.messages:
    #         if message.payload == payload:
    #             topics.append(message.topic)
    #     return topics
    
    # # Funcion que se le pasa un topic, busca en la lista y si encuentra alguno devuelve el topic, si no lo encuentra devuelve None
    # # El topic puede tener + que significa que lo que hay entre el + y el / anterior puede ser cualquier cosa
    # # El topic puede tener # que significa que lo que hay despues del # puede ser cualquier cosa
    # # La funcion irá comprobando cada nivel del topic, si ese nivel tiene un +, lo salta y si tiene un #, devuelve el topic
    # def search_topic(self, topic):
    #     for message in self.messages:
    #         topic_list = topic.split("/")
    #         message_topic_list = message.topic.split("/")
    #         if len(topic_list) <= len(message_topic_list):
    #             for i in range(len(topic_list)):
    #                 if topic_list[i] == message_topic_list[i] or topic_list[i] == "+":
    #                     if i == len(message_topic_list) - 1:
    #                         return message.topic
    #                 elif topic_list[i] == "#":
    #                     return message.topic
    #                 else:
    #                     break
    #     return None
    
    # # Funcion que se le pasa un topic, busca en la lista y si encuentra alguno devuelve el topic, si no lo encuentra devuelve None
    # # El topic puede tener + que significa que lo que hay entre el + y el / anterior puede ser cualquier cosa
    # # El topic puede tener # que significa que lo que hay despues del # puede ser cualquier cosa
    # # La funcion irá comprobando cada nivel del topic, si ese nivel tiene un +, lo salta y si tiene un #, devuelve el topic
    # def search_all_topics(self, topic):
    #     topics = []
    #     for message in self.messages:
    #         topic_list = topic.split("/")
    #         message_topic_list = message.topic.split("/")
    #         if len(topic_list) <= len(message_topic_list):
    #             for i in range(len(topic_list)):
    #                 if topic_list[i] == message_topic_list[i] or topic_list[i] == "+":
    #                     if i == len(message_topic_list) - 1:
    #                         topics.append(message.topic)
    #                 elif topic_list[i] == "#":
    #                     topics.append(message.topic)
    #                 else:
    #                     break
    #     return topics
    
    # # Funcion que se le pasa un topic, busca en la lista desde la ultima llamada y si encuentra alguno devuelve el topic, si no lo encuentra devuelve None
    # # El topic puede tener + que significa que lo que hay entre el + y el / anterior puede ser cualquier cosa
    # # El topic puede tener # que significa que lo que hay despues del # puede ser cualquier cosa
    # # La funcion irá comprobando cada nivel del topic, si ese nivel tiene un +, lo salta y si tiene un #, devuelve el topic
    # def search_topic_from_last_call(self, topic):
    #     for message in self.messages[self.last_message_position:]:
    #         self.last_message_position = self.messages.index(message)
    #         topic_list = topic.split("/")
    #         message_topic_list = message.topic.split("/")
    #         if len(topic_list) <= len(message_topic_list):
    #             for i in range(len(topic_list)):
    #                 if topic_list[i] == message_topic_list[i] or topic_list[i] == "+":
    #                     if i == len(message_topic_list) - 1:
    #                         return message.topic
    #                 elif topic_list[i] == "#":
    #                     return message.topic
    #                 else:
    #                     break
    #     return None
    
    # # Funcion que se le pasa un topic, busca en la lista desde la ultima llamada y si encuentra alguno devuelve el topic, si no lo encuentra devuelve None
    # # El topic puede tener + que significa que lo que hay entre el + y el / anterior puede ser cualquier cosa
    # # El topic puede tener # que significa que lo que hay despues del # puede ser cualquier cosa
    # # La funcion irá comprobando cada nivel del topic, si ese nivel tiene un +, lo salta y si tiene un #, devuelve el topic
    # def search_all_topics_from_last_call(self, topic):
    #     topics = []
    #     for message in self.messages[self.last_message_position:]:
    #         self.last_message_position = self.messages.index(message)
    #         topic_list = topic.split("/")
    #         message_topic_list = message.topic.split("/")
    #         if len(topic_list) <= len(message_topic_list):
    #             for i in range(len(topic_list)):
    #                 if topic_list[i] == message_topic_list[i] or topic_list[i] == "+":
    #                     if i == len(message_topic_list) - 1:
    #                         topics.append(message.topic)
    #                 elif topic_list[i] == "#":
    #                     topics.append(message.topic)
    #                 else:
    #                     break
    #     return topics

    # # Funcion que se le pasa un topic, busca en la lista y si encuentra alguno devuelve el payload, si no lo encuentra devuelve None
    # # El topic puede tener + que significa que lo que hay entre el + y el / anterior puede ser cualquier cosa
    # # El topic puede tener # que significa que lo que hay despues del # puede ser cualquier cosa
    # # La funcion irá comprobando cada nivel del topic, si ese nivel tiene un +, lo salta y si tiene un #, devuelve el topic
    # def get_message(self, topic):
    #     for message in self.messages:
    #         topic_list = topic.split("/")
    #         message_topic_list = message.topic.split("/")
    #         if len(topic_list) == len(message_topic_list):
    #             for i in range(len(topic_list)):
    #                 if topic_list[i] == message_topic_list[i] or topic_list[i] == "+":
    #                     if i == len(topic_list) - 1:
    #                         return message.payload
    #                 elif topic_list[i] == "#":
    #                     return message.payload
    #                 else:
    #                     break
    #     return None
    
    # # Funcion que se le pasa un topic, busca en la lista y si encuentra alguno devuelve el payload, si no lo encuentra devuelve None
    # # El topic puede tener + que significa que lo que hay entre el + y el / anterior puede ser cualquier cosa
    # # El topic puede tener # que significa que lo que hay despues del # puede ser cualquier cosa
    # # La funcion irá comprobando cada nivel del topic, si ese nivel tiene un +, lo salta y si tiene un #, devuelve el topic
    # def get_all_messages(self, topic):
    #     messages = []
    #     for message in self.messages:
    #         topic_list = topic.split("/")
    #         message_topic_list = message.topic.split("/")
    #         if len(topic_list) == len(message_topic_list):
    #             for i in range(len(topic_list)):
    #                 if topic_list[i] == message_topic_list[i] or topic_list[i] == "+":
    #                     if i == len(topic_list) - 1:
    #                         messages.append(message.payload)
    #                 elif topic_list[i] == "#":
    #                     messages.append(message.payload)
    #                 else:
    #                     break
    #     return messages

    # # Funcion que se le pasa un topic, busca en la lista desde la ultima llamada y si encuentra alguno devuelve el payload, si no lo encuentra devuelve None
    # # El topic puede tener + que significa que lo que hay entre el + y el / anterior puede ser cualquier cosa
    # # El topic puede tener # que significa que lo que hay despues del # puede ser cualquier cosa
    # # La funcion irá comprobando cada nivel del topic, si ese nivel tiene un +, lo salta y si tiene un #, devuelve el topic
    # def get_message_from_last_call(self, topic):
    #     for message in self.messages[self.last_message_position:]:
    #         self.last_message_position = self.messages.index(message)
    #         topic_list = topic.split("/")
    #         message_topic_list = message.topic.split("/")
    #         if len(topic_list) == len(message_topic_list):
    #             for i in range(len(topic_list)):
    #                 if topic_list[i] == message_topic_list[i] or topic_list[i] == "+":
    #                     if i == len(topic_list) - 1:
    #                         return message.payload
    #                 elif topic_list[i] == "#":
    #                     return message.payload
    #                 else:
    #                     break
    #     return None
    
    # # Funcion que se le pasa un topic, busca en la lista desde la ultima llamada y si encuentra alguno devuelve el payload, si no lo encuentra devuelve None
    # # El topic puede tener + que significa que lo que hay entre el + y el / anterior puede ser cualquier cosa
    # # El topic puede tener # que significa que lo que hay despues del # puede ser cualquier cosa
    # # La funcion irá comprobando cada nivel del topic, si ese nivel tiene un +, lo salta y si tiene un #, devuelve el topic
    # def get_all_messages_from_last_call(self, topic):
    #     messages = []
    #     for message in self.messages[self.last_message_position:]:
    #         self.last_message_position = self.messages.index(message)
    #         topic_list = topic.split("/")
    #         message_topic_list = message.topic.split("/")
    #         if len(topic_list) == len(message_topic_list):
    #             for i in range(len(topic_list)):
    #                 if topic_list[i] == message_topic_list[i] or topic_list[i] == "+":
    #                     if i == len(topic_list) - 1:
    #                         messages.append(message.payload)
    #                 elif topic_list[i] == "#":
    #                     messages.append(message.payload)
    #                 else:
    #                     break
    #     return messages

    # Funcion que se le pasa un topic, busca en la lista desde la ultima llamada y si encuentra alguno devuelve el payload, si no lo encuentra devuelve None
    def match_topic(self, topic_list, message_topic_list):
        for i in range(len(topic_list)):
            if topic_list[i] == message_topic_list[i] or topic_list[i] == "+":
                if i == len(topic_list) - 1:
                    return True
            elif topic_list[i] == "#":
                return True
            else:
                break
        return False

    # Funcion que se le pasa un topic, busca en la lista desde la ultima llamada y si encuentra alguno devuelve el topic, si no lo encuentra devuelve None
    def search_topics(self, messages, topic, last_message_position=None):
        if last_message_position is None:
            last_message_position = 0
        result = []
        for message in messages[last_message_position:]:
            message_topic_list = message.topic.split("/")
            topic_list = topic.split("/")
            if len(topic_list) == len(message_topic_list):
                if self.match_topic(topic_list, message_topic_list):
                    result.append(message.topic)
        return result
    
    def search_topic_from_last_call(self, topic):
        result = self.search_topics(self.messages, topic, last_message_position=self.last_message_position)
        if result:
            return result[-1]
        return None
    
    def search_all_topics_from_last_call(self, topic):
        result = self.search_topics(self.messages, topic, last_message_position=self.last_message_position)
        return result
    
    def search_topic(self, topic):
        result = self.search_topics(self.messages, topic)
        if result:
            return result[-1]
        return None
    
    def search_all_topics(self, topic):
        result = self.search_topics(self.messages, topic)
        return result

    # Funcion que se le pasa un topic, busca en la lista desde la ultima llamada y si encuentra alguno devuelve el payload, si no lo encuentra devuelve None
    def search_messages(self, messages, topic, last_message_position=None):
        if last_message_position is None:
            last_message_position = 0
        result = []
        for message in messages[last_message_position:]:
            message_topic_list = message.topic.split("/")
            topic_list = topic.split("/")
            if len(topic_list) == len(message_topic_list):
                if self.match_topic(topic_list, message_topic_list):
                    result.append(message.payload)
        return result

    def get_message_from_last_call(self, topic):
        result = self.search_messages(self.messages, topic, last_message_position=self.last_message_position)
        if result:
            self.last_message_position = self.messages.index(next(iter(self.result)))
            return result[0]
        return None

    def get_all_messages_from_last_call(self, topic):
        result = self.search_messages(self.messages, topic, last_message_position=self.last_message_position)
        self.last_message_position = self.messages.index(self.messages[-1]) + 1
        return result

    def get_message(self, topic):
        result = self.search_messages(self.messages, topic)
        if result:
            return result[0]
        return None

    def get_all_messages(self, topic):
        return self.search_messages(self.messages, topic)


if __name__ == "__main__":
    # Inicia la conexion con el broker
    pass
