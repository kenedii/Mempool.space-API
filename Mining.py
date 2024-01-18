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

    @staticmethod
    def Hashrates(timePeriod=''):
        # Returns average hashrates (and share of total hashrate) of mining pools active in
        # the specified trailing timePeriod, in descending order of hashrate.
        # Leave :timePeriod unspecified to get all available data,
        # or specify any of the following time periods: 1m, 3m, 6m, 1y, 2y, 3y.

        response = requests.get(f'https://mempool.space/api/v1/mining/hashrate/pools/{timePeriod}')
        json_data = MempoolAPI.validateResponse(response)
        pools = []  # Initialize the array of pool hashrates
        for pool in range(len(json_data)):
            info = {'timestamp': json_data[pool]['timestamp'],
                    'avgHashrate': json_data[pool]['avgHashrate'],
                    'share': json_data[pool]['share'],
                    'poolName': json_data[pool]['poolName']}
            pools.append(info)
        return pools

    @staticmethod
    def Hashrate(slug):
        # Returns all known hashrate data for the mining pool specified by slug.
        # Hashrate values are weekly averages.

        response = requests.get(f'https://mempool.space/api/v1/mining/pool/{slug}/hashrate')
        json_data = MempoolAPI.validateResponse(response)
        pools = []  # Initialize the array of hashrates
        for hashrate in range(len(json_data)):
            info = {'timestamp': json_data[hashrate]['timestamp'],
                    'avgHashrate': json_data[hashrate]['avgHashrate'],
                    'share': json_data[hashrate]['share'],
                    'poolName': json_data[hashrate]['poolName']}
            pools.append(info)
        return pools

    @staticmethod
    def PoolBlock(slug, blockheight=''):
        # Returns past 10 blocks mined by the specified mining pool (slug) before the
        # specified blockHeight. If no blockHeight is specified, the mining
        # pool's 10 most recent blocks are returned.

        response = requests.get(f'https://mempool.space/api/v1/mining/pool/{slug}/blocks/{blockheight}')
        json_data = MempoolAPI.validateResponse(response)
        blocks = []
        for blockPosition in range(len(json_data)):  # Iterate through blocks
            info = {'id': json_data[blockPosition]['id'],
                    'height': json_data[blockPosition]['height'],
                    'version': json_data[blockPosition]['version'],
                    'timestamp': json_data[blockPosition]['timestamp'],
                    'bits': json_data[blockPosition]['bits'],
                    'nonce': json_data[blockPosition]['nonce'],
                    'difficulty': json_data[blockPosition]['difficulty'],
                    'merkle_root': json_data[blockPosition]['merkle_root'],
                    'tx_count': json_data[blockPosition]['tx_count'],
                    'size': json_data[blockPosition]['size'],
                    'weight': json_data[blockPosition]['weight'],
                    'previousblockhash': json_data[blockPosition]['previousblockhash'],
                    'mediantime': json_data[blockPosition]['mediantime'],
                    'totalFees': json_data[blockPosition]['extras']['totalFees'],
                    'medianFee': json_data[blockPosition]['extras']['medianFee'],
                    'reward': json_data[blockPosition]['extras']['reward'],
                    'avgFee': json_data[blockPosition]['extras']['avgFee'],
                    'avgFeeRate': json_data[blockPosition]['extras']['avgFeeRate'],
                    'coinbaseRaw': json_data[blockPosition]['extras']['coinbaseRaw'],
                    'coinbaseAddress': json_data[blockPosition]['extras']['coinbaseAddress'],
                    'coinbaseSignature': json_data[blockPosition]['extras']['coinbaseSignature'],
                    'coinbaseSignatureAscii': json_data[blockPosition]['extras']['coinbaseSignatureAscii'],
                    'avgTxSize': json_data[blockPosition]['extras']['avgTxSize'],
                    'totalInputs': json_data[blockPosition]['extras']['totalInputs'],
                    'totalOutputs': json_data[blockPosition]['extras']['totalOutputs'],
                    'totalOutputAmt': json_data[blockPosition]['extras']['totalOutputAmt'],
                    'medianFeeAmt': json_data[blockPosition]['extras']['medianFeeAmt'],
                    'segwitTotalTxs': json_data[blockPosition]['extras']['segwitTotalTxs'],
                    'segwitTotalSize': json_data[blockPosition]['extras']['segwitTotalSize'],
                    'segwitTotalWeight': json_data[blockPosition]['extras']['segwitTotalWeight'],
                    'header': json_data[blockPosition]['extras']['header'],
                    'utxoSetChange': json_data[blockPosition]['extras']['utxoSetChange'],
                    'utxoSetSize': json_data[blockPosition]['extras']['utxoSetSize'],
                    'totalInputAmt': json_data[blockPosition]['extras']['totalInputAmt'],
                    'virtualSize': json_data[blockPosition]['extras']['virtualSize'],
                    'orphans': json_data[blockPosition]['extras']['orphans'],
                    'matchRate': json_data[blockPosition]['extras']['matchRate'],
                    'expectedFees': json_data[blockPosition]['extras']['expectedFees'],
                    'expectedWeight': json_data[blockPosition]['extras']['expectedWeight'],
                    }
            feeRanges = []
            for feeRange in range(len(json_data[blockPosition]['extras']['feeRange'])):
                feeRanges.append(json_data[blockPosition]['extras']['feeRange'][feeRange])
            info['feeRange'] = feeRanges
            feePercentiles = []
            for feePercentile in range(len(json_data[blockPosition]['extras']['feePercentiles'])):
                feePercentiles.append(json_data[blockPosition]['extras']['feePercentiles'][feePercentile])
            info['feePercentiles'] = feePercentiles
            pool = {'id': json_data[blockPosition]['extras']['pool']['id'],
                    'name': json_data[blockPosition]['extras']['pool']['name'],
                    'slug': json_data[blockPosition]['extras']['pool']['slug']}
            info['pool'] = pool
        blocks.append(info)
        return blocks

    @staticmethod
    def NetworkHashrate(timeperiod=''):
        # Returns network-wide hashrate and difficulty figures over the specified trailing timePeriod
        # -Current (real-time) hashrate, -Current (real-time) difficulty,
        # -Historical daily average hashrates, -Historical difficulty
        # Valid values for :timePeriod are 1m, 3m, 6m, 1y, 2y, 3y. If no time interval is specified, all available data is returned.
        response = requests.get(f'https://mempool.space/api/v1/mining/hashrate/{timeperiod}')
        json_data = MempoolAPI.validateResponse(response)
        info = {'difficulty': json_data['difficulty'],
                'currentHashrate': json_data['currentHashrate'],
                'currentDifficulty': json_data['currentDifficulty'],
                }
        hashrates = []
        for hashrate in range(len(json_data['hashrates'])):
            rates = {'timestamp': json_data['hashrates'][hashrate]['timestamp'],
                     'avgHashrate': json_data['hashrates'][hashrate]['avgHashrate']}
            hashrates.append(rates)
        info['hashrates'] = hashrates
        return info
