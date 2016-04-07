import discord
import riot_api as rito
import random
from giphypop import screensaver
import logging
import cleverbot
import json
import utils

logging.basicConfig(level=logging.INFO)

utils.check_auth()

client = discord.Client()
json_info = json.load(open('auth.json'))

try:
    email = json_info['discord_email']
    password = json_info['discord_password']
except KeyError:
    print 'Auth info not found'

client.login(email, password)

cb1 = cleverbot.Cleverbot()

@client.event
def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        client.send_message(message.channel, 'Hello {}!'.format(message.author.mention()))

    # hehe
    if ('is Will awesome?') in message.content:
        client.send_message(message.channel, 'Of course he is {}!'.format(message.author.mention()))

    # LoLNexus lite in chat
    if message.content.startswith('!currentgame'):
        summoner = message.content[13:]
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
        rng = random.randint(1, 3)
        if rng == 1:
            client.send_message(message.channel, 'Dank meme {}'.format(message.author.mention()))

    # Random gif using giphy: https://github.com/shaunduncan/giphypop
    if message.content.startswith('!gif'):
        search_term = message.content[5:]
        gif = screensaver(search_term)
        try:
            client.send_message(message.channel, '#{} {}'.format(search_term, gif['url']))
        except TypeError:
            client.send_message(message.channel, 'No gif found for {}'.format(search_term))

    # Ultimate bravery in chat
    if message.content.startswith('!bravery'):
        build = None
        map = message.content[9:]
        if map == '' or map == "Summoner's Rift" or map == 'SR':
            build = rito.ultimate_bravery(11)
        elif map == 'Twisted Treeline' or map == 'TT':
            build = rito.ultimate_bravery(10)
        elif map == 'Howling Abyss' or map == 'HA' or map == 'ARAM':
            build = rito.ultimate_bravery(12)
        else:
            client.send_message(message.channel, "Please specify map: Summoner's Rift, Twisted Treeline, or Howling Abyss")
        if build is not None:
            client.send_message(message.author, '{}: {}'.format(message.author, build))
            client.send_message(message.channel, 'Check your PMs {}!'.format(message.author.mention()))

    # Need to find a way to auto update this as new methods are added
    if message.content.startswith('!help'):
        client.send_message(message.channel, 'Current commands: !hello, !currentgame, /roll, !gif, !bravery')

    # Uses cleverbot for mentions: https://github.com/folz/cleverbot.py
    if client.user in message.mentions:
        new_content = message.content.replace('<@{}>'.format(client.user.id), '')
        client.send_message(message.channel, '{}'.format(cb1.ask(new_content)))


@client.event
def on_member_join(member):
    server = member.server
    client.send_message(server, 'Welcome {0} to {1.name}!'.format(member.mention(), server))


@client.event
def on_member_update(before, after):
    old_status = before.status
    new_status = after.status
    old_game = before.game
    new_game = after.game
    # Announces when someone comes online or starts playing a game
    if old_status != new_status:
        if new_status == 'online' or new_status == 'offline' and old_status != 'idle':
            client.send_message(after.server.channels[0], '%s is now %s' % (after.name, new_status))
    elif old_game != new_game:
        if new_game is not None:
            client.send_message(after.server.channels[0], '%s is now playing %s' % (after.name, new_game))

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()
