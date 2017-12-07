from SwergioUtility.MessageUtility.MessageParts.baseClass import BaseMessagePart

class ChatNumber(BaseMessagePart):

    def __init__(self, custom_settings_path = None):
        super(ChatNumber, self).__init__('ChatNumber', custom_settings_path)
        
