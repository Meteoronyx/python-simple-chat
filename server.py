import socket
import threading

client_connections = []

def handle_client(client_socket, client_address):
    print(f"[INFO] Connection from {client_address} has been established.")
    nickname = client_socket.recv(1024).decode('utf-8')
    client_connections.append((client_socket, nickname))
    print(f"[INFO] Nickname set to {nickname}")
    broadcast(f"{nickname} has joined the chat!", client_socket)

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[{nickname}] {message}")
            broadcast(f"{nickname}: {message}", client_socket)
    finally:
        client_connections.remove((client_socket, nickname))
        client_socket.close()
        print(f"[INFO] Connection from {client_address} has been closed.")
        broadcast(f"{nickname} has left the chat.", client_socket)

def broadcast(message, current_socket):
    for client_socket, _ in client_connections:
        if client_socket != current_socket:
            try:
                client_socket.send(message.encode('utf-8'))
            except:
                client_socket.close()
                client_connections.remove(client_socket)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("[INFO] Server is listening on port 12345.")
    
    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()