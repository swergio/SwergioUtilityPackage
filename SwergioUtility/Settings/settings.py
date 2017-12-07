import json
import os
from os.path import dirname
from os.path import join 
import enum

def getSettingsJSON(custom_settings_path = None):
    settings = None
    if custom_settings_path is not None:
        with open(custom_settings_path) as json_data:
            settings = json.load(json_data)

    dir = dirname(__file__)
    with open(join(dir,'DEFAULT_settings.json')) as json_data:
        default_settings = json.load(json_data)

    return settings, default_settings

def _getSetting(settings,key):
    if settings is None:
        return None
    ks = key.split('.')
    set = settings
    for k in ks:
        set = set.get(k)
        if set is None:
            return None
    return set

def getSetting(settings,default_settings,key):
    value = _getSetting(settings,key)
    if value is not None:
        return value
    value = _getSetting(default_settings,key)
    return value

def SettingToEnum(name,setting):
    enum_dict = {}
    for e in setting:
        enum_dict[e['Name']] = e['Value']

    return enum.Enum(name, enum_dict)


def getBasicSettings(custom_settings_path = None):    
    settings,default_settings = getSettingsJSON(custom_settings_path = custom_settings_path) 
    '''
    Maximum length of message text
    '''
    max_length_message_text = getSetting(settings,default_settings,'MessageParts.MessageText.MessageSize')

    '''
    MessageType Enum
    '''
    MessageTypeEnum = SettingToEnum('MessageType', getSetting(settings,default_settings,'MessageParts.MessageType.Enums'))
        
    return max_length_message_text, MessageTypeEnum

def getMessagePartSettings(message_part_name,custom_settings_path = None):  
    settings,default_settings = getSettingsJSON(custom_settings_path = custom_settings_path) 

    key_part = 'MessageParts.' + message_part_name+ '.'

    message_position  =  getSetting(settings,default_settings,key_part +'MessagePosition')
    message_size = getSetting(settings,default_settings,key_part +'MessageSize')
    vocab_size  = getSetting(settings,default_settings,key_part +'VocabSize')
    action_size  = getSetting(settings,default_settings,key_part +'ActionSize')
    embedding_size  = getSetting(settings,default_settings,key_part +'EmbeddingSize')

    values  = SettingToEnum('MessageType', getSetting(settings,default_settings,key_part + 'Enums'))

    return message_position, message_size, vocab_size, action_size, embedding_size, values

def getReviewerSettings(custom_settings_path = None): 
    settings,default_settings = getSettingsJSON(custom_settings_path = custom_settings_path) 

    fail_reward_max = getSetting(settings,default_settings,'CommunicationEnviroment.Reviewer.FailRewardMax')
    fail_reward_min = getSetting(settings,default_settings,'CommunicationEnviroment.Reviewer.FailRewardMin')
    used_namespace = getSetting(settings,default_settings,'CommunicationEnviroment.Reviewer.UsedNamespace')

    return fail_reward_max, fail_reward_min, used_namespace
