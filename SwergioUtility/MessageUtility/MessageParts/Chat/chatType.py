from SwergioUtility.MessageUtility.MessageParts.baseClass import BaseMessagePart

class ChatType(BaseMessagePart):

    def __init__(self, custom_settings_path = None):
        super(ChatType, self).__init__('ChatType', custom_settings_path)
        