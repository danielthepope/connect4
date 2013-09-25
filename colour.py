white = ''
magenta = ''
cyan = ''
blue = ''
green = ''
yellow = ''
red = ''
default = ''
    
def enable():
    global white
    global magenta
    global cyan
    global blue
    global green
    global yellow
    global red
    global default

    white = '\033[97m'
    cyan = '\033[96m'
    magenta = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    default = '\033[0m'
