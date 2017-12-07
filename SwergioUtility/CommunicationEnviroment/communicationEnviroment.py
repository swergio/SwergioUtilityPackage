from uuid import uuid4
import numpy as np
import os

from SwergioUtility.SocketIOClient.socketIOClient import SocketIOClient
from SwergioUtility.MessageUtility.MessageInterface.messageList import MessageList
from SwergioUtility.MessageUtility.MessageParts.Chat.chatType import ChatType
from SwergioUtility.MessageUtility.MessageParts.Chat.chatNumber import ChatNumber
from SwergioUtility.MessageUtility.MessageParts.Type.messageType import MessageType
from SwergioUtility.MessageUtility.MessageParts.Text.messageText import MessageText
from SwergioUtility.MessageUtility.MessageParts.Other.actionFlag import ActionFlag
from SwergioUtility.MessageUtility.MessageParts.Other.feedbackReward import FeedbackReward
from SwergioUtility.ExpertData.expertData import ExpertData

from SwergioUtility.CommunicationEnviroment.reviewer import Reviewer
from SwergioUtility.CommunicationEnviroment.reviewFunctions import HasValidNamespace
from SwergioUtility.CommunicationEnviroment.reciever import Reciever
from SwergioUtility.CommunicationEnviroment.internalMessageHandler import InternalMessageHandler
from SwergioUtility.CommunicationEnviroment.sender import Sender
from SwergioUtility.CommunicationEnviroment.questionFeedback import QuestionFeedback


class CommunicationEnviroment():
    def __init__(self,SocketIONamespaces = None, 
                CallbackFunction = None, 
                ReviewFunctionList = None,
                no_socketIO_client = False, 
                expertdata_file_path = None, 
                custom_settings_path = None):
       
        '''
        Set up Namespaces
        '''
        if SocketIONamespaces is None:
            agent_ns = [ns for ns in os.getenv('AGENT_NAMESPACES').split(';')] if os.getenv('AGENT_NAMESPACES') is not None else []
            worker_ns = [ns for ns in os.getenv('WORKER_NAMESPACES').split(';')] if os.getenv('WORKER_NAMESPACES') is not None else []
            knowledge_ns = [ns for ns in os.getenv('KNOWLEDGEBASE_NAMESPACES').split(';')] if os.getenv('KNOWLEDGEBASE_NAMESPACES') is not None else []
            self._socketIONamespacesDict = {'AGENT':agent_ns,'WORKER':worker_ns, 'KNOWLEDGEBASE':knowledge_ns}
        else:
            self._socketIONamespacesDict = SocketIONamespaces
      
        self._socketIONamespacesDict['REVIEW'] = ['InternReview']
        self._socketIONamespaces = [n for c  in self._socketIONamespacesDict.values() for n in c]
   
        '''
        Set internal Variables
        '''   
        self.message_callback = CallbackFunction
        self._ReviewFunctions = ReviewFunctionList
        self._socketIOSenderID = uuid4()

        self.expertdata_file_path = expertdata_file_path
        self.custom_settings_path = custom_settings_path
  
        '''
        Set socketIOClient if required
        '''  
        if no_socketIO_client is False:
            self._socketIOClient = SocketIOClient(self._socketIONamespaces)
        
        '''
        Initiate helper classes 
        ''' 
        self.Messages = MessageList()
        self.ExpertData = ExpertData(self, expertdata_file_path)

        self.ChatType = ChatType(custom_settings_path = custom_settings_path)
        self.ChatNumber = ChatNumber(custom_settings_path = custom_settings_path)
        self.MessageType = MessageType(custom_settings_path = custom_settings_path)
        self.MessageText = MessageText(expert_data = self.ExpertData, custom_settings_path = custom_settings_path)
        self.ActionFlag = ActionFlag(custom_settings_path = custom_settings_path)
        self.FeedbackReward = FeedbackReward(custom_settings_path = custom_settings_path)
       
        self.Reviewer = Reviewer(self)
        self._ReviewFunctions = [HasValidNamespace]

        self.Reciever = Reciever(self)
        self.InternalMessageHandler = InternalMessageHandler(self)
        self.Sender = Sender(self)
        self.QuestionFeedback = QuestionFeedback(self)
        
        '''
        Set external Variables
        ''' 
        self.LengthOfMessageText = self.MessageText.message_size
        
        '''
        Set the inofrmations for internal message representation
        Expected structure of List are:
        CHATTYPE, CHAT NUMBER, MESSAGE TYPE, MESSAGE TEXT, ACT FLAG
        '''
        self.message_space = [self.ChatType.message_size,self.ChatNumber.message_size,self.MessageType.message_size,self.MessageText.message_size,self.ActionFlag.message_size]
        self.vocab_space = [self.ChatType.vocab_size,self.ChatNumber.vocab_size,self.MessageType.vocab_size,self.MessageText.vocab_size,self.ActionFlag.vocab_size]
        self.action_space = [self.ChatType.action_size,self.ChatNumber.action_size,self.MessageType.action_size,self.MessageText.action_size,self.ActionFlag.action_size]
        self.embedding_space = [self.ChatType.embedding_size,self.ChatNumber.embedding_size,self.MessageType.embedding_size,self.MessageText.embedding_size,self.ActionFlag.embedding_size]

        self.emit = self.Sender.emit



    def SetCallbackFunction(self,CallbackFunction):
        self.message_callback = CallbackFunction

    def SetReviewFunctions(self,ReviewFunctionList):
        self._ReviewFunctions = ReviewFunctionList

    def ListenToSocketIO(self):

        def On_Message(data):
            self.Reciever.On_Message(data)
            
        self._socketIOHandler = [On_Message for i in range(len(self._socketIONamespaces))]
        print('Start listenning')
        self._socketIOClient.listen(self._socketIOHandler)




     
