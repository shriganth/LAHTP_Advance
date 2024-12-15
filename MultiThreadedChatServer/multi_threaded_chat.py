import socket
import time
from threading import Thread
from time import sleep


class ChatBotThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.threads = []
        self.messages = []

    def addChatThread(self, thread):
        self.threads.append(thread)
        # print(self.threads)

    def removeChatThread(self, thread):
        print("removeChat thread")
        print("Before remove the thread: {}".format(thread))
        if thread in self.threads:
            self.threads.remove(thread)
        print("After remove the thread: {}".format(self.threads))

    def queueMessages(self, user, message):
        data = (user, message)
        self.messages.append(data)
        print("[queue message] {}: {}".format(user, message))
        # print("[threads]: {}".format(self.threads))
        print("[message length]: {}".format(len(message)))
        self.run()

    def run(self):
        while True:
            time.sleep(0.025)
            if len(self.messages) > 0:
                for thread in self.threads:
                    for message in self.messages:
                        user = message[0]
                        msg = message[1]
                        if thread.getUsername() != user:
                            thread.sendMessage(msg)

class ChatServerOutgoingThread(Thread):
    def __init__(self, incoming_thread):
        Thread.__init__(self)
        self.incoming_thread = incoming_thread
        self.messages = []
        self.canKill = False

    def sendMessage(self, user, message):
        fMessage = "{username}: {message}".format(username=user, message=message)
        try:
            # print(fMessage.encode())
            con = self.incoming_thread.getConnection()
            con.sendall(fMessage.encode())
            con.flush()
        except:
            bot.removeChatThread(self.incoming_thread)
            self.killThread()

    def queueMessage(self, user, message):
        data = (user, message)
        self.messages.append(data)

    def killThread(self):
        self.canKill = True

    def run(self):
        while True:
            sleep(0.1)
            if self.canKill:
                break
            if len(self.messages) > 0:
                for message in self.messages:
                    try:
                        print("[send message] {}: {}".format(message[0], message[1]))
                        self.sendMessage(message[0], message[1])
                    except:
                        break


class ChatServerIncomingThread(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.username = ""
        self.user_ip = addr[0]
        self.user_port = addr[1]
        self.outgoing_thread = None
        self.can_kill = False

    def setUsername(self, username):
        self.username = username

    def getUsername(self):
        return self.username

    def getConnection(self):
        return self.conn

    def isClosed(self):
        return self.conn.close()

    def initSendMessageThread(self):
        self.outgoing_thread = ChatServerOutgoingThread(self)
        self.outgoing_thread.start()

    def sendMessage(self, message):
        self.outgoing_thread.queueMessage(self.getUsername(), message)

    def broadcastMessage(self, message):
        print("broadcastMessage Section")
        self.outgoing_thread.queueMessage("Server Bot", message)

    def killThread(self):
        bot.removeChatThread(self)
        self.can_kill = True

    def run(self):
        self.initSendMessageThread()
        self.broadcastMessage("Welcome to LAHTP Group Chat Server...\n")
        self.broadcastMessage("You are connected from {}: {}\n".format(self.user_ip, self.user_port))
        self.broadcastMessage("Please enter your name to continue: ")
        data = self.conn.recv(1024)
        print("Data: {}".format(data.strip()))
        if not data:
            self.outgoing_thread.killThread()
            self.killThread()
            return
        else:
            self.setUsername(data.decode().strip())
            print("User connected with server: {}".format(self.username))
            self.initSendMessageThread()
            self.broadcastMessage("You can now chat with our group...\n\n> ")

        while not self.conn._closed:
            data = self.conn.recv(1024)
            if not data:
                self.outgoing_thread.killThread()
                self.killThread()
                break
            if data.decode().strip() == "kill":
                self.killThread()
            # message = data.decode().strip()
            # print(f"Received message from {self.getUsername()}: {message}")
            # if message == "kill":
            #     self.killThread()
            else:
                # print("{name}: {message}".format(name=self.username, message=data.decode()))
                bot.queueMessages(self.getUsername(), data.decode().strip())

HOST = ""
PORT = 9987

bot = ChatBotThread()
bot.start()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
sock.bind((HOST, PORT))
sock.listen()
print("Server listening on {}: {}".format(HOST, PORT))

while not sock._closed:
    conn, addr = sock.accept()
    print("conn: {} \n addr: {}".format(conn, addr))
    t = ChatServerIncomingThread(conn, addr)
    t.start()
    bot.addChatThread(t)

if not sock._closed:
    sock.close()