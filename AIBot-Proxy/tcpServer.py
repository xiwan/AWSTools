import socket
import threading
import argparse
import progen.python.todolist_pb2 as TodoList
from Core.protoKlass import ProtoKlass

def example_proto(owner_id):
    my_list = TodoList.TodoList()
    my_list.owner_id = owner_id
    my_list.owner_name = "Tim"

    first_item = my_list.todos.add()
    first_item.state = TodoList.TaskState.Value("TASK_DONE")
    first_item.task = "Test ProtoBuf for Python"
    first_item.due_date = "31.10.2019"
    proto = ProtoKlass()
    return proto.SerializeToString(my_list)


def proto_handler(recv_data):
    return example_proto(77777)

def echo_handler(recv_data):
    msg = recv_data.decode("utf-8")
    send_data = msg.encode("utf-8")
    return send_data

def dispose_client_request(tcp_client_1, tcp_client_address):
    while True:
        try:
            recv_data = tcp_client_1.recv(4096)
            if len(recv_data) == 0:
                print("%s client closed ..." % tcp_client_address[1])
                break

            # send_data = echo_handler(recv_data)

            send_data = proto_handler(recv_data)
            print("send_data:", send_data)
            tcp_client_1.send(send_data)

        except Exception as e:
            print(e)
            break

    tcp_client_1.close()
    pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='tcp server command-line options')
    parser.add_argument('--host', type=str, help='host address: 0.0.0.0 or localhost', default='localhost')
    parser.add_argument('--port', type=int, help='host port number: 5000', default='8000')
    args = parser.parse_args()

    tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    tcp_server.bind((args.host, args.port))
    tcp_server.listen(128)

    while True:
        tcp_client_1 , tcp_client_address = tcp_server.accept()
        print("client address:", tcp_client_address)
        thd = threading.Thread(target = dispose_client_request, args = (tcp_client_1,tcp_client_address))

        #thd.setDaemon(True)

        thd.start()
        pass

    tcp_server.close()