import socket
import os

def handle_client(client_socket):
    while True:
        command = client_socket.recv(1024).decode('utf-8').strip()
        if not command:
            break
        
        if command == "lsFiles":
            try:
                files = os.listdir("Files")
                response = "\n".join(files)
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                client_socket.send(f"Error: {str(e)}".encode('utf-8'))
        
        elif command.startswith("get "):
            filename = command.split(" ")[1]
            try:
                filepath = os.path.join("Files", filename)
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        data = f.read()
                    client_socket.send(data)
                else:
                    client_socket.send(f"Error: El archivo '{filename}' no existe.".encode('utf-8'))
            except Exception as e:
                client_socket.send(f"Error: {str(e)}".encode('utf-8'))
        
        else:
            client_socket.send(b"Comando no reconocido.")
    
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Esperando conexiones...")

    while True:
        client_sock, addr = server.accept()
        print(f"Conexión aceptada de {addr}")
        handle_client(client_sock)

if __name__ == "__main__":
    main()
