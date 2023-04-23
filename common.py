import cbor
import json
import binascii

from datetime import datetime
from collections import OrderedDict

class common(object):

    # Funcion que tranforma de json a cbor
    def json_to_cbor(self, json_data):
        return cbor.dumps(json_data)
    
    # Funcion que tranforma de cbor a json
    def cbor_to_json(self, cbor_data):
        return cbor.loads(cbor_data)
    
    # Funcion que tranforma de json a string
    def json_to_string(self, json_data):
        return json.dumps(json_data)
    
    # Funcion que tranforma de cbor a string
    def cbor_to_string(self, cbor_data):
        return json.dumps(cbor.loads(cbor_data))
    
    # Funcion que tranforma de string a json
    def string_to_json(self, string_data):
        return json.loads(string_data)
    
    # Funcion que tranforma de string a cbor
    def string_to_cbor(self, string_data):
        return cbor.dumps(json.loads(string_data))
    
    # Calculo de CRC32 de un json
    def crc32(self, json_data):
        return binascii.crc32(json.dumps(json_data).encode('utf-8'))
    
    # Creacion de un mensaje en formato IRMS
    # json_data = {
        # 3300:{
        #  5700: "Juan"},
        # 3301:{
        #  5700: 30,
        #  5701: 0.5}
        # }
    # create_IRMS(101104, 0, 0, 0, json_data)
    def create_IRMS(service, gateway, source, nodeID, nodesData):
        message_dict = OrderedDict()
        message_dict['ServiceID'] = int(service)
        root = OrderedDict()
        timeStamp = datetime.now().timestamp()
        root['Gateway'] = gateway
        root['Source'] = source
        root['TimeStamp'] = int(timeStamp)
        message_dict['Root'] = root
        nodesList = []
        node = OrderedDict()
        node['Safety'] = True
        node['NodeID'] = nodeID
        timeStamp = datetime.now().timestamp()
        node['TimeStamp'] = int(timeStamp)
        node['TimeAccuracy'] = int((timeStamp % 1) * pow(10, 9))
        sensors = []
        for nodeSensor in nodesData.keys():
            sensor = OrderedDict()
            sensor['SensorID'] = nodeSensor
            sensor['TimeStamp'] = int(timeStamp)
            sensor['TimeAccuracy'] = int((timeStamp % 1) * pow(10, 9))
            resources = OrderedDict()
            for sensorResource in nodesData[nodeSensor]:
                resources[sensorResource] = nodesData[nodeSensor][sensorResource]
                sensor['Resources'] = resources
            sensors.append(sensor)
        node["Sensors-Actuators"] = sensors
        node["CRC"] = 0
        bytesCRC= bytearray(cbor.dumps(node))[:-1]
        node["CRC"] = binascii.crc32(bytesCRC)
        nodesList.append(node)
        message_dict['Nodes'] = nodesList
        message_dict['CRC'] = 0
        bytesCRC= bytearray(cbor.dumps(message_dict))[:-1]
        message_dict["CRC"] = binascii.crc32(bytesCRC)
        return (json.dumps(message_dict))
        