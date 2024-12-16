import socket
import time
from threading import Thread, Lock
import curses
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])

def main(stdscr):
    stdscr.clear()
    stdscr.addstr("Starting server...\n")
    stdscr.refresh()

    class ChatBotThread(Thread):
        def __init__(self):
            super().__init__()
            self.threads = []
            self.messages = []
            self.running = True
            self.lock = Lock()

        def addChatThread(self, thread):
            with self.lock:
                self.threads.append(thread)

        def removeChatThread(self, thread):
            with self.lock:
                if thread in self.threads:
                    self.threads.remove(thread)

        def queueMessages(self, user, message):
            with self.lock:
                self.messages.append((user, message))

        def broadcast(self):
            with self.lock:
                for thread in self.threads:
                    for user, msg in self.messages:
                        if thread.getUsername() != user:
                            thread.sendMessage(msg)
                self.messages.clear()

        def run(self):
            while self.running:
                time.sleep(0.05)
                if self.messages:
                    self.broadcast()

        def stop(self):
            self.running = False

    class ChatServerIncomingThread(Thread):
        def __init__(self, conn, addr):
            super().__init__()
            self.conn = conn
            self.addr = addr
            self.username = ""
            self.running = True

        def getUsername(self):
            return self.username

        def setUsername(self, username):
            self.username = username

        def sendMessage(self, message):
            try:
                self.conn.sendall(message.encode())
            except Exception as e:
                stdscr.addstr(f"Error sending message: {e}\n")
                self.running = False

        def run(self):
            try:
                self.sendMessage("Welcome! Please enter your username: ")
                username = self.conn.recv(1024).decode().strip()
                self.setUsername(username)
                bot.queueMessages("Server", f"{username} has joined the chat!")
                while self.running:
                    data = self.conn.recv(1024)
                    if not data:
                        break
                    message = data.decode().strip()
                    if message.lower() == "quit":
                        bot.queueMessages("Server", f"{self.username} has left the chat.")
                        break
                    bot.queueMessages(self.username, message)
            except Exception as e:
                stdscr.addstr(f"Connection error: {e}\n")
            finally:
                bot.removeChatThread(self)
                self.conn.close()

    bot = ChatBotThread()
    bot.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen()

    stdscr.addstr(f"Server listening on {HOST}:{PORT}\n")
    stdscr.refresh()

    try:
        while True:
            conn, addr = sock.accept()
            stdscr.addstr(f"Connection from {addr}\n")
            stdscr.refresh()
            client_thread = ChatServerIncomingThread(conn, addr)
            client_thread.start()
            bot.addChatThread(client_thread)
    except KeyboardInterrupt:
        stdscr.addstr("\nShutting down server...\n")
        stdscr.refresh()
    finally:
        bot.stop()
        sock.close()


if __name__ == "__main__":
    curses.wrapper(main)
