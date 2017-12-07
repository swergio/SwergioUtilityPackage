import numpy as np

from SwergioUtility.MessageUtility.MessageParts.baseClass import BaseMessagePart


class FeedbackReward(BaseMessagePart):

    def __init__(self, custom_settings_path = None):    
       super(FeedbackReward, self).__init__('ActionFlag', custom_settings_path)



    def IndexToValue(self,indices):
        return [i + self.values.LOWERBOUND.value for i in indices]

    def ValueToIndex(self, values):
        return np.asarray([v - self.values.LOWERBOUND.value for v in values])


    def NormalizeValue(self,values,to=[-1,1]):
        oL = self.values.LOWERBOUND.value
        oU = self.values.UPPERBOUND.value
        nL = to[0]
        nU = to[1]
        return [((v - oL)/(oU-oL))*(nU-nL) + nL  for v in values]

    def NormalizeToBounds(self,values, from_bound=[-1,1]):
        oL = from_bound[0]
        oU = from_bound[1]
        nL = self.values.LOWERBOUND.value
        nU = self.values.UPPERBOUND.value
        return [((v - oL)/(oU-oL))*(nU-nL) + nL  for v in values]


if __name__ == "__main__":
    x = FeedbackReward()
    print(x.NormalizeValue([-100,-50,20,60,100,0]))
    print(x.NormalizeValue([-100,-50,20,60,100,0],[0,2]))
    print('Hello')