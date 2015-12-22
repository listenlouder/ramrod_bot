import riotwatcher
from riotwatcher import RiotWatcher

w = RiotWatcher('api-key')


def get_summonerId_from_name(summonerName):
    print "Getting info for summonerName: %s..." % summonerName
    summoner = w.get_summoner(name=summonerName)
    return summoner['id']


def get_summoner_name_from_id(summonerId):
    print "Getting info for summonerID: %s..." % summonerId
    summoner = w.get_summoner(name=None, _id=summonerId)
    name = summoner.get('name')
    return name


def get_match_players(summonerId):
    print "Getting current match..."
    current_match = w.get_current_game(summonerId)
    players = []
    for item in current_match['participants']:
        if item.get('summonerId') != None:
            playerId = item.get('summonerId')
        if item.get('teamId') is not None:
            teamId = item.get('teamId')
        players.append([playerId, teamId])
    return players


def get_tier_division(summonerId, teamId):
    try:
        print "Getting league info for %s..." % summonerId
        league = w.get_league_entry([summonerId])
        temp = league[str(summonerId)]
        for item in temp:
            if item.get('queue') == 'RANKED_SOLO_5x5':
                if item.get('tier') != None:
                    tier = item.get('tier')
                if item.get('entries') != None:
                    for thingy in item.get('entries'):
                        division = thingy.get('division')
                        name = thingy.get('playerOrTeamName')
            tier_division = [str(name), str(tier), str(division), teamId]

    except riotwatcher.LoLException:
        print "Unranked summoner %s" % summonerId
        tier_division = [get_summoner_name_from_id(summonerId), 'Unranked', None, teamId]

    return tier_division

# Formats everything all pretty like for chat
def prettyfy_ranks(ranks):
    stringy = '\nTeam 1:\n'
    for item in ranks:
        if ranks[3] == 100:
            if item[1] == 'Unranked':
                stringy += '\t%s: %s\n' % (item[0], item[1])
            else:
                stringy += '\t%s: %s %s\n' % (item[0], item[1], item[2])

    stringy += '\nTeam 2:\n'
    for item in ranks:
        if ranks[3] == 200:
            if item[1] == 'Unranked':
                stringy += '\t%s: %s\n' % (item[0], item[1])
            else:
                stringy += '\t%s: %s %s\n' % (item[0], item[1], item[2])

    return stringy


# Making sure it doesn't bomb if your discord name doesn't match your IGN
def get_match_ranks(summonerName):
    try:
        print "Getting match info for %s..." % summonerName
        id = get_summonerId_from_name(summonerName)
    except riotwatcher.LoLException:
        return "No summoner found with name: "

    players = get_match_players(id)

    ranks = []
    for player in players:
        temp = get_tier_division(player[0], player[1])
        ranks.append(temp)
    pretty_ranks = prettyfy_ranks(ranks)
    print "Done!"
    return pretty_ranks
