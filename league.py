#!/usr/bin/env python
import os
import requests
import constants
import sys
import time
import dynamo

def get_account_id(name):
    player_json = requests.get(constants.URLS['NAME_TO_ID'].format(name=name), headers=constants.HEADERS).json()
    try:
        return_value = player_json['accountId']
    except:
        return_value = 'Bad "name" error.'
    return return_value

def get_summoner_id(account_id):
    player_json = requests.get(constants.URLS['ID_TO_NAME'].format(id=account_id), headers=constants.HEADERS).json()
    try:
        return_value = player_json['id']
    except:
        return_value = 'Bad "accountId" error.'
    return return_value

def get_name(account_id):
    player_json = requests.get(constants.URLS['ID_TO_NAME'].format(id=account_id), headers=constants.HEADERS).json()
    try:
        return_value = player_json['name']
    except:
        return_value = 'Bad "accountId" error.'
    return return_value

def get_matches(account_id):
    r = requests.get(constants.URLS['MATCHES_BY_ID'].format(id=account_id), headers=constants.HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        return 'Bad request error. Error code: {}'.format(r.status_code)

def get_recent_ten(account_id):
    summoner_id = get_summoner_id(account_id)
    r = requests.get(constants.URLS['RECENT_TEN'].format(summonerId=summoner_id), headers=constants.HEADERS)
    if r.status_code == 200:
        return r.json()['games']
    else:
        return 'Bad request error. Error code: {}'.format(r.status_code)

def get_twenty_normals(account_id):
    r = requests.get(constants.URLS['RECENT_MATCHES_BY_ID'].format(id=account_id), headers=constants.HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        return 'Bad request error. Error code: {}'.format(r.status_code)
    
def champ_histogram(matches):
    champ_hist = {}
    for i in matches['matches']:
        champ = constants.CHAMP_BY_ID['data'][str(i['champion'])]['name']
        if champ not in champ_hist.keys():
            champ_hist[champ] = 1
        else:
            champ_hist[champ] += 1
    return champ_hist


def interesting_info(histogram):
    total_champs = len(histogram.keys())
    total_games = sum(histogram.values())
    average_games = total_games/total_champs
    print('{:<35}: {:<10}'.format('Total Champion Played', total_champs))
    print('{:<35}: {:<10}'.format('Total Games', total_games))
    print('{:<35}: {:<10}'.format('Average Games Per Champ', average_games)) 
    sorted_list = sorted(histogram, key=histogram.get, reverse=True)
    top_five = sorted_list[:5]
    bottom_five = sorted_list[-5:]
    for i in top_five:
        print('{:<35}: {:<10}'.format(i, histogram[i]))
    for i in bottom_five:
        print('{:<35}: {:<10}'.format(i, histogram[i]))    

def main(args):
    if not args[1:]:
        print('0 name arguments')
    else:
        for i in args[1:]:
            name = i
            print('{:<35}: {:<10}'.format('Player', get_name(get_account_id(name))))
            x = get_matches(get_account_id(name))
            y = champ_histogram(x)
            interesting_info(y)
            print('---------------------------------------------')
            time.sleep(5)

    tester = dynamo.DynamoMatches()
    matches = get_recent_ten(get_account_id('bluelldragon'))
    acc_id = str(get_account_id('bluelldragon'))
    for i in matches:
        if i['subType'] == 'NORMAL':
            tester.add_match(acc_id, str(i['gameId']), i)


if __name__ == '__main__':
    main(sys.argv)


