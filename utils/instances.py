from telegram import Update


class Message:

    def __init__(self, update: Update):
        update_dict = update.to_dict()

        if 'channel_post' in update_dict:
            self.type = update_dict['channel_post']['chat']['type']
        else:
            self.type = update_dict['message']['chat']['type']


        self.text = ''
        if 'caption' not in update_dict and 'text' in update_dict['message']:
            self.text = update_dict['channel_post']['text'] \
                if 'channel_post' in update_dict else update_dict['message']['text']
        elif 'text' in update_dict['message']:
            self.text = update_dict['channel_post']['caption'] \
                if 'channel_post' in update_dict else update_dict['message']['caption']
        self.text_array = self.text.split()
        self.len = len(self.text_array)

        self.sender_id = 0 if self.type == 'channel' else update_dict['message']['from']['id']

        self.chat_id = update_dict['channel_post']['sender_chat']['id'] \
            if self.type == 'channel' else update_dict['message']['chat']['id']

        if self.type == 'channel' :
            self.chat_name = update_dict['channel_post']['chat']['username']
        elif self.type == 'private':
            self.chat_name = '@' + update_dict['message']['chat']['username']
        elif self.type == 'group' or self.type == 'supergroup':
            self.chat_name = update_dict['message']['chat']['title']
        self.message_id = update_dict['channel_post']['message_id'] \
            if self.type == 'channel' else update_dict['message']['message_id']
