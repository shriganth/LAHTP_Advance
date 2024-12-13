from subprocess import Popen, STDOUT, PIPE
from threading import Thread
from time import clock_settime

class ProcessOutputThread(Thread):
    def __init__(self, proc):
        Thread.__init__(self)
        self.proc = proc

    def run(self):
        while not self.proc.stdout.closed:
            print(p.stdout.readline().decode().rstrip())

p = Popen(['bc', '-i'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
output = ProcessOutputThread(p)
output.start()

while p.poll() is None:
    print("Process id: " + str(p.pid))
    query = input()
    if query == 'quit' or query == 'exit':
        p.communicate(query.encode(), timeout=1)
        if p.poll() is not None:
            break
    query = query + '\n'
    p.stdin.write(query.encode())
    p.stdin.flush()



