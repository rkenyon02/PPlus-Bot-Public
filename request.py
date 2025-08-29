import requests

def getPlayerData(netPlayName):
    # Headers for Slippi API request
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'apollographql-client-name': 'slippi-web',
        'content-type': 'application/json',
        'origin': 'https://slippi.gg',
        'priority': 'u=1, i',
        'referer': 'https://slippi.gg/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    # API Query json
    json_data = {
        'operationName': 'UserProfilePageQuery',
        'variables': {
            'cc': netPlayName,
            'uid': netPlayName,
        },
        'query': "fragment profileFields on NetplayProfile {\n  id\n  ratingOrdinal\n  ratingUpdateCount\n  wins\n  losses\n  dailyGlobalPlacement\n  dailyRegionalPlacement\n  continent\n  characters {\n    character\n    gameCount\n    __typename\n  }\n  __typename\n}\n\nfragment userProfilePage on User {\n  fbUid\n  displayName\n  connectCode {\n    code\n    __typename\n  }\n  status\n  activeSubscription {\n    level\n    hasGiftSub\n    __typename\n  }\n  rankedNetplayProfile {\n    ...profileFields\n    __typename\n  }\n  rankedNetplayProfileHistory {\n    ...profileFields\n    season {\n      id\n      startedAt\n      endedAt\n      name\n      status\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nquery UserProfilePageQuery($cc: String, $uid: String) {\n  getUser(fbUid: $uid, connectCode: $cc) {\n    ...userProfilePage\n    __typename\n  }\n}\n"
    }

    # Post requests to Slippi API with headers and json data
    response = requests.post('https://internal.slippi.gg/graphql', headers=headers, json=json_data)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        json_response = response.json()
        if json_response['data']['getUser'] == None:
            return None
        playerData = [
            json_response['data']['getUser']['connectCode']['code'],
            str(json_response['data']['getUser']['rankedNetplayProfile']['ratingOrdinal']),
            str(json_response['data']['getUser']['rankedNetplayProfile']['ratingUpdateCount']),
            str(json_response['data']['getUser']['rankedNetplayProfile']['wins']),
            str(json_response['data']['getUser']['rankedNetplayProfile']['losses']),
            json_response['data']['getUser']['displayName']
        ]
        return playerData
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)  # Print the response content for debugging
        return None