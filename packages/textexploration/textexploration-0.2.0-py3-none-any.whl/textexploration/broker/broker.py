import requests
import json
from .request.request import Request
from .response.response import Response

class Broker:
    
    def __init__(self, url):
        #define url
        self.url = url
        self.timeout = 180
        
    def do_request(self, request):    
        """Perform a BrokerRequest"""
        if type(request) == Request:
            data = json.dumps(request.raw())  
        elif type(request) == dict:
            data = json.dumps(request)  
        elif type(request) == str:
            data = request
        else:
            raise Exception("unsupported type of request")  
        try: 
            response = requests.post(self.url, data, timeout=self.timeout)
            response.raise_for_status() 
            return(Response(response.text))                        
        except requests.exceptions.HTTPError as httpErr: 
            print ("Http Error:",httpErr) 
        except requests.exceptions.ConnectionError as connErr: 
            print ("Error Connecting:",connErr) 
        except requests.exceptions.Timeout as timeOutErr: 
            print ("Timeout Error:",timeOutErr) 
        except requests.exceptions.RequestException as reqErr: 
            print ("Something Else:",reqErr) 
        raise Exception("no (valid) response from broker")
        
        
