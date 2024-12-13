import socket as s
import select as sel
import sys

HOST = ''
PORT = 7770
SOCKET_LIST = []
RECEIVE_BUFF = 4096


def chat_server():
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    SOCKET_LIST.append(server_socket)

    print(f"Chat server started on PORT {PORT}...")

    try:
        while True:
            ready_read, _, _ = sel.select(SOCKET_LIST, [], [], 0)

            for sock in ready_read:
                if sock == server_socket:
                    # New connection
                    client_socket, addr = server_socket.accept()
                    SOCKET_LIST.append(client_socket)
                    print(f"Client {addr[0]}:{addr[1]} connected.")
                    broadcast(server_socket, client_socket, f"{addr[0]}:{addr[1]} entered the chat.\n")
                else:
                    # Incoming message from a client
                    try:
                        data = sock.recv(RECEIVE_BUFF)
                        if data:
                            message = data.decode('utf-8')
                            broadcast(server_socket, sock, f"[{sock.getpeername()}] {message}")
                        elif not data:
                            # Disconnected client
                            if sock in SOCKET_LIST:
                                SOCKET_LIST.remove(sock)
                            broadcast(server_socket, sock, f"{sock.getpeername()} has left the chat.\n")
                            print(f"Client {sock.getpeername()} disconnected.")
                        else:
                            info = sys.stdin.readline().strip()
                            if info.lower() == 'exit':
                                print("Exiting chat...")
                                server_socket.close()
                                sys.exit()
                            broadcast(server_socket, sock, f"[{sock.getpeername()}] {info}")

                    except Exception as e:
                        print(f"Error with client {sock.getpeername()}: {e}")
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        continue
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        for sock in SOCKET_LIST:
            sock.close()


def broadcast(server_socket, client_socket, message):
    """Send a message to all clients except the sender and server socket."""
    print(f"Broadcasting: {message.strip()}")
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != client_socket:
            try:
                socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending to client {socket.getpeername()}: {e}")
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


if __name__ == "__main__":
    chat_server()
