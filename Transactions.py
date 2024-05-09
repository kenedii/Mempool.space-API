from MempoolAPI import MempoolAPI
import requests

class Transactions(MempoolAPI):
    @staticmethod
    def ChildPayForParent(txid): # https://mempool.space/docs/api/rest#get-cpfp
        response = requests.get(f'https://mempool.space/api/v1/cpfp/{txid}')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Transaction(txid): # https://mempool.space/docs/api/rest#get-transaction
        response = requests.get(f'https://mempool.space/api/tx/{txid}')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Hex(txid): # https://mempool.space/docs/api/rest#get-transaction-hex
        url = f'https://mempool.space/api/tx/{txid}/hex'
        response = requests.get(url)
        # Check for successful response status code
        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Error: API request failed. Status code: {response.status_code}")
        return response.text
    
    @staticmethod
    def MerkleblockProof(txid): # https://mempool.space/docs/api/rest#get-transaction-merkleblock-proof
        url = f'https://mempool.space/api/tx/{txid}/merkleblock-proof'
        response = requests.get(url)
        # Check for successful response status code
        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Error: API request failed. Status code: {response.status_code}")
        return response.text
    
    @staticmethod 
    def MerkleProof(txid): # https://mempool.space/docs/api/rest#get-transaction-merkle-proof
        response = requests.get(f'https://mempool.space/api/tx/{txid}/merkle-proof')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Outspend(txid, vout): # https://mempool.space/docs/api/rest#get-transaction-outspend
        response = requests.get(f'https://mempool.space/api/tx/{txid}/outspend/{vout}')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Outspends(txid): # https://mempool.space/docs/api/rest#get-transaction-outspends
        response = requests.get(f'https://mempool.space/api/tx/{txid}/outspends')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod # https://mempool.space/docs/api/rest#get-transaction-raw
    def Raw(txid, save=False):
        url = f'https://mempool.space/api/tx/{txid}/raw'
        response = requests.get(url, stream=True)

        # Check for successful response status code
        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Error: API request failed. Status code: {response.status_code}")

        # Return raw binary data
        if not save:
            return response.content

        # Save raw data to disk
        filename = f"{txid}.raw"  # Customize filename if needed
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Raw data saved to: {filename}")
        return None
    
    @staticmethod
    def RBFHistory(txid): # https://mempool.space/docs/api/rest#get-transaction-rbf-history
        response = requests.get(f'https://mempool.space/api/tx/{txid}/rbf')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod
    def Status(txid): # https://mempool.space/docs/api/rest#get-transaction-status
        response = requests.get(f'https://mempool.space/api/tx/{txid}/status')
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    @staticmethod # https://mempool.space/docs/api/rest#get-transaction-times
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