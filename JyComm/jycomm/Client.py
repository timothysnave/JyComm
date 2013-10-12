''' 
The following is a list of commands that may be sent through
the sockets obtained from the server or client. Note that
some may not be implemented yet.

0 - Ping (essentially). Response will be 0. If there is
  - no response, the client should be assumed dead and
  - removed from the clientlist.
  - On second thought, this may be unnecessary. The socket
  - should go dead completely, if the client disconnects.
  - No arguments.
  
1 - Handle (Screen name) request. Response will be a byte
  - array which can be converted into a string (in Java).
  - No arguments.
  
2 - Chat request. Open a chat window for the client
  
3 - Broadcast Chat message. This essentially sends a message
  - to a 'chat room' of every client that can be found.
  - Arguments:
  - 0: byte[] containing the message

 '''

from javax.swing import *
from java.awt import BorderLayout
import socketComm, thread

class Client(object):

    def __init__(self, socket, handle):
        self.socket = socket
        self.sockIn = socketComm.Server.getDataInputStream(socket)
        self.sockOut = socketComm.Server.getDataOutputStream(socket)
        self.isChatting = False
        self.handle = handle
        
        # Get screen name
        self.sockOut.writeInt(1)
        hb = self.sockIn.readBytes()
        self.screenName = socketComm.Client.parseBytes(hb)
        
        '''
        - Monitor the input in a new thread, and handle the input appropriately
        - Thread closes only if client logs off
        - ChatBox opens in the client's thread, not in main thread
        - Thread handles ALL interactions with clients
        '''
        thread.start_new_thread(self.monitor, (self.handle, self))
    
    def connect(self):
        self.window = ChatBox(self.screenName, self) # fix this
        return self.window
        
    def monitor(self, handle, client):
        chatWindow = False
        channelIn = client.sockIn
        channelOut = client.sockOut
        while(True):
            x = channelIn.readInt()
            if (x==0):
                channelOut.writeInt(0)
                channelOut.flush()
            if (x==1):
                channelOut.write(socketComm.Client.getBytes(handle))
                channelOut.flush()
            if (x==2):
                handleTextIn()
            if (x==3):
                handleTextIn()
        
        def handleTextIn():
            text = channelIn.read()
            text = socketComm.Client.parseBytes(text)
            if (not client.isChatting):
                chatWindow = client.connect()
            chatWindow.receive(text)
        
    def __repr__(self):
        return self.screenName
    
    def __eval__(self):
        return self.screenName
    
class ChatBox(object):
    
    def __init__(self, client, localHandle):
        self.client = client
        self.localHandle = localHandle
        
        window = JFrame(repr(client))
        window.setSize(450, 350)
        
        topPanel = JPanel()
        self.conversationBox = JTextArea(18,40)
        self.conversationBox.setAutoscrolls(JTextArea.HEIGHT); #Questionable
        self.conversationBox.setEditable(False);
        topPanel.add(self.conversationBox)
        
        bottomPanel = JPanel()
        self.textField = JTextField(30)
        bottomPanel.add(self.textField, BorderLayout.WEST)
        self.sendButton = JButton("Send", actionPerformed=self.send);
        bottomPanel.add(self.sendButton, BorderLayout.EAST)
        
        window.add(topPanel, BorderLayout.CENTER)
        window.add(bottomPanel, BorderLayout.SOUTH)

        window.setVisible(True)
        
    def send(self, event):
        # TODO:
        text = self.textField.getText()
        byteArray = socketComm.Client.getBytes(text)
        self.client.sockOut.sendBytes(byteArray)
        ctext = self.conversationBox.getText()
        ctext += self.localHandle + ": " + text + "\n"
        self.conversationBox.setText(ctext)
        self.textField.setText("")

    def receive(self, text):
        ctext = self.textField.getText()
        ctext += repr(self.client) + ": " + text + "\n"
        self.textField.setText(ctext)


