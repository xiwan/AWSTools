

from google.protobuf.json_format import MessageToJson, MessageToDict
from google.protobuf.json_format import ParseDict
from Core.utils import encodeLittle, encodeBig, decodeLittle, decodeBig

import progen.python.todolist_pb2 as TodoList
import progen.python.omni.base_pb2 as base_pb2
import progen.python.omni.msg_pb2 as msg_pb2

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

    def ParseDict(self, message, bin):
        ParseDict(message, bin)

    def sendPayload(self, send_data):
        bin = self.SerializeToString(send_data)
        bin_len = len(bin)
        # print(bin_len, bin)
        payload = encodeLittle(bin_len) + bin
        return payload

    def revPayload(self, recv_data):
        all_len = len(recv_data)
        if all_len < 4:
            return
        bin_len = decodeLittle(recv_data[:4])
        bin = recv_data[4:]
        # print(bin_len, bin)

        baseRsp = base_pb2.BaseRsp()
        self.ParseFromString(baseRsp, bin)
        return self.MessageToJson(baseRsp)
    
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