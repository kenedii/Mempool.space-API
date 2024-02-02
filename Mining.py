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
    def NetworkHashrate(timePeriod=''):
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

    @staticmethod
    def DifficultyAdjustments(interval='1m'):
        # Returns the record of difficulty adjustments over the specified trailing interval
        # Block timestamp, Block height,Difficulty, Difficulty change
        # If no time interval is specified, all available data is returned.
        response = requests.get(f'https://mempool.space/api/v1/mining/difficulty-adjustments/{interval}')
        json_data = MempoolAPI.validateResponse(response)
        adjustments = []
        for entry in range(len(json_data)):  # Iterate through the outer iterable
            diff = []
            for entry2 in range(len(json_data[entry])):  # Iterate through the inner iterables
                diff.append(json_data[entry][entry2])
            adjustments.append(diff)
        return adjustments

    @staticmethod
    def RewardStats(blockcount='100'):
        # Returns block reward and total transactions confirmed for the past blockCount blocks.
        response = requests.get(f'https://mempool.space/api/v1/mining/reward-stats/{blockcount}')
        json_data = MempoolAPI.validateResponse(response)
        info = {'startBlock': json_data['startBlock'],
                'endBlock': json_data['endBlock'],
                'totalReward': int(json_data['totalReward']),
                'totalFee': int(json_data['94202990908']),
                'totalTx': int(json_data['3866808']),
                }
        return info

    @staticmethod
    def BlockFees(timePeriod='24h'):
        # Returns average total fees for blocks in the specified :timePeriod, ordered oldest to newest.
        # timePeriod can be any of the following: 24h, 3d, 1w, 1m, 3m, 6m, 1y, 2y, 3y.
        # For 24h and 3d time periods, every block is included and fee amounts are exact (not averages).
        # For the 1w time period, fees may be averages depending on how fast blocks were found
        # around a particular timestamp. For other time periods, fees are averages.

        response = requests.get(f'https://mempool.space/api/v1/mining/blocks/fees/{timePeriod}')
        json_data = MempoolAPI.validateResponse(response)
        fees = []
        for block in range(len(json_data)):
            info = {'avgHeight': json_data[block]['avgHeight'],
                    'timestamp': json_data[block]['timestamp'],
                    'avgFees': json_data[block]['avgFees'],
                    'USD': json_data[block]['USD'],
                    }
            fees.append(info)
        return fees

    @staticmethod
    def BlockRewards(timePeriod='24h'):
        # Returns average block rewards for blocks in the specified timePeriod,
        # ordered oldest to newest. timePeriod can be any of the following: 24h, 3d, 1w, 1m, 3m, 6m, 1y, 2y, 3y.
        # For 24h and 3d time periods, every block is included and block rewards are exact (not averages).
        # For the 1w time period, block rewards may be averages depending on how fast blocks were found around a particular timestamp.
        # For other time periods, block rewards are averages.

        response = requests.get(f'https://mempool.space/api/v1/mining/blocks/rewards/{timePeriod}')
        json_data = MempoolAPI.validateResponse(response)
        rewards = []
        for block in range(len(json_data)):
            info = {'avgHeight': json_data[block]['avgHeight'],
                    'timestamp': json_data[block]['timestamp'],
                    'avgRewards': json_data[block]['avgRewards'],
                    'USD': json_data[block]['USD'],
                    }
            rewards.append(info)
        return rewards

    @staticmethod
    def BlockFeerates(timePeriod='24h'):
        # Returns average feerate percentiles for blocks in the specified timePeriod, ordered oldest to newest.
        # timePeriod can be any of the following: 24h, 3d, 1w, 1m, 3m, 6m, 1y, 2y, 3y.
        # For 24h and 3d time periods, every block is included and percentiles are exact (not averages).
        # For the 1w time period, percentiles may be averages depending on how fast blocks were found around a particular timestamp.
        # For other time periods, percentiles are averages.

        response = requests.get(f'https://mempool.space/api/v1/mining/blocks/fee-rates/{timePeriod}')
        json_data = MempoolAPI.validateResponse(response)
        feerates = []
        for block in range(len(json_data)):
            info = {'avgHeight': json_data[block]['avgHeight'],
                    'timestamp': json_data[block]['timestamp'],
                    'avgFee_0': json_data[block]['avgFee_0'],
                    'avgFee_10': json_data[block]['avgFee_10'],
                    'avgFee_25': json_data[block]['avgFee_25'],
                    'avgFee_50': json_data[block]['avgFee_50'],
                    'avgFee_75': json_data[block]['avgFee_75'],
                    'avgFee_90': json_data[block]['avgFee_90'],
                    'avgFee_100': json_data[block]['avgFee_100']}
            feerates.append(info)
        return feerates

    @staticmethod
    def BlockSizesWeights(timePeriod='24h'):
        # Returns array representing a block [[size, weight], [size, weight]]
        # Returns average size (bytes) and average weight (weight units) for blocks in the specified timePeriod, ordered oldest to newest.
        # timePeriod can be any of the following: 24h, 3d, 1w, 1m, 3m, 6m, 1y, 2y, 3y.
        # For 24h and 3d time periods, every block is included and figures are exact (not averages).
        # For the 1w time period, figures may be averages depending on how fast blocks were found around a particular timestamp.
        # For other time periods, figures are averages.

        response = requests.get(f'https://mempool.space/api/v1/mining/blocks/sizes-weights/{timePeriod}')
        json_data = MempoolAPI.validateResponse(response)
        blocks = []

        for block in range(len(json_data['sizes'])):
            size = {'avgHeight': json_data['sizes'][block]['avgHeight'],
                    'timestamp': json_data['sizes'][block]['timestamp'],
                    'avgSize': json_data['sizes'][block]['avgSize']}

            weight = {'avgHeight': json_data['weights'][block]['avgHeight'],
                      'timestamp': json_data['weights'][block]['timestamp'],
                      'avgWeight': json_data['weights'][block]['avgWeight']}

            blocks.append([size,weight])
        return blocks

    @staticmethod
    def BlockPredictions(timePeriod='24h'): # https://mempool.space/docs/api/rest#get-block-predictions
        response = requests.get(f'https://mempool.space/api/v1/mining/blocks/predictions/{timePeriod}')
        json_data = MempoolAPI.validateResponse(response)
        blocks = []
        for block in range(len(json_data)):
            blocks.append([json_data[block][0],json_data[block][1],json_data[block][2]])
        return blocks

    @staticmethod
    def BlockAuditScore(blockHash): # https://mempool.space/docs/api/rest#get-block-audit-score
        # Returns: hash, matchrate, expectedfees and expectedweight for a block
        response = requests.get(f'https://mempool.space/api/v1/mining/blocks/audit/score/{blockHash}')
        json_data = MempoolAPI.validateResponse(response)
        return [json_data['hash'], json_data['matchRate'], json_data['expectedFees'], json_data['expectedWeight']]

    @staticmethod
    def AuditScores(startHeight):  # https://mempool.space/docs/api/rest#get-block-audit-score
        response = requests.get(f'https://mempool.space/api/v1/mining/blocks/audit/scores/{startHeight}')
        json_data = MempoolAPI.validateResponse(response)
        scores=[]
        for i in range(len(json_data)):
            scores.append([json_data[i]['hash'], json_data[i]['matchRate'], json_data[i]['expectedFees'], json_data[i]['expectedWeight']])
        return scores

    @staticmethod
    def AuditSummary(blockHash): # https://mempool.space/docs/api/rest#get-block-audit-summary
        response = requests.get(f'https://mempool.space/api/v1/block/{blockHash}/audit-summary')
        json_data = MempoolAPI.validateResponse(response)
        summary = {'height' : json_data['height'],
                   'id' : json_data['height'],
                   'timestamp' : json_data['height'],
                   'missingTxs' : json_data['height'],
                   'freshTxs' : json_data['height'],
                   'sigopTxs' : json_data['height'],
                   'fullrbfTxs' : json_data['height'],
                   'acceleratedTxs' : json_data['acceleratedTxs'],
                   'matchRate' : json_data['matchRate'],
                   'expectedFees' : json_data['expectedFees'],
                   'expectedWeight' : json_data['expectedWeight'],}
        template = []
        for i in range(len(json_data['template'])):
            tx = {'txid' : json_data['template'][i]['txid'],
                  'fee' : json_data['template'][i]['fee'],
                  'vsize' : json_data['template'][i]['vsize'],
                  'value' : json_data['template'][i]['value'],
                  'rate' : json_data['template'][i]['rate'],
                  'flags' : json_data['template'][i]['flags']}
            template.append(tx)
        summary['template'].append(template)

        txCategories = ['missingTxs', 'addedTxs', 'freshTxs', 'sigopTxs', 'fullrbfTxs', 'acceleratedTxs']
        for i in range(6):
            transactions = []
            for tx in range(len(json_data[txCategories[i]])):
                transactions.append(tx)
            summary[txCategories[i]] = transactions

        return summary
