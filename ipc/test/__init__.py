import socket


addr = ('localhost', 18900) 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(addr)
sock.listen(1)
conn, client_addr = sock.accept()
