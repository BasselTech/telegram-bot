class Message:
    supported_types = ['text', 'audio', 'document', 'photo']

    def __init__(self, message):
        self.chat_id = message['from']['id']
        for message_type in self.supported_types:
            if message.get(message_type):
                self.type = message_type
                self.value = message[message_type]
                break
            else:
                self.type = False
                self.value = False

    def _text_get_response(self):
        response = {
            'text': self.value,
        }
        method_name = 'sendMessage'
        return method_name, response

    def _not_implemented_response(self):
        response = {
            'text': 'I am sorry. This type is not implemented!',
        }
        method_name = 'sendMessage'
        return method_name, response

    def get_response(self):
        if self.type and hasattr(self, '_%s_get_response' % self.type):
            result = getattr(self, '_%s_get_response' % self.type)()
        else:
            result = self._not_implemented_response()

        assert isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], dict)

        result[1].update({
            'chat_id': self.chat_id,
        })
        return result