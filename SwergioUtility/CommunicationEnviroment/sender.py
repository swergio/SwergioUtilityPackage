from SwergioUtility.MessageUtility.MessageInterface.messageInterface import MessageInterface

class Sender():

    def __init__(self,communication_enviroment):
        self.env = communication_enviroment

    def emit(self,CommunicationID,action, value):    
        Message = self.env.InternalMessageHandler.InternalToExternalMessage(action)

        message_type = self.env.MessageType.GetValueByName(Message.MessageType)
        nameSpace = Message.NameSpace
        
        Message.Reward = self.env.QuestionFeedback.OnOut(nameSpace,message_type,value[0])

        if self.env.Reviewer.review(Message) == True:
            self.env._socketIOClient.emit(Message,nameSpace)

    def ForwardFeedback(self,msg):
        nspace = msg.NameSpace
        for ns in self.env._socketIONamespaces:
            if ns != nspace:
                Message = MessageInterface(ns,self.env._socketIOSenderID, msg.MessageType,msg.CommunicationID,Data = msg.Data, Reward = msg.Reward, DoneFlag = msg.DoneFlag)
                self.env._socketIOClient.emit(Message,ns)
