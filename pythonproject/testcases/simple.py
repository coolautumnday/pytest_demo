import requests

#
url = r'http://127.0.0.1:5000/api/login'

r = requests.post(url, json={"user":"test","pwd":"123456"})

print(r.json()["data"]["token"])
