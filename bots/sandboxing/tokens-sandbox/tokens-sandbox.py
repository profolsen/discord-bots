import sys
import os

from bots import tokens_util


if __name__ == "__main__" :
    token = tokens_util.load_token_from_file('florence')
    print(token)

