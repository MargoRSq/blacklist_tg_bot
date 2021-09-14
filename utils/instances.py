from telegram import Update


class Message:

    def __init__(self, update: Update):
        update = update.to_dict()

        if 'channel_post' in update:
            self.type = update['channel_post']['chat']['type']
        else:
            self.type = update['message']['chat']['type']

        self.text = update['channel_post']['text'] \
            if 'channel_post' in update else update['message']['text']
        self.text_array = self.text.split()
        self.len = len(self.text_array)

        self.sender_id = 0 if self.type == 'channel' else update['message']['from']['id']

        self.chat_id = update['channel_post']['sender_chat']['id'] \
            if self.type == 'channel' else update['message']['chat']['id']

        self.message_id = update['channel_post']['message_id'] \
            if self.type == 'channel' else update['message']['message_id']
