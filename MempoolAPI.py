import requests


class MempoolAPI:
    @staticmethod
    def validateResponse(response):  # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON data from the response
            json_data = response.json()
            return json_data
        else:  # If error getting json data
            raise Exception('Error retrieving json data. Invalid Parameters or API Endpoint is down.')

    @staticmethod
    def inputOutputBuilder(json_data):  # Constructs input and output dictionaries. Used by several functions
        vin = {}  # Initialize the dictionary of inputs
        vout = {}  # Initialize the dictionary of outputs
        for i in range(len(json_data['vin'])):
            vin[str(json_data['vin'][i])] = {'txid': json_data['vin'][i]['txid'],
                                             'vout': json_data['vin'][i]['vout'],
                                             'prevout': json_data['vin'][i]['prevout'],
                                             'scriptsig': json_data['vin'][i]['scriptsig'],
                                             'scriptsig_asm': json_data['vin'][i]['scriptsig_asm'],
                                             'is_coinbase': json_data['vin'][i]['is_coinbase'],
                                             'sequence': json_data['vin'][i]['sequence'],

                                             }
        for i in range(len(json_data['vout'])):
            vout[str(json_data['vout'][i])] = {'scriptpubkey': json_data['vout'][i]['scriptpubkey'],
                                               'scriptpubkey_asm': json_data['vout'][i]['scriptpubkey_asm'],
                                               'scriptpubkey_type': json_data['vout'][i]['scriptpubkey_type'],
                                               'value': json_data['vout'][i]['value']
                                               }
            if json_data['vout'][i]['scriptpubkey_type'] != 'op_return':
                vout[str(json_data['vout'][i])]['scriptpubkey_address'] = json_data['vout'][i]['scriptpubkey_address']
        return vin, vout

    @staticmethod
    def DifficultyAdjustment():  # Returns details about difficulty adjustment.
        response = requests.get("https://mempool.space/api/v1/difficulty-adjustment")
        json_data = MempoolAPI.validateResponse(response)

        info = {'progressPercent': json_data['progressPercent'],
                'difficultyChange': json_data['difficultyChange'],
                'estimatedRetargetDate': json_data['estimatedRetargetDate'],
                'remainingBlocks': json_data['remainingBlocks'],
                'remainingTime': json_data['remainingTime'],
                'previousRetarget': json_data['previousRetarget'],
                'nextRetargetHeight': json_data['nextRetargetHeight'],
                'timeAvg': json_data['timeAvg'],
                'timeOffset': json_data['timeOffset'],
                }

        return info

    @staticmethod
    def Price():  # Returns bitcoin latest price denominated in main currencies.
        response = requests.get("https://mempool.space/api/v1/prices")
        json_data = MempoolAPI.validateResponse(response)

        info = {'time': json_data['time'],
                'USD': json_data['USD'],
                'EUR': json_data['EUR'],
                'GBP': json_data['GBP'],
                'CAD': json_data['CAD'],
                'CHF': json_data['CHF'],
                'AUD': json_data['AUD'],
                'JPY': json_data['JPY']
                }

        return info

    @staticmethod
    def RecommendedFees(): # Returns Mempool.space's currently suggested fees for new transactions.
        response = requests.get("https://mempool.space/api/v1/fees/recommended")
        json_data = MempoolAPI.validateResponse(response)
        info = {'fastestFee': json_data['fastestFee'],
                'halfHourFee': json_data['halfHourFee'],
                'hourFee': json_data['hourFee'],
                'economyFee': json_data['economyFee'],
                'minimumFee': json_data['minimumFee']
                }

        return info

    @staticmethod
    def MempoolBlocksFees(): # Returns current mempool as projected blocks.
        response = requests.get("https://mempool.space/api/v1/fees/mempool-blocks")
        json_data = MempoolAPI.validateResponse(response)
        blocks = [] # Initialize the array containing projected blocks
        for blok in range(len(json_data)): # Iterate through all the blocks
            block = {'blockSize': json_data[blok]['blockSize'],
                     'blockVSize': json_data[blok]['blockVSize'],
                     'nTx': json_data[blok]['nTx'],
                     'totalFees': json_data[blok]['totalFees'],
                     'medianFee': json_data[blok]['medianFee'],
                     }
            feeRange = [] # Initialize the array containing fee Ranges
            for fr in range(len(json_data[blok]['feeRange'])): # Iterate through all the fee ranges
                feeRange.append(json_data[blok]['feeRange'][fr])
            block['feeRange'] = feeRange
            blocks.append(block)
        return blocks




