#!/usr/bin/env python
from flask import jsonify
import requests

'''
Send a  GET or POST request to a specified URL

Parameters
-----------

url : str
    The URL to be reached

auth : pair
    The first element represents the user and the other the associated password. To use to authenticate.
    
headers : str
    Headers to pass for the request

data : str
    Data to pass for a POST request
    
params : str
    Parameters to pass for a GET request
    
type : str
    Define the typer of the request. Only 'get' and 'post' are available

format : str
    Define the type of the output. Only 'json' and None are available
    
Returns 
-----------

Json OR Dictionary
    Response of the request
'''
    
def send_request(url, auth=None, headers=None, data=None, params=None, type = 'get', format='json'):
    if(type == 'get'):
        response=requests.get(url, headers=headers, params=params)
    elif(type == 'post'):
        response=requests.post(url,data=data, auth=auth)
    if response.status_code == 200:
        json_resp = response.json()  
        if(format == 'json'):
            return jsonify(json_resp)
        else:
            return json_resp
    else:
        raise Exception(response.reason)