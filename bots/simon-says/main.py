import discord
from bots import tokens_util
token = tokens_util.load_token_from_file('simon-says')

client = discord.Client()
@client.event
async def on_ready():
    print('Logged in. Waiting...')

@client.event
async def on_message(message) :
    if message.author == client.user: #client.user must be the bot itself.
        return
    if message.content.startswith('$simon says'):
        await message.channel.send(message.content[11:])

if __name__ == "__main__" :
    client.run(token)

