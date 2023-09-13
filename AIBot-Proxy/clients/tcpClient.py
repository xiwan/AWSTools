import socket
# 1.创建socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 链接服务器
server_addr = ("34.229.191.120", 7788)
tcp_socket.connect(server_addr)

# 3. 发送数据
send_data = input("请输入要发送的数据：")
tcp_socket.send(send_data.encode("gbk"))

# 4. 关闭套接字
tcp_socket.close()