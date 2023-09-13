

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

    def RevHandler(self, recv_data):
        protoData = TodoList.TodoList()

        self.ParseFromString(protoData, recv_data)

        return self.MessageToJson(protoData)
    
    def SendHandler(self, send_data):

        my_list = TodoList.TodoList()
        my_list.owner_id = 77777
        my_list.owner_name = "Benxiwan"

        first_item = my_list.todos.add()
        first_item.state = TodoList.TaskState.Value("TASK_DONE")
        first_item.task = f"Test ProtoBuf: {send_data}"
        first_item.due_date = "31.10.2019"

        return self.SerializeToString(my_list)