import riotwatcher
from riotwatcher import RiotWatcher

w = RiotWatcher('api-key')


def get_summonerId_from_name(summonerName):
    print "Getting info for summonerName: %s..." % summonerName
    summoner = w.get_summoner(name=summonerName)
    return summoner['id']


def get_unranked(summonerIds):
    print "Getting info for summonerID: %s..." % summonerIds
    summoners = w.get_summoners(names=None, ids=summonerIds)
    names = []
    for item in summoners.values():
        name = item.get('name')
        names.append(name)
    return names


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


def get_tier_division(summonerId):
    print "Getting league info for %s..." % summonerId
    leagues = w.get_league_entry([summonerId])
    return leagues


def parse_leagues(players, leagues):
    ranks = []
    unranked_ids = []
    for player in players:
        league = leagues.get(str(player[0]), 'Unranked')

        if league != 'Unranked':
            for item in league:
                if item.get('queue') == 'RANKED_SOLO_5x5':

                    if item.get('tier') != None:
                        tier = item.get('tier')
                    if item.get('entries') != None:

                        for thingy in item.get('entries'):
                            division = thingy.get('division')
                            name = thingy.get('playerOrTeamName')

            tier_division = [str(name), str(tier), str(division), player[1]]
            ranks.append(tier_division)
        else:
            unranked_ids.append(str(player[0]))

    if len(unranked_ids) != 0:
        unranked_names = get_unranked(unranked_ids)
        for name in unranked_names:
            tier_division = [name, 'Unranked', None, player[1]]
            ranks.append(tier_division)

    return ranks


# Formats everything all pretty like for chat
def prettyfy_ranks(ranks):
    stringy = '\nTeam 1:\n'
    for item in ranks:
        if item[3] == 100:
            if item[1] == 'Unranked':
                stringy += '\t%s: %s\n' % (item[0], item[1])
            else:
                stringy += '\t%s: %s %s\n' % (item[0], item[1], item[2])

    stringy += '\nTeam 2:\n'
    for item in ranks:
        if item[3] == 200:
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

    try:
        players = get_match_players(id)
    except riotwatcher.LoLException:
        return "Summoner is not in a game."

    players_list = ''
    for player in players:
        players_list += str(player[0]) + ','

    ranks = parse_leagues(players, get_tier_division(players_list))

    pretty_ranks = prettyfy_ranks(ranks)
    print "Done!"
    return pretty_ranks
