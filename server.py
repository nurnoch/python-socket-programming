import socket
import threading

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 1024

def handle_request(sock, addr):
    print "Accept new connection from {addr}".format(addr = addr)
    request_data = sock.recv(1024)
    print request_data.decode()
    http_response = "Hello, world!"
    # send response data to the socket
    sock.sendall(http_response)
    sock.close()

def serve_forever():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse socket immediately
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(REQUEST_QUEUE_SIZE)
    print 'Serving HTTP on port {port} ...'.format(port = PORT)

    while True:
        try:
            client_connection, client_address = server_socket.accept()
        except IOError as e:
            code, msg = e.args
            # restart 'accept' if it was interrupted
            if code == errno.EINTR:
                continue
            else:
                raise
        # create a thread to handle this request
        t = threading.Thread(target=handle_request, args=(client_connection, client_address))
        t.start()

if __name__ == '__main__':
    serve_forever()
