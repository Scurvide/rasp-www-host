import requests
import json

url = 'http://192.168.1.107:8000/send/'
client = requests.session()
csrf = client.get( url ).cookies[ 'csrftoken' ]

payload = { 'name': 'Petteri', 'secretid': 'dkw21ssdXa', 'datatype': 'instance', 'point': 63.4311 }
payload = json.dumps( payload )
headers = { 'X-CSRFToken': csrf }

resp = client.post( url, data = payload, headers = headers )
print(resp.content)
