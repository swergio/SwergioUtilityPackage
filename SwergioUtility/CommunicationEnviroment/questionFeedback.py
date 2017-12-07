from SwergioUtility.MessageUtility.MessageInterface.messageInterface import MessageInterface

class QuestionFeedback():

    def __init__(self,communication_enviroment):
        self.env = communication_enviroment
        self.QuestionOut = {}
        self.QuestionIn = {}

    def OnIn(self,CommunicationID,namespace,message_type, value):
        if message_type  == self.env.MessageType.values.QUESTION:
            self.QuestionIn[namespace] = value
        if message_type  == self.env.MessageType.values.ANSWER:
            old_value = self.QuestionOut.pop(namespace,None)
            if old_value is not None:
                reward = value - old_value
                #emit feedback
                Message = MessageInterface(namespace,self.env._socketIOSenderID, self.env.MessageType.values.FEEDBACK.name,CommunicationID,Data = 'My Feedback', Reward = float(reward))
                self.env._socketIOClient.emit(Message,namespace)


    def OnOut(self,namespace,message_type, value):
        reward = 0
        if message_type  == self.env.MessageType.values.QUESTION:
            self.QuestionOut[namespace] = value
            
        if message_type  == self.env.MessageType.values.ANSWER:
            old_value = self.QuestionIn.pop(namespace,None)
            if old_value is not None:
                reward = value - old_value
        return float(reward)

    def ResetQestionInOut(self):
        self.QuestionIn = {}
        self.QuestionOut = {}