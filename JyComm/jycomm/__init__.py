from Client import Client, ChatBox
from ClientList import ClientList
import socketComm, thread, threading, Client
from threading import Thread
from java.io import DataInputStream, DataOutputStream


# Use a popup window to get this, in the final version:
handle = "timothysnave"

# Open client list window, insert handle
x = ClientList(handle)

# Get an ArrayList<Socket> from Java:
sQ1 = socketComm.Server.getNewSocketList()
sQ2 = socketComm.Server.getNewSocketList()

#!!! Make sure server & client have local and remote codes reversed !!!#
server = socketComm.Server(1113, 1, 1, sQ1)
thread.start_new_thread(server.start,());

# Server is now running. Get Client going.
client = socketComm.Client(1113, 1, 1, sQ2)
class ClientScanner(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        
    def run(self):
        self.client.scan()
        
t1 = ClientScanner(client)
t1.start()

# Add clients found by 'client' thread to chat window
t1.join()
for s in sQ1:
    x.add(Client(s, handle))

# Watch the server queue, add the things that come into it to the clientlist
def run(self):
    while True:
        if not self.sQ.isEmpty():
            x.add(Client(self.sQ.remove(), handle))



