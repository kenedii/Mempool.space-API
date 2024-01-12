import requests


def validateResponse(response):  # Checks if response is valid
    if response.status_code == 200:
        # Parse JSON data from the response
        json_data = response.json()
    else:  # If error getting json data
        raise Exception('Error retrieving json data. API Endpoint may be down.')


def getDifficultyAdjustment():  # Returns details about difficulty adjustment.
    response = requests.get("https://mempool.space/api/v1/difficulty-adjustment")
    # Check if the request was successful (status code 200)
    json_data = validateResponse(response)

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


def getPrice():  # Returns bitcoin latest price denominated in main currencies.
    response = requests.get("https://mempool.space/api/v1/prices")
    # Check if the request was successful (status code 200)
    json_data = validateResponse(response)

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


# Get Historical Price curl -sSL "https://mempool.space/api/v1/historical-price"

def getAddress(address):
    # Returns details about an address.
    # Available fields: address, chain_stats, and mempool_stats.
    # chain_stats and mempool_stats each contain an object with tx_count,
    # funded_txo_count, funded_txo_sum, spent_txo_count, and spent_txo_sum.

    response = requests.get(f'https://mempool.space/api/address/1{address}')
    # Check if the request was successful (status code 200)
    json_data = validateResponse(response)

    chain_stats = {'funded_txo_count': json_data['funded_txo_count'],
                   'funded_txo_sum': json_data['funded_txo_sum'],
                   'spent_txo_count': json_data['spent_txo_count'],
                   'spent_txo_sum': json_data['spent_txo_sum'],
                   'tx_count': json_data['tx_count'],
                   }
    mempool_stats = {'funded_txo_count': json_data['funded_txo_count'],
                     'funded_txo_sum': json_data['funded_txo_sum'],
                     'spent_txo_count': json_data['spent_txo_count'],
                     'spent_txo_sum': json_data['spent_txo_sum'],
                     'tx_count': json_data['tx_count'],
                     }
    info = {'chain_stats': chain_stats,
            'mempool_stats': mempool_stats

            }
    return info


def getTxs(address):
    # Get transaction history for the specified address/scripthash, sorted with newest first.
    # Returns up to 50 mempool transactions plus the first 25 confirmed transactions.
    # You can request more confirmed transactions using :last_seen_txid (see below).

    response = requests.get(f'https://mempool.space/api/address/{address}/txs')
    # Check if the request was successful (status code 200)
    json_data = validateResponse(response)
    transactions = {}  # Initialize dictionary of transactions
    for tx in range(len(json_data)):  # Constructing a transaction
        vin = {}  # Initialize the dictionary of inputs
        vout = {}  # Initialize the dictionary of outputs

        if json_data[tx]['status']['confirmed'] == False:  # Build the dictionary for transaction status
            status = {'confirmed' == False}
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


def getTxsChain(address):
    # Get confirmed transaction history for the specified address/scripthash, sorted with newest first.
    # Returns 25 transactions per page. More can be requested by specifying the last txid seen by the previous query.

    response = requests.get(f'https://mempool.space/api/address/{address}/txs/chain')
    # Check if the request was successful (status code 200)
    json_data = validateResponse(response)
    transactions = {}  # Initialize dictionary of transactions
    for tx in range(len(json_data)):  # Constructing a transaction
        vin = {}  # Initialize the dictionary of inputs
        vout = {}  # Initialize the dictionary of outputs

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


def getMempoolTxs(address):
    # Get unconfirmed transaction history for the specified address/scripthash.
    # Returns up to 50 transactions (no paging).

    response = requests.get(f'https://mempool.space/api/address/{address}/txs/mempool')
    # Check if the request was successful (status code 200)
    json_data = validateResponse(response)
    transactions = {}  # Initialize dictionary of transactions
    for tx in range(len(json_data)):  # Constructing a transaction
        vin = {}  # Initialize the dictionary of inputs
        vout = {}  # Initialize the dictionary of outputs
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


def getAddressUTXO(address):
    # Get the list of unspent transaction outputs associated with the address/scripthash.
    # Available fields: txid, vout, value, and status (with the status of the funding tx).

    response = requests.get(f'https://mempool.space/api/address/{address}/txs/utxo')
    # Check if the request was successful (status code 200)
    json_data = validateResponse(response)
    transactions = {}  # Initialize dictionary of transactions
    for tx in range(len(json_data)):  # Constructing a transaction
        vin = {}  # Initialize the dictionary of inputs
        vout = {}  # Initialize the dictionary of outputs

        if not json_data[tx]['status']['confirmed']:  # Build the dictionary for transaction status
            status = {'confirmed' == False}
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


def getAddressValidation(address):
    # Returns whether an address is valid or not.
    # Available fields: isvalid (boolean), address (string), scriptPubKey (string),
    # isscript (boolean), iswitness (boolean),
    # witness_version (numeric, optional), and witness_program (string, optional).

    response = requests.get(f'https://mempool.space/api/validate-address/{address}/')
    # Check if the request was successful (status code 200)
    json_data = validateResponse(response)

    info = {'isvalid': json_data['isvalid'],
            'scriptPubKey': json_data['scriptPubKey'],
            'isscript': json_data['isscript'],
            'iswitness': json_data['iswitness'],
            }
    if (json_data['iswitness']) == True:
        info['witness_version'] = json_data['witness_version']
        info['witness_program'] = json_data['witness_program']

    return info
