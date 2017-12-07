from SwergioUtility.MessageUtility.MessageParts.baseClass import BaseMessagePart

class ActionFlag(BaseMessagePart):

    def __init__(self, custom_settings_path = None):
        super(ActionFlag, self).__init__('ActionFlag', custom_settings_path)