import socket 
import asyncio
import platform

FPS = 60
MAX_CLIENT_CONNECTION = 5

async def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode('utf-8')

        if not data:
            break
        print(f"Recieved: {data}")
        client_socket.send(f"Echo: {data}".encode('utf-8'))

    client_socket.close()

async def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.7.1', 5000))
    server.listen(MAX_CLIENT_CONNECTION)
    print("Server listing on 192.168.7.1:5000 ... ")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        await handle_client(client_socket)
        await asyncio.sleep(1.0/FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())

else:
    if __name__ == "__main__":
        asyncio.run(main())
