from MempoolAPI import MempoolAPI
import requests
import os
import urllib.request
import json

class Transactions(MempoolAPI):
    @staticmethod
    def ChildPayForParent(txid): # https://mempool.space/docs/api/rest#get-cpfp
        response = requests.get(f'https://mempool.space/api/v1/services/cpfp/{txid}')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Transaction(txid):
        response = requests.get(f'https://mempool.space/api/tx/{txid}')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Hex(txid):
        response = requests.get(f'https://mempool.space/api/tx/{txid}/hex')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def MerkleblockProof(txid):
        response = requests.get(f'https://mempool.space/api/tx/{txid}/merkleblock-proof')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def MerkleProof(txid):
        response = requests.get(f'https://mempool.space/api/tx/{txid}/merkle-proof')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Outspend(txid, vout):
        response = requests.get(f'https://mempool.space/api/tx/{txid}/outspend/{vout}')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Outspends(txid):
        response = requests.get(f'https://mempool.space/api/tx/{txid}/outspends')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Raw(txid):
        response = requests.get(f'https://mempool.space/api/tx/{txid}/raw')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def RBFHistory(txid):
        response = requests.get(f'https://mempool.space/api/tx/{txid}/rbf')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Status(txid):
        response = requests.get(f'https://mempool.space/api/tx/{txid}/status')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Times(txid): # Accepts string or list of txids
        try:
            if type(txid) == str:
                url= f'https://mempool.space/api/v1/transaction-times?txId[]={txid}'
            elif type(txid) == list:
                url = 'https://mempool.space/api/v1/transaction-times?'
                for tx in txid:
                    url += f'txId[]={tx}&'
            response = requests.get(url)
            json_data = MempoolAPI.validateResponse(response)
            return json_data
        except TypeError:
            raise TypeError('Invalid input type. Must be string or list of txids.')

            