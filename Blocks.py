from MempoolAPI import MempoolAPI
import requests
import os
import urllib.request

class Block:
    @staticmethod
    def Block(hash):  # Returns details about a block.
        response = requests.get(f'https://mempool.space/api/block/{hash}')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)

        info = {'id': json_data['id'],
                'height': json_data['height'],
                'version': json_data['version'],
                'timestamp': json_data['timestamp'],
                'size': json_data['size'],
                'weight': json_data['weight'],
                'merkle_root': json_data['merkle_root'],
                'previousblockhash': json_data['previousblockhash'],
                'mediantime': json_data['mediantime'],
                'nonce': json_data['nonce'],
                'bits': json_data['bits'],
                'difficulty': json_data['difficulty'],
                }

        return info

    @staticmethod
    def Header(hash):  # Returns the hex-encoded block header.
        response = requests.get(f'https://mempool.space/api/block/{hash}/header')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        return json_data

    @staticmethod
    def Height(hash, height):  # Returns the hash of the block currently at :height.
        response = requests.get(f'https://mempool.space/api/block/{hash}/{height}')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        return json_data

    @staticmethod
    def Timestamp(hash, timestamp):
        # Returns the height and the hash of the block closest to the given :timestamp.
        # timestamp : int,unix time

        response = requests.get(f'https://mempool.space/api/block/{hash}/{timestamp}')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        return json_data

    @staticmethod
    def Raw(hash, save=False):  # Returns the raw block representation in binary or saves it to a file.
        url = (f'https://mempool.space/api/block/{hash}/raw')
        urllib.request.urlretrieve(url, hash + '-raw')  # Download the block file from Mempool.space
        with open(hash + '-raw', 'rb') as file:
            data = file.read()  # Copy contents of file to data variable
        if not save:
            os.remove(hash)  # Delete the file
        return data

    @staticmethod
    def Status(hash):
        # Returns the confirmation status of a block.
        # Available fields: in_best_chain (boolean, false for orphaned blocks),
        # next_best (the hash of the next block, only available for blocks in the best chain).

        response = requests.get(f'https://mempool.space/api/block/{hash}/status')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        info = {'in_best_chain': json_data['in_best_chain'],
                'height': json_data['height'],
                'next_best': json_data['next_best']
                }
        return info

    @staticmethod
    def TipHeight():  # Returns the height of the last block.
        response = requests.get(f'https://mempool.space/api/blocks/tip/height')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        return json_data

    @staticmethod
    def TipHash():  # Returns the hash of the last block.
        response = requests.get(f'https://mempool.space/api/blocks/tip/hash')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        return json_data

    @staticmethod
    def txid(hash, index):  # Returns the transaction at index :index within the specified block.
        response = requests.get(f'https://mempool.space/api/block/{hash}/txid/{index}')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        return json_data

    @staticmethod
    def txids(hash):  # Returns a list of all txids in the block.
        response = requests.get(f'https://mempool.space/api/block/{hash}/txids')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        transactions = []  # Initialize the tx array
        for tx in range(len(json_data)):
            transactions.append(tx)
        return transactions

    @staticmethod
    def transactions(hash):
        # Returns a list of transactions in the block
        # (up to 25 transactions beginning at start_index).
        # Transactions returned here do not have the status field,
        # since all the transactions share the same block and confirmation status.
        response = requests.get(f'https://mempool.space/api/block/{hash}/txs')
        json_data = MempoolAPI.validateResponse(response)
        transactions = {}  # Initialize the tx dictionary
        for tx in range(len(json_data)):
            vin, vout = MempoolAPI.inputOutputBuilder(json_data[tx])

            if json_data[tx]['status']['confirmed'] == False:  # Build the dictionary for transaction status
                status = {'confirmed': False}
            else:
                status = {'confirmed': True,
                          'block_height': json_data[tx]['status']['block_height'],
                          'block_hash': json_data[tx]['status']['block_hash'],
                          'block_time': json_data[tx]['status']['block_time']
                          }

            transactions[json_data[tx]['txid']] = {'version': json_data[tx]['version'],
                                                   'locktime': json_data[tx]['locktime'],
                                                   'vin': vin,
                                                   'vout': vout,
                                                   'size': json_data[tx]['size'],
                                                   'weight': json_data[tx]['weight'],
                                                   'fee': json_data[tx]['fee'],
                                                   'status': status
                                                   }
            return transactions
