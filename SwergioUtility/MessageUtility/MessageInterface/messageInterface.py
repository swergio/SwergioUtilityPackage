from uuid import uuid4
from time import time

'''
Basic class for external messages to communicate between swergio components
'''
class MessageInterface():

    def __init__(self,NameSpace,SenderID, MessageType,CommunicationID = None,  MessageID = None, TimeStamp = None, Data = [], Reward = 0.0, DoneFlag = False):
        self.NameSpace = NameSpace
        self.MessageID = MessageID if MessageID is not None else uuid4()
        self.MessageType = MessageType
        self.SenderID = SenderID
        self.TimeStamp = TimeStamp if TimeStamp is not None else time()
        self.CommunicationID = CommunicationID 
        self.Data = Data
        self.StepID = None
        self.Reward = Reward
        self.DoneFlag = DoneFlag

    def AddBody(self,Body, BodyType = None):
        self.Body = Body

    def SetStepID(self,StepID):
        self.StepID = StepID

    def to_document(self):
        return dict(
            NameSpace = str(self.NameSpace),
            MessageID = str(self.MessageID),
            MessageType = str(self.MessageType),
            SenderID = str(self.SenderID),
            TimeStamp = str(self.TimeStamp),
            CommunicationID = str(self.CommunicationID),
            Data = self.Data,
            Reward = self.Reward,
            DoneFlag = self.DoneFlag
        ) 

    @classmethod
    def from_document(cls,document):
        NameSpace = document['NameSpace']
        MessageID = document['MessageID']
        MessageType = document['MessageType']
        SenderID = document['SenderID']
        TimeStamp = document['TimeStamp']
        CommunicationID = document['CommunicationID'] if 'CommunicationID' in document else None
        Data  = document['Data']
        Reward = document['Reward']
        DoneFlag = document['DoneFlag']
        
        return cls(NameSpace,SenderID, MessageType, CommunicationID ,MessageID, TimeStamp , Data, Reward,DoneFlag )

    