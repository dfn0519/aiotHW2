import requests
import urllib3
import sys
import io

# 強制 stdout 使用 utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api_key = "CWA-E5510A11-13B3-4E4B-B90B-B413719E16E5"
url = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization={api_key}&format=JSON"

response = requests.get(url, verify=False)
data = response.json()
locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
names = [loc['locationName'] for loc in locations]
print("Location names in API:", names)
