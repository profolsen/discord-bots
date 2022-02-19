import os
from pathlib import Path
#the following is to solve a problem with python that only exists because of the stupidity of Guido.
path = Path(__file__)
while not str(path).endswith('discord-bots') :
    path = path.parent
os.environ['PROJECT_PATH'] = str(path.absolute())
os.environ['TOKEN_PATH'] = str(path.absolute()) + '/tokens'