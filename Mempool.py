from MempoolAPI import MempoolAPI
import requests
import os
import urllib.request

class Mempool(MempoolAPI):

    @staticmethod
    def Mempool():
        response = requests.get(f'https://mempool.space/api/mempool')
        json_data = MempoolAPI.validateResponse(response)

        info = {'count': json_data['count'],
                'vsize': json_data['vsize'],
                'total_fee': json_data['total_fee']
                }
        
        fee_histogram = []
        for fee in range(len(json_data['fee_histogram'])):
            fee_histogram.append([json_data['fee_histogram'][fee][0],
                                json_data['fee_histogram'][fee][1]])
            
        info['fee_histogram'] = fee_histogram

        return info

    @staticmethod
    def Txids():
        response = requests.get(f'https://mempool.space/api/mempool/txids')
        json_data = MempoolAPI.validateResponse(response)
        transactions = []  # Initialize the tx array
        for tx in range(len(json_data)):
            transactions.append(tx)
        return transactions
    
    @staticmethod
    def Recent():
        response = requests.get(f'https://mempool.space/api/mempool/recent')
        json_data = MempoolAPI.validateResponse(response)
        recent = []

        for tx in range(len(json_data)):
            tx = [json_data[tx]['txid'], json_data[tx]['fee'], json_data[tx]['vsize'], json_data[tx]['value']]
            recent.append(tx)
        return recent
    
    @staticmethod
    def Replacements():
        response = requests.get(f'https://mempool.space/api/mempool/replacements')
        json_data = MempoolAPI.validateResponse(response)
        replacements = []
        replaces = []

        for tx in range(len(json_data)):
            tx = [json_data[tx]['tx']['txid'], json_data[tx]['tx']['fee'], json_data[tx]['tx']['vsize'], json_data[tx]['tx']['value'], json_data[tx]['tx']['rate'], json_data[tx]['tx']['rbf'], json_data[tx]['tx']['fullRbf'], json_data[tx]['time'], json_data[tx]['fullRbf']]

            for replace in range(len(json_data['replaces'])):
                replace = [json_data[tx]['replaces'][replace]['txid'], json_data[tx]['replaces'][replace]['fee'], json_data[tx]['replaces'][replace]['vsize'], json_data[tx]['replaces'][replace]['value'], json_data[tx]['replaces'][replace]['rate'], json_data[tx]['replaces'][replace]['rbf'], json_data[tx]['replaces'][replace]['time'], json_data[tx]['replaces'][replace]['interval'], json_data[tx]['replaces'][replace]['fullRbf'], json_data[tx]['replaces'][replace]['replaces']]
                tx.append(replace)
            replacements.append(tx)


        return replacements