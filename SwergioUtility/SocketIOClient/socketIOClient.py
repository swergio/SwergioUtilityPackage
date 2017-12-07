from socketIO_client import SocketIO, BaseNamespace
from SwergioUtility.MessageUtility.MessageInterface.messageInterface import MessageInterface
from uuid import uuid4
import os

class SocketIOClient():

    _namespaces = []

    def __init__ (self, NameSpaces):
        self.MessageSenderID = uuid4()
        #get the socketIOserver and PORT from enviroment variable!!!
        server =  os.getenv('SOCKETIOSERVER_NAME')
        port = os.getenv('SOCKETIOSERVER_PORT')
        
        self.SocketIO  = SocketIO(server, port)
      
        for name in NameSpaces:
           self._namespaces.append({'Name':name,'Class':self.SocketIO.define(BaseNamespace,'/' + name)})

    #listen to all Namespaces. List of handler function needs to be in same  order as prior NameSpace names
    def listen(self, handlerList):
        self._handlerList = handlerList
        for name in [x for x in self._namespaces]:
            self.listenToNameSpace(name['Name'],handlerList[self._namespaces.index(name)])
        self.SocketIO.wait()
        

    def listenToNameSpace(self,NameSpaceName,handler, event = 'mymessage'):
        #get NameSpaceClass
        NameSpaceClass = [x['Class'] for x in self._namespaces if x['Name'] == NameSpaceName][0]
        NameSpaceClass.on(event, handler)

    def stoplistening(self, NameSpaceName = None, event = 'mymessage'):
        if NameSpaceName is None:
            NameSpacesClasses = [x['Class'] for x in self._namespaces]
        else:
            NameSpacesClasses = [x['Class'] for x in self._namespaces if x['Name'] == NameSpaceName]

        for NameSpaceClass in NameSpacesClasses:
            NameSpaceClass.off(event) 

    def emit(self,Message, NameSpaceName, event='mymessage'):
        NameSpaceClass = [x['Class'] for x in self._namespaces if x['Name'] == NameSpaceName][0]
        NameSpaceClass.emit(event,Message.to_document())


        