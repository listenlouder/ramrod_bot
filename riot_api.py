import riotwatcher
from riotwatcher import RiotWatcher

w = RiotWatcher('api-key')


def get_summonerId_from_name(summonerName):
    summoner = w.get_summoner(name=summonerName)
    return summoner['id']


def get_summoner_name_from_id(summonerId):
    summoner = w.get_summoner(name=None, _id=summonerId)
    name = summoner.get('name')
    return name


def get_match_players(summonerId):
    current_match = w.get_current_game(summonerId)
    players = []
    for item in current_match['participants']:
        if item.get('summonerId') != None:
            players.append(item.get('summonerId'))
    return players


def get_tier_division(summonerId):
    try:
        league = w.get_league_entry([summonerId]) #TODO: 404 = Unranked. Catch dat error
        temp = league[str(summonerId)]
        for item in temp:
            if item.get('queue') == 'RANKED_SOLO_5x5':
                if item.get('tier') != None:
                    tier = item.get('tier')
                if item.get('entries') != None:
                    for thingy in item.get('entries'):
                        division = thingy.get('division')
                        name = thingy.get('playerOrTeamName')
            tier_division = [str(name), str(tier), str(division)]

    except riotwatcher.LoLException:
        tier_division = [get_summoner_name_from_id(summonerId), 'Unranked']

    return tier_division


def get_match_ranks(summonerName):
    id = get_summonerId_from_name(summonerName)
    players = get_match_players(id)

    ranks = []
    for player in players:
        temp = get_tier_division(player)
        ranks.append(temp)
    pretty_ranks = prettyfy_ranks(ranks)
    return pretty_ranks


def prettyfy_ranks(ranks):
    stringy = '\n'
    for item in ranks:
        if item[1] == 'Unranked':
            stringy += '\t%s: %s\n' % (item[0], item[1])
        else:
            stringy += '\t%s: %s %s\n' % (item[0], item[1], item[2])
    return stringy
