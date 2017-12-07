import json
import os
from os.path import dirname
from os.path import join 
import enum
import numpy as np

from SwergioUtility.Settings.settings import getMessagePartSettings



class BaseMessagePart():

    def __init__(self, message_part_name,custom_settings_path = None):    
        message_position, message_size, vocab_size, action_size, embedding_size, values = getMessagePartSettings(message_part_name,custom_settings_path)

        self.message_position  = message_position
        self.message_size = message_size
        self.vocab_size  = vocab_size
        self.action_size  = action_size
        self.embedding_size  = embedding_size
        self.values  = values


    def IndexToOneHot(self, indices):
        import tensorflow as tf
        return tf.one_hot(indices,self.vocab_size)

    def OneHotToIndex(self,onehots):
        import tensorflow as tf
        return tf.argmax(onehots,axis = 1)

    def IndexToValue(self,indices):
        if type(indices) == np.ndarray:
            indices = indices.tolist()
        return [self.values(i) for i in indices]

    def ValueToIndex(self, values):
        return np.asarray([e.value for e in values])

    def ValueNameToIndex(self, names):
        return np.asarray([self.values[n].value for n in names])

    def ValueToOneHot(self,values):
        indices = self.ValueToIndex(values)
        return self.IndexToOneHot(indices)

    def OneHotToValue(self, onehots):
        indices = self.OneHotToIndex(onehots)
        return self.IndexToValue(indices)

    def GetValueByIndex(self,index):
        return self.values(index)

    def GetValueByName(self, name):
        return self.values[name]

    def GetValueNameByIndex(self, index):
        return self.values(index).name

