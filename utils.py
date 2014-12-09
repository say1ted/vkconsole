import sys, tty, termios, os
from json import load


def getch():
    '''
        Gets a single character from standard input.
    '''
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    #echo
    sys.stdout.write(ch)
    sys.stdout.flush()
    return ch

def read_message(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    value = []
    while True:
        ch = getch()
        if ord(ch) == 27:
            sys.stdout.write('\n')
            sys.stdout.flush()
            sys.exit(0)

        if ord(ch) == 127:
            sys.stdout.write('\n')
            sys.stdout.flush()
            return ''

        value.append(ch)


        if ord(ch) == 13:
            sys.stdout.write('\n')
            sys.stdout.flush()
            return ''.join(value)

def read_config():
    config_filename = ".vk.json"
    config_list = [
          os.path.join(os.path.abspath(os.path.dirname(__file__)), config_filename),
          os.path.join(os.getenv('HOME'), config_filename)
    ]

    config_contents = None
    for config in config_list:
        if os.path.isfile(config):
            try:
                with open(config) as f:
                    config_contents = load(f)
            except:
                print("Error opening configuration file", config)
                return None

            return config_contents

    return None
