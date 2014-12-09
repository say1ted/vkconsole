from __future__ import unicode_literals

from prompt_toolkit import CommandLineInterface
from prompt_toolkit.line import Line
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.prompt import DefaultPrompt
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.contrib.completers import WordCompleter

from pygments.token import Token
from pygments.style import Style


class VkStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion:         'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton:     'bg:#003333',
        Token.Menu.Completions.ProgressBar:        'bg:#00aaaa',
    }


def autocomplete(prompt, words):
    word_complete = WordCompleter(words)
    cli = CommandLineInterface(
        style=VkStyle,
        layout=Layout(before_input=DefaultPrompt(prompt),
                      menus=[CompletionsMenu()]),
        line=Line(completer=word_complete),
        create_async_autocompleters=True)
    try:
        code_obj = cli.read_input()
        return code_obj.text
    except Exception as err:
        print(err)
    return ''



if __name__ == '__main__':
    autocomplete('Select user:', ['Иван', 'Борис'])