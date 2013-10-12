# from javax.swing import *
# from types import *
from Client import Client, ChatBox
from ClientList import ClientList
import socketComm, thread, threading, Client
from java.io import DataInputStream, DataOutputStream

'''
NEXT STEP:

Create a monitor method in the clientlist to constantly
watch for incoming requests on all open sockets. 
'''


# Use a popup window to get this, in the final version:
handle = "timothysnave"

# Open client list window, insert handle
x = ClientList(handle)

# Get an ArrayList<Socket> from Java:
sQ1 = socketComm.Server.getNewSocketList()
sQ2 = socketComm.Server.getNewSocketList()

#!!! Make sure server & client have local and remote codes reversed !!!#
server = socketComm.Server(1113, 1, 1, sQ1)
t1 = thread.start_new_thread(server.start,());

# Server is now running. Get Client going.
client = socketComm.Client(1113, 1, 1, sQ2)
thread.start_new_thread(client.scan, ())

# Add clients found by 'client' thread to chat window
t1.join()
for s in sQ1:
    x.add(Client(s, handle))

# Watch the server queue, add the things that come into it to the clientlist
def serverMonitor(sQ, cL):
    while True:
        if not sQ.isEmpty():
            x.add(Client(sQ.remove(), handle))
            
thread.start_new_thread(serverMonitor, (sQ2, x))



