import discord
import riot_api as rito
import random
from giphypop import screensaver

client = discord.Client()
client.login('email', 'password')


@client.event
def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        client.send_message(message.channel, 'Hello {}!'.format(message.author.mention()))

    # hehe
    if message.content.startswith('is Will awesome?'):
        client.send_message(message.channel, 'Of course he is {}!'.format(message.author.mention()))

    # LoLNexus lite in chat
    if message.content.startswith('!currentgame'):
        summoner = message.content[13:]
        print summoner
        if len(summoner) < 1:
            summoner = str(message.author)

        temp = rito.get_match_ranks(summoner)
        if temp.startswith('No summoner found with name: '):
            client.send_message(message.channel, 'No Summoner found with name: {}'.format(summoner))
        elif temp.startswith('Summoner is not in a game.'):
            client.send_message(message.channel, '{} is not in a game.'.format(summoner))
        else:
            client.send_message(message.channel, 'Current player tiers and divisions: {}'.format(temp))

    if message.content.startswith('/roll'):
        roll = random.randint(1, 100)
        client.send_message(message.channel, '{} rolls {}'.format(message.author, roll))

    if message.content.startswith('http://i.imgur.com/'):
        client.send_message(message.channel, 'Dank meme {}'.format(message.author.mention()))
    # Random gif using giphy api
    if message.content.startswith('!gif'):
        search_term = message.content[5:]
        gif = screensaver(search_term)
        client.send_message(message.channel, '#{} {}'.format(search_term, gif['url']))
    # Need to find a way to auto update this as new methods are added
    if message.content.startswith('!help'):
        client.send_message(message.channel, 'Current commands: !hello, !currentgame, /roll, !gif')


@client.event
def on_member_join(member):
    server = member.server
    client.send_message(server, 'Welcome {0} to {1.name}!'.format(member.mention(), server))


@client.event
def on_status(member, arg2, status):
    channels = member.server.channels
    new_status = None
    # Because it says offline when someone joins and ditto with the inverse...
    if status == 'offline':
        new_status = 'online'
    elif status == 'online':
        new_status = 'offline'
    # We only care about online/offline
    if new_status is not None:
        client.send_message(channels[0], '{} is now {}'.format(member.name, status, tts=True))
        # tts doesn't appear to work sometimes
    else:
        print status

    print arg2  # This might be game id? IDK


@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()
