import socket
import sys

# create 2 sockets for clients
clients = [socket.socket(socket.AF_INET, socket.SOCK_STREAM),
           socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           ]
# tow messages to send
messages = ["Hello, server.", "This is my message"]

# connect to the server
server_address = ('localhost', 8888)
print "connecting to {addr}".format(addr = server_address)
for sock in clients:
    sock.connect(server_address)

# send one piece of messages once
for msg in messages:
    # send message to the server
    for sock in clients:
        print "{addr} : sending {msg}".format(addr = sock.getpeername(), msg = msg)
        sock.send(msg)
    # read response from the server
    for sock in clients:
        response_data = sock.recv(1024)
        print "{addr} : received {data}".format(addr = sock.getpeername(), data = response_data)
        if not response_data:
            print "closing socket {addr}".format(addr = sock.getpeername())
            sock.close()






