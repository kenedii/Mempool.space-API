from MempoolAPI import MempoolAPI
import requests


class Address:
    @staticmethod
    def Address(address):
        # Returns details about an address.
        # Available fields: address, chain_stats, and mempool_stats.
        # chain_stats and mempool_stats each contain an object with tx_count,
        # funded_txo_count, funded_txo_sum, spent_txo_count, and spent_txo_sum.

        response = requests.get(f'https://mempool.space/api/address/{address}')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)

        chain_stats = {'funded_txo_count': json_data['chain_stats']['funded_txo_count'],
                       'funded_txo_sum': json_data['chain_stats']['funded_txo_sum'],
                       'spent_txo_count': json_data['chain_stats']['spent_txo_count'],
                       'spent_txo_sum': json_data['chain_stats']['spent_txo_sum'],
                       'tx_count': json_data['chain_stats']['tx_count'],
                       }
        mempool_stats = {'funded_txo_count': json_data['mempool_stats']['funded_txo_count'],
                         'funded_txo_sum': json_data['mempool_stats']['funded_txo_sum'],
                         'spent_txo_count': json_data['mempool_stats']['spent_txo_count'],
                         'spent_txo_sum': json_data['mempool_stats']['spent_txo_sum'],
                         'tx_count': json_data['mempool_stats']['tx_count'],
                         }
        info = {'chain_stats': chain_stats,
                'mempool_stats': mempool_stats

                }
        return info

    @staticmethod
    def Txs(address):
        # Get transaction history for the specified address/scripthash, sorted with newest first.
        # Returns up to 50 mempool transactions plus the first 25 confirmed transactions.
        # You can request more confirmed transactions using :last_seen_txid (see below).

        response = requests.get(f'https://mempool.space/api/address/{address}/txs')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        transactions = {}  # Initialize dictionary of transactions
        for tx in range(len(json_data)):  # Constructing a transaction
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

    @staticmethod
    def TxsChain(address):
        # Get confirmed transaction history for the specified address/scripthash, sorted with newest first.
        # Returns 25 transactions per page. More can be requested by specifying the last txid seen by the previous query.

        response = requests.get(f'https://mempool.space/api/address/{address}/txs/chain')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        transactions = {}  # Initialize dictionary of transactions
        for tx in range(len(json_data)):  # Constructing a transaction
            vin, vout = MempoolAPI.inputOutputBuilder(json_data[tx])

            status = {'confirmed': True,  # Build the dictionary for transaction status
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

    @staticmethod
    def TxsMempool(address):
        # Get unconfirmed transaction history for the specified address/scripthash.
        # Returns up to 50 transactions (no paging).

        response = requests.get(f'https://mempool.space/api/address/{address}/txs/mempool')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        transactions = {}  # Initialize dictionary of transactions
        for tx in range(len(json_data)):  # Constructing a transaction
            vin, vout = MempoolAPI.inputOutputBuilder(json_data[tx])
            status = {'confirmed': False}  # Build the dictionary for transaction status

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

    @staticmethod
    def AddressUTXO(address):
        # Get the list of unspent transaction outputs associated with the address/scripthash.
        # Available fields: txid, vout, value, and status (with the status of the funding tx).

        response = requests.get(f'https://mempool.space/api/address/{address}/txs/utxo')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)
        transactions = {}  # Initialize dictionary of transactions
        for tx in range(len(json_data)):  # Constructing a transaction
            vin, vout = MempoolAPI.inputOutputBuilder(json_data[tx])

            if not json_data[tx]['status']['confirmed']:  # Build the dictionary for transaction status
                status = {'confirmed': False}
            status = {'confirmed': True,  # Build the dictionary for transaction status
                      'block_height': json_data[tx]['status']['block_height'],
                      'block_hash': json_data[tx]['status']['block_hash'],
                      'block_time': json_data[tx]['status']['block_time']
                      }

            transactions[json_data[tx]['txid']] = {'vout': json_data[tx]['vout'],
                                                   'status': status,
                                                   'value': json_data[tx]['value']
                                                   }

        return transactions

    @staticmethod
    def AddressValidation(address):
        # Returns whether an address is valid or not.
        # Available fields: isvalid (boolean), address (string), scriptPubKey (string),
        # isscript (boolean), iswitness (boolean),
        # witness_version (numeric, optional), and witness_program (string, optional).

        response = requests.get(f'https://mempool.space/api/validate-address/{address}/')
        # Check if the request was successful (status code 200)
        json_data = MempoolAPI.validateResponse(response)

        info = {'isvalid': json_data['isvalid'],
                'scriptPubKey': json_data['scriptPubKey'],
                'isscript': json_data['isscript'],
                'iswitness': json_data['iswitness'],
                }
        if (json_data['iswitness']) == True:
            info['witness_version'] = json_data['witness_version']
            info['witness_program'] = json_data['witness_program']

        return info
