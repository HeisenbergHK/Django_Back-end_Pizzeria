import requests, json

endpoint = 'http://localhost:8000/api/orders'

respond = requests.get(endpoint)

print(respond.text)