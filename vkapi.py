import vk
from datetime import datetime

class VkApi():
    def __init__(self, token):
        self._api = vk.API(access_token=token)
        self._user_objects = []
        self._dialog_objects = []
        self._fill_data()

    def _fill_data(self):
        my_user = self._api.users.get()[0]
        self.my_name = '{} {}'.format(my_user['first_name'], my_user['last_name'])
        self._dialog_objects = self._api.messages.getDialogs(count=10)['items']

        #get users info
        user_ids = []
        for dialog_obj in self._dialog_objects:
            message_obj = dialog_obj['message']
            user_id = str(message_obj['user_id'])
            if not user_id in user_ids:
                user_ids.append(user_id)
        self._user_objects = self._api.users.get(user_ids=','.join(user_ids))

    def get_dialogs(self):
        dialogs = []
        for dialog_obj in self._dialog_objects:
            message_obj = dialog_obj['message']
            user = self.user_by_id(message_obj['user_id'])
            user_name = '{} {}'.format(user['first_name'], user['last_name'])
            message = VkMessage(message_obj, user_name, self.my_name)
            dialog = VkDialog(dialog_obj, [message])
            dialogs.append(dialog)
        return dialogs

    def dialog_names(self):
        names =[]
        for dialog in self.get_dialogs():
            names.append(dialog.title)
        return names

    def dialog_history(self, dialog_title):
        dialog = self.dialog_by_title(dialog_title)

        if dialog.chat:
            messages_obj = self._api.messages.getHistory(count=10, chat_id=dialog.dialog_obj['message']['chat_id'])['items']
        else:
            messages_obj = self._api.messages.getHistory(count=10, user_id=dialog.dialog_obj['message']['user_id'])['items']
        dialog.messages = []
        for message_obj in messages_obj:
            user = self.user_by_id(message_obj['user_id'])
            user_name = '{} {}'.format(user['first_name'], user['last_name'])
            message = VkMessage(message_obj, user_name, self.my_name)
            dialog.messages.append(message)
        return dialog

    def dialog_by_title(self, title):
         for dialog in self.get_dialogs():
             if dialog.title == title:
                return dialog

    def user_by_id(self, user_id):
         for user in self._user_objects:
                if user['id'] == user_id:
                    return user

    def send_dialog(self, dialog, message):
        message_obj = dialog.dialog_obj['message']
        if dialog.chat:
            self._api.messages.send(chat_id=message_obj['chat_id'], message=message)
        else:
            self._api.messages.send(user_id=message_obj['user_id'], message=message)

class VkDialog():
    def __init__(self, dialog_obj, messages):
        self.dialog_obj = dialog_obj
        self.chat = False
        self.messages = messages
        self._parse()

    def _parse(self):
        if hasattr(self.messages[0], 'chat_id'):
            self.chat = True
        self.title = self.messages[0].title

    def print(self):
        print(self.title)
        for message in self.messages:
            message.print()

class VkMessage():
    def __init__(self, message_obj, user_name, my_name):
        self.message_obj = message_obj
        self.user_name = user_name
        self.my_name = my_name
        self._parse()

    def _parse(self):
        self.message = self.message_obj['body']
        self.date = datetime.fromtimestamp(self.message_obj['date'])
        if self.message_obj['out'] == 1:
            self.sender_name = self.my_name
        else:
            self.sender_name = self.user_name
        if 'chat_id' in self.message_obj:
            self.chat_id = self.message_obj['chat_id']
            self.title = self.message_obj['title']
        else:
            self.title = self.user_name


    def print(self):
        print('{} ({})'.format(self.sender_name, self.date))
        print('\t{}\n'.format(self.message))




