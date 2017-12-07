from SwergioUtility.Settings.settings import getReviewerSettings
from SwergioUtility.MessageUtility.MessageInterface.messageInterface import MessageInterface


import sys
class Reviewer():

    def __init__(self, CommunicationEnv):
        self.env = CommunicationEnv
        self.fails = 0
        self.fail_reward_max, self.fail_reward_min, self.used_namespace  = getReviewerSettings(self.env.custom_settings_path)
        sys.setrecursionlimit(1500)

    def review(self, message):
        result = True
        for fn in self.env._ReviewFunctions:
            if fn(self, message) == False:
                result = False
                self.fails += 1
                self.emitReview(message)

        return result

    def emitReview(self, message):
        namespace = self.used_namespace
        reward =  max(self.fail_reward_min,self.fail_reward_max + int(self.fails * (self.fail_reward_min - self.fail_reward_max)))
        body = 'failed review'   
        message_type = self.env.MessageType.values.ANSWER.name
        communication_id = message.CommunicationID
        sender_id = self.env._socketIOSenderID

        msg = MessageInterface(namespace,sender_id, message_type,communication_id,Data = body, Reward = reward, DoneFlag = False)
        self.env._socketIOClient.emit(msg,namespace)
        
