import subprocess as sp


def noun_number(count):
    return '' if count == 1 else 's'


def terminal_width():
    try:
        return int(sp.check_output(['stty', 'size']).decode().split()[1])
    except:
        return 80
