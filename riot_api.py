import riotwatcher
from riotwatcher import RiotWatcher
import json

w = RiotWatcher('api_key')

# Static champion data from riot.
with open('Resources/champions.json') as data_file:
        Data = json.load(data_file)


def get_summonerId_from_name(summonerName):
    print "Getting info for summonerName: %s..." % summonerName
    summoner = w.get_summoner(name=summonerName)
    return summoner['id']


def get_champion(champ_id, data):
    champion = ''
    for key, value in data['data'].iteritems():
        if value['id'] == champ_id:
            champion = key

    if champion == '':
        return 'none'
    else:
        return champion


def get_match_players(summonerId):
    print "Getting current match..."
    current_match = w.get_current_game(summonerId)
    players = []

    for item in current_match['participants']:
        if item.get('summonerId') is not None:
            playerId = item.get('summonerId')
        if item.get('teamId') is not None:
            teamId = item.get('teamId')
        if item.get('championId') is not None:
            champId = item.get('championId')
            champ_name = get_champion(champId, Data)
        players.append([playerId, teamId, champ_name])

    return players

# summonerId is a string of summonerIds split by commas
def get_tier_division(summonerId):
    print "Getting league info for %s..." % summonerId
    leagues = w.get_league_entry([summonerId])
    return leagues

# takes a list of summonerIds
def get_unranked(summonerIds):
    print "Getting info for unranked summonerID: %s..." % summonerIds
    summoners = w.get_summoner_name(summonerIds)
    return summoners


def parse_leagues(players, leagues):
    ranks = []
    for player in players:
        league = leagues.get(str(player[0]), 'UNRANKED')

        if league != 'UNRANKED':
            for item in league:
                if item.get('queue') == 'RANKED_SOLO_5x5':

                    if item.get('tier') != None:
                        tier = item.get('tier')
                    if item.get('entries') != None:

                        for thingy in item.get('entries'):
                            division = thingy.get('division')
                            name = thingy.get('playerOrTeamName')
                            summonerid = thingy.get('playerOrTeamId')

            tier_division = [str(summonerid), str(name), str(tier), str(division)]
            ranks.append(tier_division)

    return ranks


def prettyfy_ranks(player_list):
    stringy = '\nTeam 1:\n'
    for key,value in player_list.iteritems():
        if value['team'] == 100:
            if value['tier'] == 'UNRANKED':
                stringy += '\t%s (%s): %s\n' % (value['name'], value['champion'], value['tier'])
            else:
                stringy += '\t%s (%s) : %s %s\n' % (value['name'], value['champion'], value['tier'], value['division'])

    stringy += '\nTeam 2:\n'
    for key,value in player_list.iteritems():
        if value['team'] == 200:
            if value['tier'] == 'UNRANKED':
                stringy += '\t%s (%s): %s\n' % (value['name'], value['champion'], value['tier'])
            else:
                stringy += '\t%s (%s): %s %s\n' % (value['name'], value['champion'], value['tier'], value['division'])

    return stringy


def get_match_ranks(summonerName):
    player_list = {}
    # Checks to make sure your summoner exists
    try:
        print "Getting match info for %s..." % summonerName
        sid = get_summonerId_from_name(summonerName)
    except riotwatcher.LoLException:
        return "No summoner found with name: %s" % summonerName
    # Checks to make sure you're in a game
    try:
        players = get_match_players(sid)
    except riotwatcher.LoLException:
        return "Summoner is not in a game."
    # player_list = {playerId: {name, champ, tier, division, team}}
    for player in players:
        player_list[str(player[0])] = {'name': None, 'champion': player[2], 'tier': 'UNRANKED', 'division': None, 'team': player[1]}

    temp = player_list.keys()
    id_list = ''
    for x in temp:
        id_list += str(x) + ','

    ranks = parse_leagues(players, get_tier_division(id_list))

    for x in ranks:
        info = player_list[x[0]]
        info['name'] = x[1]
        info['tier'] = x[2]
        info['division'] = x[3]
    # Gets summoner names for players who are unranked
    unranked_ids = []
    for key, value in player_list.iteritems():
        if value['tier'] == 'UNRANKED':
            unranked_ids.append(str(key))

    if len(unranked_ids) > 0:
        unranked_info = get_unranked(unranked_ids)

        for key, value in unranked_info.iteritems():
            temp = player_list[key]
            temp['name'] = value

    pretty_ranks = prettyfy_ranks(player_list)
    print "Done!"
    return pretty_ranks
