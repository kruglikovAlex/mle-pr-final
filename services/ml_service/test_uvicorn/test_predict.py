import requests

recommendations_url = "http://127.0.0.1:8088"

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
params = {"user_id": 1407515, "item_id": 166325}

resp = requests.get(recommendations_url + "/get", headers=headers, params=params)
if resp.status_code == 200:
    result = resp.json()
else:
    result = None
    print(f"status code: {resp.status_code}")
    
print(result) 