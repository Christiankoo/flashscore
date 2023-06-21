import requests

print(requests.get('https://www.google.com',verify=False).content)