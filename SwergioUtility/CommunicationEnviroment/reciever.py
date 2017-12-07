from SwergioUtility.MessageUtility.MessageInterface.messageInterface import MessageInterface

class Reciever():

    def __init__(self,communication_enviroment):
        self.env = communication_enviroment

        self.black_list = []

    def On_Message(self,data):
        msg = MessageInterface.from_document(data)
        if (msg.SenderID != str(self.env._socketIOSenderID) or msg.NameSpace == 'InternReview') and msg.CommunicationID not in self.black_list:
            self.env.Messages.addMessage(msg)
            msg = self.env.Messages.GetLastNMessages(1,msg.CommunicationID)[0]

            internal_message, reward, done, comID, step = self.env.InternalMessageHandler.ExternalMessageToRL(msg)
            #If recieved message with DONE = True flag forward all other channels:
            if done:
                self.env.Sender.ForwardFeedback(msg)
                self.black_list.append(msg.CommunicationID)
            self.env.message_callback(internal_message, 
                                    reward, 
                                    done, 
                                    comID, 
                                    step, 
                                    msg.CommunicationID,
                                    msg.NameSpace,
                                    self.env.MessageType.GetValueByName(msg.MessageType))

    