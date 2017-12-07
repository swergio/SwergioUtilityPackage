from SwergioUtility.MessageUtility.MessageParts.baseClass import BaseMessagePart

class MessageType(BaseMessagePart):

    def __init__(self, custom_settings_path = None):
        super(MessageType, self).__init__('MessageType', custom_settings_path)