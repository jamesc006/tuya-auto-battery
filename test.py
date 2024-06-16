import requests


response = requests.post("http://127.0.0.1:8000/switch", json={"state": "off"})

print(response.text)
