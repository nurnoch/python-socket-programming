import socket
import select
import sys
import Queue

# create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('localhost', 8888))
server.listen(5)

# socketss ready for reading
rlist = [server]
# sockets ready for writing
wlist = []
# exception
elist =[]

# each connection needs a queue to act as a buffer for the data to be sent
# through it
message_queues = {}

# main loop
while rlist:
    # wait for at least one socket is ready
    print "waiting for the next event"
    readable, writable, exceptional = select.select(rlist, wlist, elist)

    # handle readable lists
    for sock in readable:
        # server socket: ready to accept another connection
        if sock == server:
            conn, addr = sock.accept()
            print "new connection from {addr}".format(addr = addr)
            conn.setblocking(0)
            # add new connection to rlist
            rlist.append(conn)

            # give the connection a queue for data to send
            message_queues[conn] = Queue.Queue()
        # established connection from client
        else:
            request_data = sock.recv(1024)
            if request_data:
                print  "received {data} from {addr}".format(
                    data = request_data, addr = sock.getpeername())
                message_queues[sock].put(request_data)
                # add to response
                if sock not in wlist:
                    wlist.append(sock)
            # without data should be closed
            else:
                print "closing {addr} after no reading data".format(addr = sock.getpeername())
                if sock in wlist:
                    wlist.remove(sock)
                rlist.remove(sock)
                sock.close()
                del message_queues[sock]

    # handle writable lists
    for sock in writable:
        try:
            next_msg = message_queues[sock].get_nowait()
        except Queue.Empty:
            # no message to send
            print "output queue for {addr} is empty".format(addr = sock.getpeername())
            wlist.remove(sock)
        else:
            print "sending {msg} to {addr}".format(msg = next_msg, addr = sock.getpeername())
            sock.send(next_msg)

    # handle exceptional lists
    for sock in exceptional:
        print "handling exeptional condition for", sock.getpeername()
        rlist.remove(sock)
        if sock in wlist:
            wlist.remove(sock)
        sock.close()
        del message_queues[sock]

