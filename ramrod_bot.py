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

    if message.content.startswith('is Sam gay?'):
        client.send_message(message.channel, 'Of course he is {}!'.format(message.author.mention()))

    if message.content.startswith('!currentgame'):
        temp = rito.get_match_ranks('listenlouder')
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
