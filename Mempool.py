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
    def extract_replacements(tx_data): # used by other Replacements methods, not meant to be called directly
        replacements = []

        for tx in tx_data:
            tx_info = {  
                'txid': tx.get('txid', ''),
                'fee': tx.get('fee', 0),
                'vsize': tx.get('vsize', 0),
                'value': tx.get('value', 0),
                'rate': tx.get('rate', 0),
                'rbf': tx.get('rbf', False),
                'time': tx.get('time', 0),
                'fullRbf': tx.get('fullRbf', False),
            }

            replaces = tx.get('replaces', [])
            if replaces:
                tx_info['replaces'] = replaces
                replacements.extend(Mempool.extract_replacements(replaces))

            replacements.append(tx_info)

        return replacements
    
    @staticmethod
    def Replacements():
        response = requests.get('https://mempool.space/api/v1/replacements')
        json_data = MempoolAPI.validateResponse(response)

        return Mempool.extract_replacements(json_data)
    
    @staticmethod
    def FullRBF(): # https://mempool.space/docs/api/rest#get-mempool-fullrbf
        response = requests.get('https://mempool.space/api/v1/fullrbf/replacements')
        json_data = MempoolAPI.validateResponse(response)

        return Mempool.extract_replacements(json_data)