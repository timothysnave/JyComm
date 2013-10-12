from javax.swing import *
from Client import Client, ChatBox
import socketComm

class ClientList(object):

    def __init__(self, handle):
        self.handle = handle
        window = JFrame("JyComm")
        window.setSize(200, 400)
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        
        menuBar = JMenuBar()
        fileMenu = JMenu("File")
        menuBar.add(fileMenu)
        window.setJMenuBar(menuBar)
        
        self.clientList = JList(mouseClicked=self.mouseClicked)
        self.clientList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        self.clientList.setLayoutOrientation(JList.VERTICAL)
        self.clientList.setVisibleRowCount(-1)
        self.cL = DefaultListModel()
        self.clientList.setModel(self.cL)
        window.add(self.clientList)
        
        window.setVisible(True)
                
    def add(self, client):
        self.cL.addElement(client)
        
    def remove(self, element):
        if (self.cL.contains(element)):
            self.cL.remove(element)
            
    def mouseClicked(self, event):
        if (event.getClickCount()==2):
            self.clientList.getSelectedValue().connect()
            

            
            
            
            
            
            
            
            