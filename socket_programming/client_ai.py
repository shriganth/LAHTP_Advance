import socket
import sys
import select

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 7770
RECEIVE_BUFF = 4096

def chat_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)

    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
    except Exception as e:
        print(f"Unable to connect to {SERVER_HOST}:{SERVER_PORT}: {e}")
        sys.exit()

    print(f"Connected to remote server at {SERVER_HOST}:{SERVER_PORT}.")
    name = input("Enter your name : ")
    print("Type your messages below (type 'exit' to quit).")

    while True:
        sockets_list = [sys.stdin, client_socket]
        ready_to_read, _, _ = select.select(sockets_list, [], [])

        for sock in ready_to_read:
            # print("sock : {}" .format(sock))
            # print("client_socket : {}" .format(client_socket))
            # data = sock.recv(RECEIVE_BUFF)
            if sock == client_socket:
            # if data:
                # Incoming message from server
                # print("shriganth")
                data = sock.recv(RECEIVE_BUFF)
                print(f"\n{data.decode('utf-8')}")
                if not data:
                    print("Disconnected from server.")
                    sys.exit()
                else:
                    # print("shriganth")
                    # print(f"\n{data.decode('utf-8')}")
                    sys.stdout.write("> ")
                    sys.stdout.flush()
            else:
                # User entered a message
                message = sys.stdin.readline().strip()
                if message.lower() == 'exit':
                    print("Exiting chat...")
                    client_socket.close()
                    sys.exit()
                client_socket.send(message.encode('utf-8'))
                sys.stdout.write("> ")
                sys.stdout.flush()


if __name__ == "__main__":
    chat_client()
