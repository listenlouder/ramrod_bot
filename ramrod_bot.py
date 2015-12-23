import discord
import riot_api as rito

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

    # As long as your discord name is the same as your IGN this will work.
    if message.content.startswith('!currentgame'):
        temp = rito.get_match_ranks(str(message.author))
        if temp.startswith('No summoner found with name: '):
            client.send_message(message.channel, 'No Summoner found with name: {}'.format(message.author))
        elif temp.startswith('Summoner is not in a game.'):
            client.send_message(message.channel, 'Summoner is not in a game.')
        else:
            client.send_message(message.channel, 'Current player tiers and divisions: {}'.format(temp))


@client.event
def on_member_join(member):
    server = member.server
    client.send_message(server, 'Welcome {0} to {1.name}!'.format(member.mention(), server))


@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()
