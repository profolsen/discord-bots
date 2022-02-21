import discord
import sys
from bots.tokens_util import load_token_from_file
from datetime import datetime
import sqlite3
from bots import sqlutil
token = load_token_from_file('florence')

client = discord.Client()
@client.event
async def on_ready():
    conn = sqlutil.connect(True)
    sqlutil.reset(conn)
    conn.close()
    print('Database Ready...')

#message events:
#update category [attribute [...]]
#report now
#report csv


@client.event
async def on_message(message) :
    print('received: ' + message.content)
    parts = message.content.split()
    end = None
    parts = parts[1:end] #ignore command.
    conn = sqlutil.connect(False)
    if message.content.lower().startswith('update') :
        sqlutil.update(conn, parts[0], parts[1:end])
        pass
    if message.content.lower().startswith('report') :
        reporttype = parts[0]
        parts = parts[1:end]
        response = 'Internal Error'
        if reporttype == 'now' :
            response = sqlutil.reportnow(conn)
        elif reporttype == 'daily' :
            response = sqlutil.dailydata(conn, parts[0], parts[1], parts[2:end])
        elif reporttype == 'diff' :
            response = sqlutil.timediff(conn, parts[0], parts[1])
        await message.channel.send(response)
    conn.close()
        #message.channel.send(str(wordcount))
        #await message.channel.send(message.content[11:])

if __name__ == "__main__" :
    client.run(token)

