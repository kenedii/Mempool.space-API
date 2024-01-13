import requests

class MempoolAPI:

    def validateResponse(response): # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON data from the response
            json_data = response.json()
        else:  # If error getting json data
            raise Exception('Error retrieving json data. Invalid Parameters or API Endpoint is down.')

    def inputoutputBuilder(self, json_data): # Constructs input and output dictionaries. Used by several functions
        vin = {}  # Initialize the dictionary of inputs
        vout = {}  # Initialize the dictionary of outputs
        for i in range(len(json_data['vin'])):
            vin[json_data['vin'][i]] = {'txid': json_data['vin'][i]['txid'],
                                            'vout': json_data['vin'][i]['vout'],
                                            'prevout': json_data['vin'][i]['prevout'],
                                            'scriptsig': json_data['vin'][i]['scriptsig'],
                                            'scriptsig_asm': json_data['vin'][i]['scriptsig_asm'],
                                            'is_coinbase': json_data['vin'][i]['is_coinbase'],
                                            'sequence': json_data['vin'][i]['sequence'],

                                            }
        for i in range(len(json_data['vout'])):
            vin[json_data['vout'][i]] = {'scriptpubkey': json_data['vin'][i]['scriptpubkey'],
                                             'scriptpubkey_asm': json_data['vin'][i]['scriptpubkey_asm'],
                                             'scriptpubkey_type': json_data['vin'][i]['scriptpubkey_type'],
                                             'scriptpubkey_address': json_data['vin'][i][
                                                 'scriptpubkey_address'],
                                             'value': json_data['vin'][i]['value']

                                             }
        return vin, vout

    def DifficultyAdjustment(self):  # Returns details about difficulty adjustment.
        response = requests.get("https://mempool.space/api/v1/difficulty-adjustment")
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)

        info = {'progressPercent': json_data['progressPercent'],
                'difficultyChange': json_data['difficultyChange'],
                'estimatedRetargetDate': json_data['n_tx'],
                'remainingBlocks': json_data['final_balance'],
                'remainingTime': json_data['remainingTime'],
                'previousRetarget': json_data['previousRetarget'],
                'nextRetargetHeight': json_data['nextRetargetHeight'],
                'timeAvg': json_data['timeAvg'],
                'timeOffset': json_data['timeOffset'],
                }

        return info

    def Price(self):  # Returns bitcoin latest price denominated in main currencies.
        response = requests.get("https://mempool.space/api/v1/prices")
        # Check if the request was successful (status code 200)
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