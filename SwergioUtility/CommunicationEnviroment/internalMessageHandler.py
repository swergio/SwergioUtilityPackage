import numpy as np
from SwergioUtility.MessageUtility.MessageInterface.messageInterface import MessageInterface

class InternalMessageHandler():

    def __init__(self,communication_enviroment):
        self.env = communication_enviroment

    def ExternalToInternalMessage(self,external_message):
        nspace = external_message.NameSpace
        chat_detail = [(k,v.index(nspace)) for k,v in self.env._socketIONamespacesDict.items() if nspace in v]
        ctyi = self.env.ChatType.ValueNameToIndex([chat_detail[0][0]])
        cnri = self.env.ChatNumber.ValueToIndex([self.env.ChatNumber.GetValueByIndex(chat_detail[0][1])])

        mtyi = self.env.MessageType.ValueNameToIndex([external_message.MessageType])
        mtxt = self.env.MessageText.ValueToIndex([external_message.Data.lower()])
        mtxt = self.env.MessageText.PadIndex(mtxt,self.env.LengthOfMessageText)

        mtxt = np.reshape(mtxt,(int(mtxt.shape[0])*int(mtxt.shape[1])))
        mact = [1]
        internal_message = np.concatenate((ctyi,cnri,mtyi,mtxt,mact))
        return internal_message

    def ExternalMessageToRL(self, external_message):
        internal_message = self.ExternalToInternalMessage(external_message)
        comID = external_message.CommunicationID
        step = external_message.StepID
        reward = external_message.Reward
        done = external_message.DoneFlag
        return internal_message, reward, done, comID, step

    def SplitInternalMessage(self,internal_message, queeze = False):
        if queeze:
            internal_message  = np.squeeze(internal_message)
        cty,cnr, mty, mtxt, act = np.split(internal_message,np.cumsum(self.env.message_space), axis=-1)[:-1]
        return cty,cnr, mty, mtxt, act 

    def InternalToExternalMessage(self,internal_message):
        ctyi,cnri, mtyi, mtxt, act = self.SplitInternalMessage(internal_message, queeze = True)

        nameSpace = ""
        try:
            nameSpace = self.env._socketIONamespacesDict[self.env.ChatType.GetValueNameByIndex(ctyi)][cnri[0]]
        except:
            pass
        
        msgTyp = self.env.MessageType.IndexToValue(mtyi)[0].name
        if isinstance(mtxt, np.ndarray):
            mtxt = list(mtxt) 
        obBody = self.env.MessageText.IndexToValue([mtxt])[0]

        external_message = MessageInterface(nameSpace,self.env._socketIOSenderID, msgTyp,None,Data = obBody)
        return external_message

    def MaskTextOfInternalMessage(self,internal_message, text_length, AddStartToken = False):
        cty,cnr, mty, mtxt, act = self.SplitInternalMessage(internal_message)
        partial_message_text,_ = np.split(mtxt,(text_length,), axis = 1)

        if AddStartToken:
            partial_message_text = self.env.MessageText.AddStartToken(partial_message_text)
        partial_message_text = self.env.MessageText.PadIndex(partial_message_text,self.env.LengthOfMessageText)
        new_internal_message= np.concatenate((cty,cnr,mty,partial_message_text,act), axis = 1)

        return new_internal_message, partial_message_text
