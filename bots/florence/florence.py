import discord
import sys
from bots.tokens_util import load_token_from_file
from datetime import datetime
token = load_token_from_file('florence')

client = discord.Client()
@client.event
async def on_ready():
    print('Logged in. Waiting...')

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
    if message.content.lower().startswith('update') :
        with open(sys.argv[1], 'a+') as output:
            for word in parts :
                output.write(word + "\n")
            output.write('updates\n')
            output.write('*' + str(datetime.now().timestamp()) + '\n')
    if message.content.lower().startswith('report') :
        if parts[0] == 'now' :
            try:
                with open(sys.argv[1]) as input:
                    lines = input.readlines()
                    wordcount = {}
                    for line in lines :
                        if not line.startswith('*') :
                            pureline = line[0:len(line) - 1]
                            wordcount[pureline] = wordcount[pureline] + 1 if pureline in wordcount else 1
                    await message.channel.send(str(wordcount))
            except FileNotFoundError :
                await message.channel.send('no updates found.')


        pass
        #await message.channel.send(message.content[11:])

if __name__ == "__main__" :
    client.run(token)

