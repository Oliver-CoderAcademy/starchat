from threading import Thread
import socket
import threading
import os

class ClientObject(Thread):
    def __init__(self, conn, addr, server, *args, **kwargs):
        self.conn = conn
        self.addr = addr
        super.__init__(
            *args, 
            name=str(addr), 
            target=self.handle_client,
            args=(),
            kwargs={
                "conn": conn,
                "addr": addr,
                "server": server
            } 
            **kwargs
        )
        server.activities[f"talking to {addr}"]=self

    def handle_client(self, conn=None, addr=None, server=None):
        while True:
            data = str(conn.recv(1024))
            if data:
                message=data.strip("b'")
                message=message.strip("<>")
                server.chat_history.append(message)



class Server:
    def __init__(self):
        self.clients = {}
        self.chat_history = []
        self.activities = {}
        print(f"You are serving from {socket.gethostbyname(socket.gethostname())}")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            self.socket.bind(('0.0.0.0', 33333))
            self.socket.listen()
            self.activities["getting_clients"] = threading.Thread(target=self.get_clients)

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            for line in self.chat_history:
                print(line)


    def get_clients(self):
        while True:
            conn, addr = self.socket.accept()
            client = ClientObject(conn, addr, self)
            self.clients[client.name] = client


class Client:
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.conn:
            addr = input("Please enter the IP address to connect to: ")
            self.conn.connect((addr, 33333))
            print("CONNECTED!")
            while True:
                message = input("::: ")
                self.conn.sendall(message.encode('utf-8'))