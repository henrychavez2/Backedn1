import socket
import os

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    
    while True:
        command = input("cliente> ")
        client.send(command.encode('utf-8'))

        if command == "lsFiles":
            response = client.recv(4096).decode('utf-8')
            print(response)
        
        elif command.startswith("get"):
            filename = command.split(" ")[1]
            os.makedirs("download", exist_ok=True)
            filepath = os.path.join("download", filename)
            
            # Recibir el archivo
            data = client.recv(4096)
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"Archivo '{filename}' descargado en 'download/'.")
        
        else:
            response = client.recv(4096).decode('utf-8')
            print(response)

if __name__ == "__main__":
    main()
