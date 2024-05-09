from MempoolAPI import MempoolAPI
import requests
import os
import urllib.request
import json

class Accelerator(MempoolAPI):
    @staticmethod
    def CalculateEstimatedCosts(txInput):
        url = "https://mempool.space/api/v1/services/accelerator/estimate"

        # Data to send in the request body
        tx_data = {
            "txInput": txInput
        }

        try:
            # Send the POST request with SSL verification disabled (not recommended for production)
            response = requests.post(url, json=tx_data, verify=False)
            response.raise_for_status()  # Raise exception for non-200 status codes

            # Parse the JSON response
            json_data = response.json()
            json_data = dict(json_data)

            return json_data

        except requests.exceptions.RequestException as e:
            print(f"Error: API request failed: {e}")
            return None
        
    @staticmethod
    def PendingAccelerations():
        response = requests.get("https://mempool.space/api/v1/services/accelerator/accelerations")
        json_data = MempoolAPI.validateResponse(response)
        json_data = dict(json_data)
        return json_data
    
    @staticmethod
    def AccelerationHistory(blockHash=""):
        if blockHash:
            url = f"https://mempool.space/api/v1/services/accelerator/accelerations/history?blockHash={blockHash}"
        else:
            url = "https://mempool.space/api/v1/services/accelerator/accelerations/history"
        response = requests.get(url)
        json_data = MempoolAPI.validateResponse(response)
        return json_data
    
    