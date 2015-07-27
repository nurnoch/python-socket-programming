import socket
import select

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s1.connect(('localhost', 8888))
s2.connect(('localhost', 8888))

s1.sendall("Hello, server!")
s2.sendall("Hello, server!")

while True:
    # wait a read event
    rlist, wlist, elist = select.select([s1, s2], [], [], 5)
    # test for timeout
    if [rlist, wlist, elist] == [[], [], []]:
        print "Five seconds elapsed.\n"
    else:
        # loop through each socket in rlist, and print data
        for sock in rlist:
            print sock.recv(1024)
            sock.close()
