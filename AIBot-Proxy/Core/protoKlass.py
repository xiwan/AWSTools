

from google.protobuf.json_format import MessageToJson, MessageToDict
import progen.python.todolist_pb2 as TodoList

class ProtoKlass:
    def __init__(self):
        pass

    def MessageToJson(self, message):
        return MessageToJson(message)

    def MessageToDict(self, message):
        return MessageToDict(message)
    
    def SerializeToString(self, message):
        return message.SerializeToString()
    
    def ParseFromString(self, message, bin):
        message.ParseFromString(bin)

    def Handler(self, recv_data):
        protoData = TodoList.TodoList()

        self.ParseFromString(protoData, recv_data)

        return self.MessageToJson(protoData)