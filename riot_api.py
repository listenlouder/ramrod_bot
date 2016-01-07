import riotwatcher
from riotwatcher import RiotWatcher
import json
from random import randint

w = RiotWatcher('api_key')

# Static champion data from riot.
with open('Resources/champions.json') as data_file:
    Champs = json.load(data_file)


def get_summonerId_from_name(summonerName):
    print "Getting info for summonerName: %s..." % summonerName
    summoner = w.get_summoner(name=summonerName)
    return summoner['id']


def get_champion(champ_id, champ_data):
    champion = ''
    for key, value in champ_data['data'].iteritems():
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
            champ_name = get_champion(champId, Champs)
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

######################################################################
# Start of Ultimate Bravery
######################################################################

# structure: {player_name: { champ: 'champ', masteries: [masteries], spells: [spells], items: [items]}

with open('Resources/items.json') as data_file2:
    Items = json.load(data_file2)

with open('Resources/summoner_spells.json') as data_file3:
    Spells = json.load(data_file3)


def rand_champ(champ_data):
    champ_list = champ_data['data']
    names = []
    for key, value in champ_list.iteritems():
        name = value.get('name')
        names.append(name)

    play_champ = names[randint(0,len(names)-1)]
    return play_champ


def rand_masteries():
    temp1 = randint(0,18)
    temp2 = randint(0,18)
    temp3 = randint(0,18)
    masteries = [str(temp1), str(temp2), str(temp3)]
    if temp1 + temp2 + temp3 == 30:
        return masteries
    else:
        return rand_masteries()


def rand_spells(spells, map_id):
    if map_id == 12:
        game_mode = 'ARAM'
    elif map_id == 8:
        game_mode = 'ODIN'
    elif map_id == 10 or map_id == 11:
        game_mode = 'CLASSIC'
    else:
        print "ERROR: invalid map_id: %s" % map_id
        raise ValueError

    sum_spells = []
    list_spells = []
    for key, value in spells['data'].iteritems():
        name = value.get('name')
        modes = value.get('modes')
        if game_mode in modes:
            list_spells.append(name)

    while len(sum_spells) < 2:
        temp = randint(0,len(list_spells)-1)
        if list_spells[temp] not in sum_spells:
            sum_spells.append(list_spells[temp])

    return sum_spells


def is_boot(value):
    if value.get('tags') is not None and 'Boots' in value.get('tags') and value.get('name') is not 'Boots of Speed':
        return True
    else:
        return False


def is_enchant(value):
    if value.get('group') is not None and value.get('group').startswith('Boots'):
        return True
    else:
        return False


def is_valid_item(value):
    if not is_boot(value) and not is_enchant(value):
        if value.get('into') is None and value.get('consumed') is None and value.get('requiredChampion') is None:
            if value.get('tags') is not None and 'Lane' not in value.get('tags') and 'Jungle' not in value.get('tags') \
                    and 'Consumable' not in value.get('tags') and 'Trinket' not in value.get('tags'):
                return True
            else:
                return False


def get_boots(item_list, map_id):
    boots_list = []
    enchants_list = []

    for key, value in item_list['data'].iteritems():
        if value.get('maps').get(str(map_id)):
            if is_boot(value):
                boots_list.append(value.get('name'))
            elif is_enchant(value):
                enchants_list.append(value.get('name'))

    boots = [boots_list[randint(0,len(boots_list)-1)], enchants_list[randint(0,len(enchants_list)-1)]]
    return boots


def create_build(item_list, map_id):
    champ = rand_champ(Champs)
    sum_spells = rand_spells(Spells,map_id)
    masteries = rand_masteries()
    boots = get_boots(item_list, map_id)
    items_list = []

    for key, value in item_list['data'].iteritems():
        if value.get('maps').get(str(map_id)):
            if is_valid_item(value):
                items_list.append(value.get('name'))

    build_items = [boots]
    while len(build_items) < 6:
        item = items_list[randint(0,len(items_list)-1)]
        if item not in build_items:
            build_items.append(item)

    bravery_build = {'champ': champ, 'masteries': masteries, 'sum_spells': sum_spells, 'build': build_items}
    return bravery_build


def ultimate_bravery(map_id):
    build = create_build(Items, map_id)
    champ = build.get('champ')
    masteries = '%s, %s, %s' % (build.get('masteries')[0], build.get('masteries')[1], build.get('masteries')[2])
    sum_spells = '%s / %s' % (build.get('sum_spells')[0], build.get('sum_spells')[1])
    pretty_items = '%s - %s, %s, %s, %s, %s, %s' % \
                   (build.get('build')[0][0], build.get('build')[0][1], build.get('build')[1], build.get('build')[2],
                    build.get('build')[3], build.get('build')[4], build.get('build')[5],)
    abilities = ['Q', 'W', 'E']

    bravery = '%s (%s / max %s) (%s)\nBuild Order: %s' % \
             (champ, sum_spells, abilities[randint(0,2)], masteries, pretty_items)

    return bravery
