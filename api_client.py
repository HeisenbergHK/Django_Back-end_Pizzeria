import requests

endpoint = 'https://github.com/public-apis/public-apis'

data = requests.get(endpoint)

print(data)