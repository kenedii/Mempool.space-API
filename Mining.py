from MempoolAPI import MempoolAPI
import requests
import os
import urllib.request


class Mining:

    @staticmethod
    def Pools(timePeriod=''):
        # Returns a list of all known mining pools ordered by blocks found over the specified trailing timePeriod.
        # Leave timePeriod unspecified to get all available data,
        # or specify one of the following values: 24h, 3d, 1w, 1m, 3m, 6m, 1y, 2y, 3y.

        response = requests.get(f'https://mempool.space/api/v1/mining/pools/{timePeriod}')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        pools = {'blockCount': json_data['blockCount'],
                 'lastEstimatedHashrate': json_data['lastEstimatedHashrate']}
        for pool in range(len(json_data) - 2):
            info = {'poolId': json_data[pool]['poolId'],
                    'name': json_data[pool]['name'],
                    'link': json_data[pool]['link'],
                    'blockCount': json_data[pool]['blockCount'],
                    'rank': json_data[pool]['rank'],
                    'emptyBlocks': json_data[pool]['emptyBlocks'],
                    'slug': json_data[pool]['slug'],
                    'avgMatchRate': json_data[pool]['avgMatchRate'],
                    'avgFeeDelta': json_data[pool]['avgFeeDelta'],
                    'poolUniqueId': json_data[pool]['poolUniqueId']
                    }
            pools[str(json_data[pool]['slug'])] = info

        return pools

    @staticmethod
    def Pool(slug):  # Returns details about the mining pool specified by slug.
        response = requests.get(f'https://mempool.space/api/v1/mining/pool/{slug}')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        info = {'id': json_data['pool']['id'],
                'name': json_data['pool']['name'],
                'slug': json_data['pool']['slug'],
                'unique_id': json_data['pool']['unique_id'],
                'estimatedHashrate': json_data['estimatedHashrate'],
                'reportedHashrate': json_data['reportedHashrate'],
                'avgBlockHealth': json_data['avgBlockHealth'],
                'totalReward': json_data['totalReward'],
                'link': json_data['pool']['link'],
                }
        addresses = []  # Initialize the array to store addresses in
        regexes = []  # Initialize the array to store regexes in
        blockCount = []  # Initialize the array to store blockCount in
        blockShare = []  # Initialize the array to store blockShare in
        for address in range(len(json_data['pool']['addresses'])):
            addresses.append(json_data['pool']['addresses'][address])
        for regex in range(len(json_data['pool']['regexes'])):
            regexes.append(json_data['pool']['regexes'][regex])
        for block in json_data['blockCount']:
            regexes.append(json_data['blockCount'][block])
        for block in json_data['blockShare']:
            regexes.append(json_data['blockCount'][block])
        info['addresses'] = addresses
        info['regexes'] = regexes
        info['blockCount'] = blockCount
        info['blockShare'] = blockShare
        return info
