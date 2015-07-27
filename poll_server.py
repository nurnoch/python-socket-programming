import select
import socket
import sys
import Queue

# create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('localhost', 8888))
server.listen(5)

# queuses for message to send
message_queues = {}

# eventmask is an optional bitmask describing the type of events you want to
# check for
READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT

# Returns a polling object, which supports registering and unregistering file
# descriptors, and then polling them for I/O events
poller = select.poll()

# Register a file descriptor with the polling object
poller.register(server, READ_ONLY)

# map file desriptor to socket
fd_to_socket = {server.fileno(): server, }

# timeout pass to poll(), ms
TIMEOUT = 1000

# in the loop calls poll() and process returned events
while True:
    # wait for at least one socket be ready
    print "waiting for the next event"
    events = poller.poll(TIMEOUT)

    for fd, flag in events:
        # retrieve socket from fd
        s = fd_to_socket[fd]
        # handle read
        if flag & (select.POLLIN | select.POLLPRI):
            if s is server:
                # a readable server is ready to accept a connection
                conn, addr = s.accept()
                print "new connection from {addr}".format(addr = addr)
                conn.setblocking(0)
                fd_to_socket[conn.fileno()] = conn
                poller.register(conn, READ_ONLY)

                # give the connection a queue for sending messages
                message_queues[conn] = Queue.Queue()
        # otherwise receive data waiting to be read
            else:
                request_data = s.recv(1024)
                if request_data:
                    print "received {data} from {addr}".format(data = request_data, addr = s.getpeername())
                    message_queues[s].put(request_data)
                    # add to writable for response
                    poller.modify(s, READ_WRITE)
                # get empty data means to close the connection
                else:
                    print "closing {addr} after reading no data".format(addr = s.getpeername())
                    # stop listening for readable
                    poller.unregister(s)
                    s.close()
                    del message_queues[s]
        # a client hang up the connection
        elif flag & select.POLLHUP:
            print "closing {addr} after receiving HUP".format(addr = s.getpeername())
            # stop listening for readable
            poller.unregister(s)
            s.close()
            del message_queues[s]
        # any event with POLLERR cause to close the socket
        elif flag & select.POLLERR:
            print "handling exception for {addr}".format(addr = s.getpeername())
            poller.unregister(s)
            s.close()
            del message_queues[s]






