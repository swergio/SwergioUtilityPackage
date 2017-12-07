from enum import Enum
import numpy as np

from SwergioUtility.MessageUtility.MessageParts.Text.textDictionary import TextDictionary
from SwergioUtility.MessageUtility.MessageParts.baseClass import BaseMessagePart

class MessageText(BaseMessagePart):

    def __init__(self, expert_data = None, dictionary_text_path = None, custom_settings_path = None):
        super(MessageText, self).__init__('MessageText', custom_settings_path)
        self.spezial_token =  self.values
        expert_data.setMaxTextLentgh(self.message_size)

        self.dictionary = TextDictionary(max_dictionary_size = self.vocab_size - len(self.spezial_token),
                                        expert_data = expert_data,
                                        dictionary_text_path = dictionary_text_path)

    def IndexToValue(self,indices, return_text_only = True):
        text = []
        for ind in indices:
            t = []
            startj = -1
            endj = len(ind)

            for j,i in enumerate(ind):
                if i in range(len(self.spezial_token)):
                    if self.spezial_token(i) == self.spezial_token.STARTMESSAGE:
                        startj = j
                    if self.spezial_token(i) == self.spezial_token.ENDMESSAGE or self.spezial_token(i) == self.spezial_token.NIL:
                        endj = j
                        break
                
            txtidx = ind[startj +1:endj]
            if return_text_only is False:
                t.append(self.spezial_token.STARTMESSAGE.name)
            t.append(self.dictionary.IndexToText(txtidx,len(self.spezial_token)))
            if return_text_only is False:
                t.append(self.spezial_token.ENDMESSAGE)
            text.append(''.join(t))
        return text

    
    def ValueToIndex(self, txts, add_endtoken = True):
        ind = []
        for txt in txts:
            i = []
            i = i + self.dictionary.TextToIndex(txt,len(self.spezial_token))
            
            if add_endtoken:
                i = i +[self.spezial_token.ENDMESSAGE.value]
            ind.append(i)
        return np.asarray(ind)

    def IndexSartMessage(self,times):
        return np.expand_dims(np.asarray([self.spezial_token.STARTMESSAGE.value]*times),-1)

    def IndexNILMessage(self,times):
        return np.expand_dims(np.asarray([self.spezial_token.NIL.value]*times),-1)

    def PadIndex(self,indices, max_length = None):
        if max_length is None:
            max_length = self.message_size
        PADDING_index = self.spezial_token.NIL.value
        n_indices = []
        for i,ind in enumerate(indices):   
            if    len(ind) < max_length:
                n_indices.append(np.lib.pad(ind,(0,max_length-len(ind)), 'constant', constant_values=(PADDING_index, PADDING_index)).tolist())
            else:
                n_indices.append(ind.tolist()[:max_length])

        return np.asarray(n_indices)

    def AddStartToken(self,indices):
        STARTMESSAGE_index = self.spezial_token.STARTMESSAGE.value
        return np.concatenate((np.full((indices.shape[0],1),STARTMESSAGE_index),indices),axis=1)

    def MaskEndMessage(self, indices):
        import tensorflow as tf
        end = tf.zeros(indices.shape,tf.int64) + self.spezial_token.ENDMESSAGE.value
        return tf.to_int64(tf.not_equal(indices, end))
