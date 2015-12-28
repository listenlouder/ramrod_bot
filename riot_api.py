import riotwatcher
from riotwatcher import RiotWatcher

w = RiotWatcher('api_key')


def get_summonerId_from_name(summonerName):
    print "Getting info for summonerName: %s..." % summonerName
    summoner = w.get_summoner(name=summonerName)
    return summoner['id']


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
                            sid = thingy.get('playerOrTeamId')

            tier_division = [str(sid), str(name), str(tier), str(division)]
            ranks.append(tier_division)

    return ranks


def prettyfy_ranks(player_list):
    stringy = '\nTeam 1:\n'
    for key,value in player_list.iteritems():
        if value['team'] == 100:
            if value['tier'] == 'UNRANKED':
                stringy += '\t%s: %s\n' % (value['name'], value['tier'])
            else:
                stringy += '\t%s: %s %s\n' % (value['name'], value['tier'], value['division'])

    stringy += '\nTeam 2:\n'
    for key,value in player_list.iteritems():
        if value['team'] == 200:
            if value['tier'] == 'UNRANKED':
                stringy += '\t%s: %s\n' % (value['name'], value['tier'])
            else:
                stringy += '\t%s: %s %s\n' % (value['name'], value['tier'], value['division'])

    return stringy


def get_match_ranks(summonerName):
    player_list = {}

    try:
        print "Getting match info for %s..." % summonerName
        sid = get_summonerId_from_name(summonerName)
    except riotwatcher.LoLException:
        return "No summoner found with name: "

    try:
        players = get_match_players(sid)
    except riotwatcher.LoLException:
        return "Summoner is not in a game."

    for player in players:
        player_list[str(player[0])] = {'name': None, 'tier': 'UNRANKED', 'division': None, 'team': player[1]}

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
