from vkapi import VkApi
from autocomplete import autocomplete
from utils import getch, read_message, read_config
import time


if __name__ == "__main__":
    while True:
        token = read_config()['access_token']
        api = VkApi(token)
        print('Dialog list')
        for dialog in api.get_dialogs():
            dialog.print()
        dialog_title = autocomplete('Select dialog:', api.dialog_names())
        dialog = api.dialog_history(dialog_title)
        dialog.print()
        message = read_message('Message (press [Enter] to send, [Backspace] to back, [ESC] to exit):')
        if message:
            api.send_dialog(dialog, message)
        print('Wait to refresh dialogs...')
        time.sleep(3)

