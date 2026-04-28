import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_key = "CWA-E5510A11-13B3-4E4B-B90B-B413719E16E5"
url = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization={api_key}&format=JSON"

response = requests.get(url, verify=False)
data = response.json()

# 列出第一層與第二層的 Key
print("Keys in data:", data.keys())
if 'cwaopendata' in data:
    print("Keys in cwaopendata:", data['cwaopendata'].keys())
    if 'dataset' in data['cwaopendata']:
        print("Keys in dataset:", data['cwaopendata']['dataset'].keys())
elif 'dataset' in data:
    print("Keys in dataset:", data['dataset'].keys())

# 列出所有區域名稱
locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
for loc in locations:
    print(f"Location: {loc['locationName']}")
