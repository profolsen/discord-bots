import os


def load_token_from_file(name):
    source = open(os.getenv('TOKEN_PATH') + '/' + name, 'r')
    token = source.readlines()[0]
    return token
