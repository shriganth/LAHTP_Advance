import socket
import sys
import threading
import curses

# List of all connected clients
clients = []
# Lock for thread-safe operations on the clients list
clients_lock = threading.Lock()

# Function to handle client messages
def handle_client(client_socket, client_address):
    client_socket.send("Welcome to the group chat! Please enter your username: ".encode())
    username = client_socket.recv(1024).decode().strip()
    
    with clients_lock:
        clients.append((client_socket, username))
    print(f"New connection from {client_address} with username {username}")
    
    broadcast(f"{username} has joined the group chat!", client_socket)
    
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message.lower() == 'exit':
                break
            broadcast(f"{username}: {message}", client_socket)
    except:
        print(f"Connection with {username} lost.")
    finally:
        with clients_lock:
            clients.remove((client_socket, username))
        client_socket.close()
        broadcast(f"{username} has left the group chat.", client_socket)

# Function to broadcast messages to all clients except the sender
def broadcast(message, sender_socket):
    with clients_lock:
        for client_socket, _ in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode())
                except:
                    continue

# Function to start the server
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Function to handle the curses UI for the client
def client_ui(client_socket, stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    height, width = stdscr.getmaxyx()
    message_win = curses.newwin(height - 3, width, 0, 0)
    input_win = curses.newwin(3, width, height - 3, 0)
    input_win.border(0)
    
    username = ""
    input_win.addstr(1, 1, "Enter your username: ")
    input_win.refresh()
    curses.echo()
    username = input_win.getstr(1, 22).decode().strip()
    curses.noecho()
    
    client_socket.send(username.encode())
    
    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    message_win.addstr(f"{message}\n")
                    message_win.refresh()
            except:
                break

    threading.Thread(target=receive_messages, daemon=True).start()

    while True:
        input_win.clear()
        input_win.border(0)
        input_win.addstr(1, 1, f"{username}: ")
        input_win.refresh()
        curses.echo()
        message = input_win.getstr(1, len(username) + 3).decode().strip()
        curses.noecho()
        
        if message.lower() == "exit":
            client_socket.send(message.encode())
            break
        client_socket.send(message.encode())

    client_socket.close()

# Function to start the client
def start_client():
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    curses.wrapper(client_ui, client_socket)

if __name__ == "__main__":
    mode = input("Enter 'server' to start server or 'client' to start client: ").strip().lower()

    if mode == 'server':
        HOST = "0.0.0.0"
        PORT = int(sys.argv[2])
        start_server(HOST, PORT)
    elif mode == 'client':
        start_client()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")
import socket
import sys
import threading
import curses

# List of all connected clients
clients = []
# Lock for thread-safe operations on the clients list
clients_lock = threading.Lock()

# Function to handle client messages
def handle_client(client_socket, client_address):
    client_socket.send("Welcome to the group chat! Please enter your username: ".encode())
    username = client_socket.recv(1024).decode().strip()
    
    with clients_lock:
        clients.append((client_socket, username))
    print(f"New connection from {client_address} with username {username}")
    
    broadcast(f"{username} has joined the group chat!", client_socket)
    
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message.lower() == 'exit':
                break
            broadcast(f"{username}: {message}", client_socket)
    except:
        print(f"Connection with {username} lost.")
    finally:
        with clients_lock:
            clients.remove((client_socket, username))
        client_socket.close()
        broadcast(f"{username} has left the group chat.", client_socket)

# Function to broadcast messages to all clients except the sender
def broadcast(message, sender_socket):
    with clients_lock:
        for client_socket, _ in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode())
                except:
                    continue

# Function to start the server
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Function to handle the curses UI for the client
def client_ui(client_socket, stdscr):
    curses.curs_set(0)
    stdscr.clear()
    
    height, width = stdscr.getmaxyx()
    message_win = curses.newwin(height - 3, width, 0, 0)
    input_win = curses.newwin(3, width, height - 3, 0)
    input_win.border(0)
    
    username = ""
    input_win.addstr(1, 1, "Enter your username: ")
    input_win.refresh()
    curses.echo()
    username = input_win.getstr(1, 22).decode().strip()
    curses.noecho()
    
    client_socket.send(username.encode())
    
    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    message_win.addstr(f"{message}\n")
                    message_win.refresh()
            except:
                break

    threading.Thread(target=receive_messages, daemon=True).start()

    while True:
        input_win.clear()
        input_win.border(0)
        input_win.addstr(1, 1, f"{username}: ")
        input_win.refresh()
        curses.echo()
        message = input_win.getstr(1, len(username) + 3).decode().strip()
        curses.noecho()
        
        if message.lower() == "exit":
            client_socket.send(message.encode())
            break
        client_socket.send(message.encode())

    client_socket.close()

# Function to start the client
def start_client():
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    curses.wrapper(client_ui, client_socket)

if __name__ == "__main__":
    mode = input("Enter 'server' to start server or 'client' to start client: ").strip().lower()

    if mode == 'server':
        HOST = "0.0.0.0"
        PORT = int(sys.argv[2])
        start_server(HOST, PORT)
    elif mode == 'client':
        start_client()
    else:
        print("Invalid mode. Please enter 'server' or 'client'.")
